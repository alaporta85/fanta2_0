from schemes_allowed_changes import schemes, compatible_roles, malus_roles
import pickle
from itertools import combinations, permutations
import copy

f=open('esempi_panchina.pckl', 'rb')
lineups1 = pickle.load(f)
lineups2 = pickle.load(f)
lineups3 = pickle.load(f)
lineups4 = pickle.load(f)
lineups5 = pickle.load(f)
lineups6 = pickle.load(f)
lineups7 = pickle.load(f)
f.close()

f=open('esempi_voti.pckl', 'rb')
players_database = pickle.load(f)
f.close()

l = open('/Users/andrea/Desktop/fanta2_0/all_roles.pckl', 'rb')
all_roles = pickle.load(l)
l.close()


def take_vote_from_database(player, day, mode='ST'):
    
    '''This function returns the vote from the database for the specified
       player in that specific day. By default, the mode is 'ST' (statistical)
       which means we take the Alvin482 vote. When 'FG' is specified as mode
       than we take the normal votes from Fantagazzetta. In case player does
       NOT have a vote in that day, it manages the KeyError and returns n.e.
       (not evaluated).'''
       
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
    
    '''This function returns two lists (field and bench) and a number (n_subst)
       which represent the players who received vote in the field, in the bench
       and the number of substitutions needed by the fantateam, respectively.
       In case more than 3 substitutions are needed, the value for n_subst
       will be set to 3 anyway.'''
       
    field = []
    bench = []
    
    for player in list_of_tuples:
        
        # Extract the day
        day = int(player[0].split()[1])
        
        # Extract the vote, FG or ST
        if mode == 'FG':
            vote = take_vote_from_database(player[1], day, mode='FG')
        else:
            vote = take_vote_from_database(player[1], day)
        
        # If player has a vote on that day and his position is in the first
        # eleven spots we assign him to the field
        if vote != 'n.e.' and list_of_tuples.index(player) <= 10:
            field.append((player[0],player[1],player[2],vote))
        
        # Otherwise to the bench
        elif vote != 'n.e.' and list_of_tuples.index(player) > 10:
            bench.append((player[0],player[1],player[2],vote))
    
    # Set the number of substitutions needed        
    n_subst = 11 - len(field)
    if n_subst > 3:
        n_subst = 3
    
    return field, bench, n_subst

def n_players_role(list_of_tuples, list_of_roles):
    
    '''This function returns the number of players whose list of roles contain
       at least one element in common with the list_of_roles given as input.'''
       
    count = 0
    for i in list_of_tuples:
        if set(i[2]).intersection(list_of_roles):
            count += 1
            
    return count

def check_defense(list_of_tuples, module):
    
    '''This function returns a list with all possible combinations of defenses
       for a given lineup (list_of_tuples) according to the module. We do this
       by first selecting all the players in the lineup who are allowed to play
       as defenders and finally generating all the possible combinations of
       them in groups of N, where N is the number of defenders allowed by the
       selected module.'''
    
    n_defenders_in_module = int(module[0])
    roles = ['Dc','Dd','Ds']     # Allowed roles
    new_defense = []
    
    # As a first filter, if in the whole lineup the number of defenders is less
    # than the number requested by the selected module or there are more than
    # one goal-keeper it returns False: it is already an INVALID lineup
    if (n_players_role(list_of_tuples, roles) < n_defenders_in_module
        or n_players_role(list_of_tuples, ['Por']) > 1):
        return False
    
    # In case first condition is accomplished, we start selecting the players
    # who will form all the possible defenses. To do that we check if AT LEAST
    # one of each player roles' in the list of the allowed roles. If yes, we
    # include the player in the final list (new_defense)
    for player in list_of_tuples:
        if not set(all_roles[player[1]]).isdisjoint(roles):
            new_defense.append(player)
            
    # Generate all the combinations of defenders
    all_possible_defenses = combinations(new_defense, n_defenders_in_module)
            
    return list(all_possible_defenses)
    
def check_midfield(list_of_tuples, module):
    
    '''This function returns a list with all possible combinations of
       midfielders for a given lineup (list_of_tuples) according to the module.
       We do this by first selecting all the players in the lineup who are
       allowed to play as midfielders and finally generating all the possible
       combinations of them in groups of N, where N is the number of
       midfielders allowed by the selected module.'''
       
    n_midfielders_in_module = sum([int(x) for x in list(module[1:-1])])
    roles = ['E','C','M','T','W']       # Allowed roles
    new_midfield = []
    
    # As a first filter, if in the whole lineup the number of midfielders is
    # less than the number requested by the selected module it returns False:
    # it is already an INVALID lineup
    if n_players_role(list_of_tuples, roles) < n_midfielders_in_module:
        return False
    
    # In case first condition is accomplished, we start selecting the players
    # who will form all the possible midfields. To do that we check if AT LEAST
    # one of each player roles' in the list of the allowed roles. If yes, we
    # include the player in the final list (new_midfield)
    for player in list_of_tuples:
        if not set(all_roles[player[1]]).isdisjoint(roles):
            new_midfield.append(player)
    
    # Generate all the combinations of midfielders
    all_possible_midfields = combinations(new_midfield,
                                          n_midfielders_in_module)
    
    return list(all_possible_midfields)

def check_attack(list_of_tuples, module):
    
    '''This function returns a list with all possible combinations of attacks
       for a given lineup (list_of_tuples) according to the module. We do this
       by first selecting all the players in the lineup who are allowed to play
       as forwards and finally generating all the possible combinations of
       them in groups of N, where N is the number of forwards allowed by the
       selected module.'''
       
    n_forwards_in_module = int(module[-1])
    roles = ['Pc','A','W']         # Allowed roles
    new_attack = []
    
    # As a first filter, if in the whole lineup the number of forwards is less
    # than the number requested by the selected module or there are more than
    # two Pc it returns False: it is already an INVALID lineup
    if (n_players_role(list_of_tuples, roles) < n_forwards_in_module
        or n_players_role(list_of_tuples, ['Pc']) > 2):
        return False
    
    # In case first condition is accomplished, we start selecting the players
    # who will form all the possible attacks. To do that we check if AT LEAST
    # one of each player roles' in the list of the allowed roles. If yes, we
    # include the player in the final list (new_attack)
    for player in list_of_tuples:
        if not set(all_roles[player[1]]).isdisjoint(roles):
            new_attack.append(player)
    
    # Generate all the combinations of forwards
    all_possible_attacks = combinations(new_attack, n_forwards_in_module)
    
    return list(all_possible_attacks)

def all_players_are_different(list1, list2, list3):
    
    '''This function checks if the intersection between three lists is zero.
       It is used to check if there are NOT repeated players in all the
       possible combinations of defenses, midfields and attacks that will be
       generated. If intersection is equal to 0 it means that are players are
       different and the lineup MIGHT be a valid one (there will be more
       filters).'''
    
    # From the given lists we create other lists containing only the name of
    # the players
    new_list1 = [player[1] for player in list1]
    new_list2 = [player[1] for player in list2]
    new_list3 = [player[1] for player in list3]
    
    if (len(set(new_list1).intersection(new_list2)) == 0
    and len(set(new_list1).intersection(new_list3)) == 0
    and len(set(new_list2).intersection(new_list3)) == 0):
        return True
    else:
        return False


def valid_lineups(list_of_tuples, module, solution, mode='ST'):
    
    '''This function returns a list containing ALL the valid combinations of
       the original lineup given by the fantaplayer (list_of_tuples). "Valid"
       means that all of them are lineups that could be perfectly working
       according to the rules of the game. If "solution" == "optimal"
       than it will return all the combination AFTER applying all the filters
       definded before. If "solution" == "efficient" it returns all the
       combinations WITHOUT ANY filter.'''
    
    if mode == 'FG':
        field,bench,n_subst = players_with_vote(list_of_tuples, 'FG')
    else:
        field,bench,n_subst = players_with_vote(list_of_tuples)
    
    # This block of code is used to handle the substitution of the goal-keeper
    # which according to the rules has to be substituted as first ALWAYS.
    # If there are no goal-keepers with vote in the lineup (field and bench) we
    # only decrease the number of allowed substitutions: the team will play
    # without goal-keeper
    if (n_players_role(field, ['Por']) == 0
        and n_players_role(bench, ['Por']) == 0):
        n_subst = n_subst - 1
    
    # If in the bench there are goal-keepers with vote, we select the first one
    # (if more than one is present) and insert him at the beginning of the
    # field list. Finally we decrease the number of allowed substitutions
    elif (n_players_role(field, ['Por']) == 0
        and n_players_role(bench, ['Por']) != 0):
        gkeepers = []
        for player in bench:
            if player[2] == ['Por']:
                gkeepers.append(player)
        field.insert(0, gkeepers[0])
        n_subst = n_subst - 1
    
    # Once the goal-keeper issue is over, we generate all the combination of
    # the players in the bench. Each combination will be made of a number of
    # players equal to the number of allowed substitutions
    players_from_bench = list(combinations(bench, n_subst))
    all_lineups = []                  # All candidates
    optimal_lineups = []              # All candidates for an optimal solution
    
    # First we combine players in the field with each combination of players
    # from the bench. The resulting lineup will be a candidate to be checked
    for block in players_from_bench:
        new_field = copy.copy(field)
        for player in block:
            new_field.append(player)
        all_lineups.append(new_field)
    
    # Now for each candidate we apply the filters defined before
    for lineup in all_lineups:
        
        # If the three filters for defense, midfield and attack are satisfied
        # (ALL of them have to be satisfied) it means that, as requested by the
        # filters, in each area we have the minimum number of players requested
        # by the selected module
        if (check_defense(lineup, module)
        and check_midfield(lineup, module)
        and check_attack(lineup, module)):
            
            # If the candidate has a goal-keeper we assign him to a variable
            if n_players_role(lineup, ['Por']):
                gkeeper = lineup[0]
            
            # Define all the combinations of defense, midfield and attack
            # separately
            possible_defenses = check_defense(lineup, module)
            possible_midfields = check_midfield(lineup, module)
            possible_attacks = check_attack(lineup, module)
            
            # Cross all the combination between them and apply the last filter
            for defense in possible_defenses:
                for midfield in possible_midfields:
                    for attack in possible_attacks:
                        
                        # If there are no repeated players we create the new
                        # lineup and it will be one of the valid candidates
                        if all_players_are_different(defense,
                                                     midfield,
                                                     attack):
                            
                            new_lineup = [gkeeper] + list(defense)\
                                       + list(midfield) + list(attack)
                            
                            optimal_lineups.append(new_lineup)                            
            
    if solution == 'optimal':
        return optimal_lineups
    elif solution == 'efficient':
        return all_lineups
    
def reduce_roles(list_of_tuples, roles_of_module, solution):
        
        '''This function eliminates from the list of roles of each player all
           the roles that are not allowed in the chosen module. For example, if
           the list of roles of a player is ['Dc', 'Dd'] and the module is 343
           (or any with 3 defenders) this function will return ['Dc'] as list
           of roles of the player because 'Dd' is not allowed in 343.'''
                
        # Create the list of roles needed in the module. Roles like 'M/C' will
        # be split as 'M' and 'C'
        needed_roles = set([x for y in roles_of_module for x in y.split('/')])
        
        reduced_list = []
        
        for player in list_of_tuples:
            old_roles = player[2]
            new_roles = copy.copy(old_roles)
            
            # If the player has no valid roles for the module we do not do
            # anything (instead of deleting all of them) because those players
            # will be the ones that will be deployed at the end and will
            # receive a malus
            if set(old_roles).isdisjoint(needed_roles) and solution == 'adapted':
                    pass
            elif set(old_roles).isdisjoint(needed_roles) and solution == 'optimal':
                    return False
                
            # Otherwise we delete only the ones which are not allowed
            else:
                for role in old_roles:
                    if role not in needed_roles and len(new_roles) > 1:
                        new_roles.remove(role)
                
            
            reduced_list.append((player[0], player[1], new_roles))
        
        return reduced_list
    
def deploy_players(reduced_list, roles_of_module, solution):
        
        '''This function deploys the players in the lineup according to the
           module. It deploys only the players who have one role, delete the
           role from the roles to be covered and delete the player from the
           players to be deployed. It returns the lists of the non-deployed
           players and non-covered roles.'''
        
        new_list = copy.copy(reduced_list)
        new_schemes = copy.copy(roles_of_module)
        
        for player in reduced_list:
            role = player[2]
            
            # First we try to delete the same role: if player is a 'M' than we
            # look for 'M' in the positions to be covered
            if len(role)==1 and role[0] in new_schemes:
                role_to_delete = role[0]
                new_list.remove(player)
                new_schemes.remove(role_to_delete)
            
            # If there is no 'M' than we look for the compatible roles, which
            # are the roles where 'M' is contained ('M/C' in our case)
            elif (len(role)==1
                  and set(compatible_roles[role[0]])\
                  .intersection(new_schemes)):
                
                role_to_delete = set(compatible_roles[role[0]])\
                                                 .intersection(new_schemes)
                role_to_delete = list(role_to_delete)[0]
                new_list.remove(player)
                new_schemes.remove(role_to_delete)
            
            # If the role is not present in the positions to be covered we do
            # not do anything, just skip it (it will be used later for malus)
            elif len(role)==1 and role[0] not in new_schemes and solution == 'optimal':
                return False
            elif len(role)==1 and role[0] not in new_schemes and solution == 'adapted':
                pass
                    
        return new_list,new_schemes
    
    
def find_solution(list_of_tuples, module):
    
    '''This function checks if a solution is available, according to the module.
       A solution is found when all the players thah contributes to
       the final score (including the ones entered from the bench) can be
       arranged in a way consistent with possible roles defined by the module.
       It returns the final lineup that will be used to calculate the final
       score in case it exists. Otherwise it returns False.'''

    
    def same_roles_left(deployed_list, new_schemes):
        
        '''This function is used to handle the case when for example there is
           a last player to be deployed with roles ['T', 'W'] and tho role to
           be covered is 'T/W'. In this situation the reduce_role function will
           not reduce anything and the deploy_players function will return
           False, causing a wrong result. It handles also the case with more
           than one player left to deploy.'''
        
        res = [role for roles in new_schemes for role in roles.split('/')]
        
        for player in deployed_list:
            roles = player[2]
            for role in roles:
                if role in res:
                    res.remove(role)
        
        if len(res)==0:
            return True
        else:
            return False
    
    def calculate(candidate, roles_of_module):
        
        '''This function recursively applies the reduce_roles and deploy_players
           functions to look for the right solution, if it exists.'''
        
        # "try" method is used to handle the cases when the function
        # deploy_players returns False instead of the two lists (to_deploy_list
        # and roles_left). In that case we would have
        #
        #            to_deploy_list,roles_left = False
        #
        # which gives a TypeError. In our case the error means that the
        # candidate can not be a solution and it returns False.
        try:
            reduced_list = reduce_roles(candidate, roles_of_module, 'optimal')
            to_deploy_list,roles_left = deploy_players(reduced_list, roles_of_module, 'optimal')
            
            # If all players are deployed the lineup represents an optimal
            # solution and we return it
            if len(to_deploy_list) == 0:
                return True
            
            # If the function deploy_players is NOT able to deploy any player
            # but the roles to deploy are the same as the roles left, the
            # lineup represents an optimal solution and we return it
            elif (len(to_deploy_list) == len(candidate)
            and same_roles_left(to_deploy_list, roles_left)):
                return True
            
            # If the function deploy_players is NOT able to deploy any player
            # and the roles to deploy are different from the roles left, the
            # lineup is NOT an optimal solution and we return False
            elif (len(to_deploy_list) == len(candidate)
            and not same_roles_left(to_deploy_list, roles_left)):
                return False
            
            # Otherwise we repeat the process
            else:
                return calculate(to_deploy_list, roles_left)
            
        except TypeError:
            return False
    
    # If a solution is found we return True
    if calculate(list_of_tuples, schemes[module]):
        return True
    else:
        return False

    
def find_adapted_solution(list_of_tuples, module):
    
    '''This function checks if an adapted solution is available, according to
       the module. By using all the functions defined inside it will return
       True if an adapted solution exists and False if not.'''
       
    
    def any_in_malus_role(roles_to_check, substitute):
        
        '''This function splits roles like 'M/C' in ['M','C'] and checks if any
           of them can be covered with malus by the role 'substitute'. If at
           least one of them can be covered it returns True, else False.'''
        
        new_roles = roles_to_check.split('/')
        
        count = 0
        
        for role in new_roles:
            if role in malus_roles[substitute]:
                count += 1
                
        if count == 0:
            return False
        else:
            return True
    
    def malus_roles_left(players_left, roles_left):
        
        '''This function is used to handle the case when for example there are
           still players to be deployed in players_left list but none of the
           roles of such players is in the roles_left list. So we check whether
           it is possible to deploy ALL of them with 1 or more malus.'''
        
        # Depending on the module the available roles with malus for 'W' change
        special_modules = ['352', '442', '4411']
        
        # To store the roles which are left to cover after modifing the
        # roles_left list according to the special modules
        adapted_roles = []
        
        # Permutations of the players still to be deployed. We do that because
        # we only want that combination of players in which ALL of them are
        # deployed
        players_perm = permutations(players_left, len(players_left))
        
        # For modules in special_modules the rules for the substitutions of
        # the role 'W' are different. So here we take the roles inside the
        # input roles_left and directly append them in adapted roles if they
        # are != 'W'. In case there is a 'W' between the players to be deployed
        # we than modify it to be either 'W1' or 'W2' depending on the module
        # and append them
        for role in roles_left:
            if role == 'W' and module in special_modules:
                adapted_roles.append('W2')
            elif role == 'W' and module not in special_modules:
                adapted_roles.append('W1')
            else:
                adapted_roles.append(role)
        
        n_malus = 0
        
        # For each permutation of players to be deployed        
        for perm in players_perm:
            
            n_malus = len(perm)
            
            # Make a copy of the roles to be covered so we can use it later to
            # delete roles that we are able to cover
            copy_of_adapted_roles = copy.copy(adapted_roles)
            
            # For each player in the permutation we make a copy of his roles
            # and for each of these roles we check if they are allowed to cover
            # (with a malus) any of the still uncovered positions in the field.
            # If yes we delete the role which is now covered from the list of
            # uncovered role, delete it also from the roles of the player and
            # finally break the loop to be able to go to the next player in the
            # permutation. If no we just break the loop
            for player in perm:
                roles = player[2]
                copy_of_roles = copy.copy(roles)
                for role in roles:
                    for adapted_role in copy_of_adapted_roles:
                        if any_in_malus_role(adapted_role, role):
                            copy_of_adapted_roles.remove(adapted_role)
                            copy_of_roles.remove(role)
                            break
                        else:
                            break
                    
                    # This is to decide if we need to procede with the next
                    # player of the permutation (condition satisfied) or with
                    # the next role, if there is any, of the same player.
                    if len(copy_of_roles) != len(roles):
                        break
            
            # If after all the players in the permutation we have covered all
            # the positions in the field we return True, otherwise we check
            # the next permutation of players
            if len(copy_of_adapted_roles) == 0:
                return n_malus
        
        # If after all the permutaions we still have positions in the field
        # still to be covered, this means that it is not possible to find an
        # adapted solution for the original lineup and we return False
        if len(copy_of_adapted_roles) > 0:
            return False
        
    
    def calculate(candidate, roles_of_module):
        
        '''This function recursively applies the reduce_roles and deploy_players
           functions to look for the right solution, if it exists.'''
        
# =============================================================================
#         def role_to_delete(to_deploy_list, roles_to_reduce):
#             
#             all_roles_comb = combinations(roles_to_reduce, len(to_deploy_list))
#             
#             reduced_roles = 0
#             
#             malus = 4
#             
#             for comb in all_roles_comb:
#                 for role in comb:
# =============================================================================
                    
        
        # "try" method is used to handle the cases when the function
        # deploy_players returns False instead of the two lists (to_deploy_list
        # and roles_left). In that case we would have
        #
        #            to_deploy_list,roles_left = False
        #
        # which gives a TypeError. In our case the error means that the
        # candidate can not be a solution and it returns False.
        try:
            reduced_list = reduce_roles(candidate, roles_of_module, 'adapted')
            to_deploy_list,roles_left = deploy_players(reduced_list, roles_of_module, 'adapted')
            
            if len(to_deploy_list) < len(roles_left):
                print('esatto')
            
            
# =============================================================================
#             # If all players are deployed the lineup represents an optimal
#             # solution and we return it
#             if len(to_deploy_list) == 0:
#                 return True
# =============================================================================
            
            # If the function deploy_players is NOT able to deploy any player
            # but the roles to deploy are the same as the roles left, the
            # lineup represents an optimal solution and we return it
            elif (len(to_deploy_list) == len(candidate)
            and malus_roles_left(to_deploy_list, roles_left)):
                return malus_roles_left(to_deploy_list, roles_left)
            
            # If the function deploy_players is NOT able to deploy any player
            # and the roles to deploy are different from the roles left, the
            # lineup is NOT an optimal solution and we return False
            elif (len(to_deploy_list) == len(candidate)
            and not malus_roles_left(to_deploy_list, roles_left)):
                return False
            
            # Otherwise we repeat the process
            else:
                return calculate(to_deploy_list, roles_left)
            
        except TypeError:
            return False
        
    # If a solution is found we return True
    if calculate(list_of_tuples, schemes[module]):
        return calculate(list_of_tuples, schemes[module])
    else:
        return False
    

    
def MANTRA_simulation(lineup, module, mode='ST'):
    
    '''This function returns the lineup chosen by the fantaplayer where all the
       players who contribute to the final score are uppercase and the others
       lowercase. It first tries to find an optimal solution. If it exists it
       will be returned otherwise the function will look for an efficient
       solution. Again, if it exists it will be returned otherwise the function
       will return an adapted solution.'''
    
    # We need all the modules to be able to iterate over them in case of an
    # efficient solution is needed. Before using them we remove from the list
    # the initial module chosen by the fantaplayer (see below)
    all_modules = ['343','3412','3421','352','442','433',
                   '4312','4321','4231','4411','4222']
    
    # Initialize the new module, in case of efficient solution
    efficient_module = 0
    adapted_module = 0
    
    # Make a copy of the starting lineup
    original = copy.copy(lineup)
    
    # Initialize a list for the final solution. With an empty list it does not
    # work
    final = 0
    
    # As explained already, we first try to find an otimal solution
    if mode == 'FG':
        all_valid_candidates = valid_lineups(lineup, module, 'optimal', 'FG')
    else:
        all_valid_candidates = valid_lineups(lineup, module, 'optimal')
    
    for candidate in all_valid_candidates:
        
        if find_solution(candidate, module):
            final = copy.copy(candidate)
            break
    
    # In case an optimal solution does not exist we try to find an efficient
    # solution. To do that we try each lineup combination (FOLLOWING THE ORDER
    # IN THE BENCH) with each module (different from the input "module").
    if not final:
        if mode == 'FG':
            all_valid_candidates = valid_lineups(lineup, module, 'efficient', 'FG')
        else:
            all_valid_candidates = valid_lineups(lineup, module, 'efficient')
        modules_for_efficient_solution = copy.copy(all_modules)
        modules_for_efficient_solution.remove(module)
        for candidate in all_valid_candidates:
            for a_module in modules_for_efficient_solution:
                if find_solution(candidate, a_module):
                    efficient_module = a_module
                    final = copy.copy(candidate)
                    break
            if final:
                break
            
    final_malus = 4
    alternative_modules = []
    
    if not final:
        if mode == 'FG':
            all_valid_candidates = valid_lineups(lineup, module, 'efficient', 'FG')
        else:
            all_valid_candidates = valid_lineups(lineup, module, 'efficient')
        modules_for_adapted_solution = copy.copy(all_modules)
        for candidate in all_valid_candidates:
            for a_module in modules_for_adapted_solution:
                if find_adapted_solution(candidate, a_module):
                    n_malus = find_adapted_solution(candidate, a_module)
                    if n_malus < final_malus:
                        final_malus = n_malus
                        adapted_module = a_module
                        final = copy.copy(candidate)
                    if n_malus == final_malus:
                        alternative_modules.append(a_module)
            if final:
                break
            
    alternative_modules.remove(adapted_module)
            
    
    # This is for printing the result. We use the try method to handle the
    # TypeError case. In fact if an optimal solution is not found, the "if"
    # statement in the code below will try to subscript an integer ([1]) and
    # that will give an error
        
    # This is for printing the result. We initialize the final list. In this
    # list, only players with vote will be printed uppercase
    printed_lineup =[]
    
    for player in original:
        if player[1] in [data[1] for data in final]:
            printed_lineup.append(player)
        else:
            new_tuple = (player[0], player[1].title(), player[2])
            printed_lineup.append(new_tuple)
    
    
    separator = '- - - - - - - - - - - - - -'
    printed_lineup.insert(11, separator)
    
    if not efficient_module and not adapted_module:
        print('\n')
        print('Optimal solution found: module is %s' % module)
        print('\n')
    elif efficient_module:
        print('\n')
        print('Efficient solution found: module changed from %s to %s'
              % (module, efficient_module))
        print('\n')
    else:
        print('\n')
        print('Adapted solution found: module changed from %s to %s'
              % (module, adapted_module))
        print('\n')
        print('Equivalent modules were: %s.' % alternative_modules)
        print('\n')
    
    return printed_lineup







