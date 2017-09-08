from schemes_allowed_changes import schemes, compatible_roles, allowed_changes
import pickle
import random
from itertools import combinations
import copy

f=open('esempi_panchina.pckl', 'rb')
lineups1 = pickle.load(f)
lineups2 = pickle.load(f)
lineups3 = pickle.load(f)
f.close()

f=open('esempi_voti.pckl', 'rb')
players_database = pickle.load(f)
f.close()

l = open('/Users/andrea/Desktop/fanta2_0/all_roles.pckl', 'rb')
all_roles = pickle.load(l)
l.close()

def take_vote_from_database(player, day, mode='ST'):
    
    '''This function returns the vote from the database for the specified
       player in that specific day. In case player does NOT have a vote in that
       day, it manages the KeyError and returns n.e. (not evaluated).'''
       
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
       and the number of substitutions needed by the fantateam. In case more
       than three substitutions are needed, the value for n_subst will be three
       anyway.'''
       
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


def valid_lineups(list_of_tuples, module):
    
    '''This function uses all the filters defined above to return a list
       containing ALL the valid combinations of the original lineup given by
       the fantaplayer (list_of_tuples). "Valid" means that all of them are
       lineups that could be perfectly working according to the rules of the
       game. Whether they will work or not it depends on the module chosen by
       the fantaplayer.'''
    
    field,bench,n_subst = players_with_vote(list_of_tuples, mode='ST')
    
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
    all_valid_lineups = []            # All valid candidates
    
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
                        
# =============================================================================
#                         clean_def = [x[1] for x in defense]
#                         clean_mid = [y[1] for y in midfield]
#                         clean_att = [z[1] for z in attack]
# =============================================================================
                        # If there are no repeated players we create the new
                        # lineup and it will be one of the valid candidates
                        if all_players_are_different(defense,
                                                     midfield,
                                                     attack):
                            
                            new_lineup = [gkeeper] + list(defense)\
                                       + list(midfield) + list(attack)
                            
                            all_valid_lineups.append(new_lineup)                            
            
    return all_valid_lineups
    
    
def optimal_solution(list_of_tuples, module):
    
    '''This function checks if an optimal solution is available.
       A solution is called optimal when all the players thah contributes to
       the final score (including the ones entered from the bench) are arranged
       in a way that implies NO change in module and NO malus. It returns the
       final lineup that will be used to calculate the final score in case it
       exists. Otherwise it returns False. To check if an optimal solution
       exists we RECURSIVELY apply two functions (reduce_roles and
       deploy_players) inside a third one (calculate).'''
    
    def reduce_roles(list_of_tuples, roles_of_module):
        
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
            for role in old_roles:
                if not role in needed_roles:
                    new_roles.remove(role)
            
            reduced_list.append((player[0], player[1], new_roles))
        
        return reduced_list
    
    def deploy_players(reduced_list, roles_of_module):
        
        '''This function deploys the players in the lineup according to the
           module. It deploys only the players who has one role, delete the
           role from the roles to be covered and delete the player from the
           players to be deployed. It returns the lists of the non-deployed
           players and non-covered roles. It return False if the role to deploy
           is not in the list of the still-to-be-covered roles (it can happen
           even after the application of reduce_roles because it is a recursive
           process.'''
        
        new_list = copy.copy(reduced_list)
        new_schemes = copy.copy(roles_of_module)
        
        for player in reduced_list:
            role = player[2]
            if len(role)==1:
                role_to_delete = set(compatible_roles[role[0]])\
                                                 .intersection(roles_of_module)
                role_to_delete = list(role_to_delete)[0]
                new_list.remove(player)
                try:
                    new_schemes.remove(role_to_delete)
                except ValueError:
                    return False
                    
        return new_list,new_schemes
    
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
        
        try:
            reduced_list = reduce_roles(candidate, roles_of_module)
            to_deploy_list,roles_left = deploy_players(reduced_list, roles_of_module)
            
            # If all players are deployed the lineup represents an optimal
            # solution and we return it
            if len(to_deploy_list) == 0:
                return O_solution
            
            # If the function deploy_players is NOT able to deploy any player
            # but the roles to deploy are the same as the roles left, the
            # lineup represents an optimal solution and we return it
            elif (len(to_deploy_list) == len(candidate)
            and same_roles_left(to_deploy_list, roles_left)):
                return O_solution
            
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
    
    O_solution = [1]

    if calculate(list_of_tuples, schemes[module]):
        O_solution = copy.copy(list_of_tuples)
        return O_solution
    else:
        return False

    
def MANTRA_simulation(lineup, module):
    
    # Make a copy of the starting lineup
    original = copy.copy(lineup)
    
    # Initialize a list for the optimal solution, if founded. With an empty
    # list it does not work
    modified = [1]
    
    all_valid_candidates = valid_lineups(lineup, module)
    
    for candidate in all_valid_candidates:
        
        if optimal_solution(candidate, module):
            modified = copy.copy(candidate)
            break
    
    # This is for printing the result. We use the try method to handle the
    # TypeError case. In fact if an optimal solution is not found, the "if"
    # statement in the code below will try to subscript an integer ([1]) and
    # that will give an error
    try:
        
        # Initialize the final list. In this list, only players with vote will be
        # printed uppercase
        printed_lineup =[]
        
        for player in original:
            if player[1] in [data[1] for data in modified]:
                printed_lineup.append(player)
            else:
                new_tuple = (player[0], player[1].title(), player[2])
                printed_lineup.append(new_tuple)
                
        return printed_lineup
    
    except TypeError:
        return False







