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

def n_players_role(list_of_tuples, list_of_roles):
    count = 0
    for i in list_of_tuples:
        if set(i[2]).intersection(list_of_roles):
            count += 1
            
    return count

def check_defense(list_of_tuples, module):
    n_defenders_in_module = int(module[0])
    roles = ['Dc','Dd','Ds']
    new_defense = []
    
    if n_players_role(list_of_tuples, roles) < n_defenders_in_module:
        return False
    
    for player in list_of_tuples:
        if not set(player[2]).isdisjoint(roles):
            new_defense.append(player)
            
    all_possible_defenses = combinations(new_defense, n_defenders_in_module)
            
    return list(all_possible_defenses)
    
def check_midfield(list_of_tuples, module):
    n_midfielders_in_module = sum([int(x) for x in list(module[1:-1])])
    roles = ['E','C','M','T','W']
    new_midfield = []
    
    if n_players_role(list_of_tuples, roles) < n_midfielders_in_module:
        return False
    
    for player in list_of_tuples:
        if not set(player[2]).isdisjoint(roles):
            new_midfield.append(player)
            
    all_possible_midfields = combinations(new_midfield, n_midfielders_in_module)
    
    return list(all_possible_midfields)

def check_attack(list_of_tuples, module):
    n_forwards_in_module = int(module[-1])
    roles = ['Pc','A','W']
    new_attack = []
    
    if n_players_role(list_of_tuples, roles) < n_forwards_in_module:
        return False
    
    for player in list_of_tuples:
        if not set(player[2]).isdisjoint(roles):
            new_attack.append(player)
            
    all_possible_attacks = combinations(new_attack, n_forwards_in_module)
    
    return list(all_possible_attacks)


def optimal_solution(field, bench, n_subst):
    players_from_bench = list(combinations(bench, n_subst))
    all_lineups = []
    all_valid_lineups = []
    
    for block in players_from_bench:
        new_field = copy.copy(field)
        for player in block:
            new_field.append(player)
        all_lineups.append(new_field)
    
    for lineup in all_lineups:
        if (check_defense(lineup,'433')
        and check_midfield(lineup,'433')
        and check_attack(lineup,'433')):
            
            a = check_defense(lineup,'433')
            b = check_midfield(lineup,'433')
            c = check_attack(lineup,'433')
                        
            for x in a:
                new_a = [i[1] for i in x]
                for y in b:
                    new_b = [i[1] for i in y]
                    for z in c:
                        new_c = [i[1] for i in z]
                        
                        if (len(set(new_a).intersection(new_b)) == 0
                        and len(set(new_a).intersection(new_c)) == 0
                        and len(set(new_b).intersection(new_c)) == 0):
                            all_valid_lineups.append(lineup)
            
    return all_valid_lineups
    
    













