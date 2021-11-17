import numpy as np
from typing import List, Tuple
from random import shuffle

# dictionary of matching genders/gender preferences i.e. for each key, val pair, if A's gender is the key, 
# then B would only be potentially attracted to A if B's gender preference is present in val
gender_match_dict = {
    'Female' : ['Women', 'Bisexual', 'Pansexual', 'Lesbian'],
    'Male' : ['Men', 'Bisexual', 'Pansexual', 'Gay'],
    'Nonbinary' : ['Pansexual'],
}

# helper function to generate dictionary of preferences i.e. how does each member of
# group 1 rank each member of group2
def generate_prefs(group1, group2):
    group1_preferences = dict()
    for g1_mem in group1:
        # filter only the scores that correspond to the receivers
        g1_mem_scores = np.array(raw_scores[g1_mem])[np.array(group2)]
        
        # set score to zero if gender does not align w/ g1_mem's preferences
        for i, g2_mem in enumerate(group2):
            if gender_preferences[g1_mem] not in gender_match_dict[genders[g2_mem]]:
                g1_mem_scores[i] = 0

        # sort the receivers based on prop's scores in descending order
        group1_preferences[g1_mem] = np.array(group2)[np.argsort(g1_mem_scores)[::-1]].tolist()
    return group1_preferences

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    matches = dict()
    num_people = len(genders)
    lst = [i for i in range(num_people)]
    
    # randomly split into 2 groups
    shuffle(lst)
    proposers = lst[:num_people // 2]
    receivers = lst[num_people // 2:]
    
    prop_prefs = generate_prefs(proposers, receivers)
    rec_prefs = generate_prefs(receivers, proposers)
    
    free_proposers = proposers
    # continue until all proposers have been matched
    while free_proposers:
        prop = free_proposers[0]
        for rec in prop_prefs[prop]:
            # if receiver is unmatched
            if rec not in matches.keys():
                matches[rec] = prop
                free_proposers.remove(prop)
                break

            # if receiver is matched but new match is better
            elif rec_prefs[rec].index(prop) < rec_prefs[rec].index(matches[rec]):
                free_proposers.append(matches[rec])
                matches[rec] = prop
                free_proposers.remove(prop)
                break
    # matches stored in dict as receiver:proposer pairs
    return [(v,k) for k,v in matches.items()]

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)

