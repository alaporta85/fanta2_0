from schemes_allowed_changes import schemes, allowed_changes
import pickle
import random
from itertools import combinations
import copy

f=open('esempi_panchina.pckl', 'rb')
lineups = pickle.load(f)
f.close()

f=open('esempi_voti.pckl', 'rb')
players_database = pickle.load(f)
f.close()

def take_vote_from_database(player, day, mode='ST'):
    try:
        for atuple in players_database[player]:
            if atuple[0] == day and mode == 'FG':
                return atuple[2]
            elif atuple[0] == day:
                return atuple[3]
        return 'n.e.'
    except KeyError:
        return 'n.e.'


def players_with_vote(list_of_tuples, mode='ST'):
    field = []
    bench = []
    for player in list_of_tuples:
        day = int(player[0].split()[1])
        if mode == 'FG':
            vote = take_vote_from_database(player[1], day, mode='FG')
        else:
            vote = take_vote_from_database(player[1], day)
        if vote != 'n.e.' and list_of_tuples.index(player) <= 10:
            field.append((player[0],player[1],player[2],vote))
        elif vote != 'n.e.' and list_of_tuples.index(player) > 10:
            bench.append((player[0],player[1],player[2],vote))
            
    n_subst = 11 - len(field)
    if n_subst > 3:
        n_subst = 3
    
    return field, bench, n_subst


def optimal_solution(field, bench, n_subst):
    players_from_bench = list(combinations(bench, n_subst))
    
    for block in players_from_bench:
        new_field = copy.copy(field)
        for player in block:
            new_field.append(player)
    


