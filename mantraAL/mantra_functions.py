from schemes_allowed_changes import schemes, compatible_roles, allowed_changes
import pickle
import random
from itertools import combinations
import copy

f=open('esempi_panchina.pckl', 'rb')
lineups1 = pickle.load(f)
lineups2 = pickle.load(f)
f.close()

f=open('esempi_voti.pckl', 'rb')
players_database = pickle.load(f)
f.close()

l = open('/Users/andrea/Desktop/fanta2_0/all_roles.pckl', 'rb')
all_roles = pickle.load(l)
l.close()

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
        if not set(all_roles[player[1]]).isdisjoint(roles):
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
        if not set(all_roles[player[1]]).isdisjoint(roles):
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
        if not set(all_roles[player[1]]).isdisjoint(roles):
            new_attack.append(player)
            
    all_possible_attacks = combinations(new_attack, n_forwards_in_module)
    
    return list(all_possible_attacks)

def all_players_are_different(list1, list2, list3):
    if (len(set(list1).intersection(list2)) == 0
    and len(set(list1).intersection(list3)) == 0
    and len(set(list2).intersection(list3)) == 0):
        return True
    else:
        return False


def valid_lineups(list_of_tuples):
    
    field,bench,n_subst = players_with_vote(list_of_tuples, mode='ST')
    
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
            
            possible_defenses = check_defense(lineup,'433')
            possible_midfields = check_midfield(lineup,'433')
            possible_attacks = check_attack(lineup,'433')
                        
            for defense in possible_defenses:
                clean_def = [i[1] for i in defense]
                for midfield in possible_midfields:
                    clean_mid = [i[1] for i in midfield]
                    for attack in possible_attacks:
                        clean_att = [i[1] for i in attack]
                        
                        if all_players_are_different(clean_def, clean_mid, clean_att):
                            all_valid_lineups.append(lineup)
                            
            
    return all_valid_lineups
    
def optimal_solution(list_of_tuples, schemes_of_module):    
    
    def reduce_roles(list_of_tuples, schemes_of_module):
        needed_roles = set([x for y in schemes_of_module for x in y.split('/')])
        
        reduced_list = []
        
        for i in list_of_tuples:
            old_roles = i[2]
            new_roles = copy.copy(old_roles)
            for x in old_roles:
                if not x in needed_roles:
                    new_roles.remove(x)
            
            reduced_list.append((i[0], i[1], new_roles))
        
        return reduced_list
    
    def deploy_players(reduced_list, schemes_of_module):
        
        new_list = copy.copy(reduced_list)
        new_schemes = copy.copy(schemes_of_module)
        
        for player in reduced_list:
            role = player[2]
            if len(role)==1:
                role_to_delete = set(compatible_roles[role[0]]).intersection(schemes_of_module)
                role_to_delete = list(role_to_delete)[0]
                new_list.remove(player)
                try:
                    new_schemes.remove(role_to_delete)
                except ValueError:
                    return False
                    
        return new_list,new_schemes
    
    def operate(list_of_tuples, schemes_of_module):
        try:
            reduced_list = reduce_roles(list_of_tuples, schemes_of_module)
            deployed_list,new_schemes = deploy_players(reduced_list, schemes_of_module)
            
            if len(deployed_list) == 0:
                return original
            elif len(deployed_list) == len(list_of_tuples):
                return False
            else:
                return operate(deployed_list,new_schemes)
        except TypeError:
            return False
    
    original = copy.copy(list_of_tuples)
    
    res = operate(list_of_tuples, schemes_of_module)
    return res
            








