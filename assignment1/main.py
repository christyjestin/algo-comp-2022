#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

# initialize variables that will be assigned within functions below
response_stats = []
users = []
num_responses = 0

GRAD_YEAR_GAP_WEIGHT = 0.1
MAX_GRAD_YEAR_GAP = 3

def generate_stats():
    global num_responses
    global response_stats
    # ensure that all users have the same number of responses
    num_responses = len(users[0].responses)
    for user in users:
        if len(user.responses)!=num_responses:
            raise ValueError("The number of responses is not the same for all users")

    response_stats = []

    for i in range(num_responses):
        responses = [user.responses[i] for user in users]
        dist_dict = dict()
        for resp in responses:
            if resp not in dist_dict.keys():
                dist_dict[resp] = 0
            dist_dict[resp] += 1 / len(responses)
        response_stats.append(dist_dict)


def compute_similarity(stats, response1, response2):
    if response1!=response2:
        return 0
    return 1 / (1 + stats[response1])

# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    if user1.gender not in user2.preferences or user2.gender not in user1.preferences:
        return 0
    grad_year_gap = abs(user1.grad_year - user2.grad_year)
    score = GRAD_YEAR_GAP_WEIGHT * (1 - grad_year_gap / MAX_GRAD_YEAR_GAP)
    if not response_stats:
        generate_stats()
    multiplier = (1 - GRAD_YEAR_GAP_WEIGHT)  * (1 / num_responses)
    for i in range(num_responses):
        score += multiplier * compute_similarity(response_stats[i], user1.responses[i], user2.responses[i])
    return score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
