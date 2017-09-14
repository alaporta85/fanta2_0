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
lineups8 = pickle.load(f)
lineups9 = pickle.load(f)
lineups10 = pickle.load(f)

f.close()

f=open('esempi_voti.pckl', 'rb')
players_database = pickle.load(f)
f.close()

l = open('/Users/andrea/Desktop/fanta2_0/all_roles.pckl', 'rb')
all_roles = pickle.load(l)
l.close()


def take_vote_from_database(player,day,mode='ST'):
    
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


def players_with_vote(list_of_tuples,mode='ST'):
    
    '''This function returns two lists (field and bench) which represent the
       players who received vote in the field and in the bench, respectively.'''
       
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
    
    return field, bench

def n_of_subst(list_of_tuples,mode='ST'):
    
    '''Returns the number of substitutions needed by the team. If this number
       will be > 3, the allowed substitutions will be 3 anyway.'''
    
    if mode == 'FG':
        field, bench = players_with_vote(list_of_tuples,mode='FG')
    else:
        field, bench = players_with_vote(list_of_tuples)
    
    # Set the number of substitutions needed        
    n_subst = 11 - len(field)
        
    return n_subst

def n_players_role(list_of_tuples,list_of_roles):
    
    '''This function returns the number of players whose list of roles contain
       at least one role in common with the list_of_roles given as input.'''
       
    count = 0
    for i in list_of_tuples:
        if set(i[2]).intersection(list_of_roles):
            count += 1
            
    return count

def find_gkeeper(alist):
    
    '''Checks whether any goal keeper is present in a given list. It returns
       the name of the first one in case there is any and False otherwise.'''
       
    gkeepers = []
    for player in alist:
        if player[2] == ['Por']:
            gkeepers.append(player)
    
    if gkeepers:
        return gkeepers[0]
    else:
        return False

def delete_gkeeper(alist):
    
    '''Returns alist without any goal keeper.'''
    
    res = []
    for player in alist:
        if player[2] != ['Por']:
            res.append(player)
            
    return res


def valid_lineups(field,bench,module,n_subst):
    
    '''This function returns a list containing ALL the possible lineups. To
       create them we first create all the combinations of players from the
       bench taking into account the n_subst allowed. After this, for each
       combination created we create the lineup by putting together the field
       + the combination.'''
            
    # Generate all the combination of the players in the bench. Each
    # combination will be made of a number of players equal to the number of
    # allowed substitutions
    players_from_bench = list(combinations(bench,n_subst))
    all_lineups = []                  # All candidates
    
    # Combine players in the field with each combination of players from the
    # bench. The resulting lineup will be a candidate to be checked
    for block in players_from_bench:
        candidate = copy.copy(field)
        for player in block:
            candidate.append(player)
        all_lineups.append(candidate)
    
    return all_lineups
    
    
def reduce_roles(list_of_tuples,roles_of_module,solution):
        
    '''This function eliminates from the list of roles of each player all the
       roles that are not allowed in the chosen module. For example, if the
       list of roles of a player is ['Dc', 'Dd'] and the module is 343 (or any
       with 3 defenders) this function will return ['Dc'] as list of roles of
       the player because 'Dd' is not allowed in 343.'''
                
    # Create the list of roles needed in the module. Roles like 'M/C' will
    # be split as 'M' and 'C'
    needed_roles = set([x for y in roles_of_module for x in y.split('/')])
        
    reduced_list = []
        
    for player in list_of_tuples:
        old_roles = player[2]
        new_roles = copy.copy(old_roles)
        
        # If the player has no valid roles for the module and we are looking
        # for an adapted soluton we do not do anything (instead of deleting all
        # of them) because those players will be the ones that will be deployed
        # at the end and will receive a malus
        if (set(old_roles).isdisjoint(needed_roles)
        and solution == 'adapted'):
                pass
        
        # If we are looking for an optimal or efficient solution we return
        # False because it means it is not a valid candidate
        elif (set(old_roles).isdisjoint(needed_roles)
        and solution == 'optimal'):
                return False
            
        # Otherwise we delete only the ones which are not allowed. The
        # condition to delete it is that it does NOT have to be the only role
        # of the player
        else:
            for role in old_roles:
                if role not in needed_roles and len(new_roles) > 1:
                    new_roles.remove(role)
            
        
        reduced_list.append((player[0], player[1], new_roles))
    
    return reduced_list
    
def deploy_players(reduced_list,roles_of_module,solution):
        
    '''This function deploys the players in the lineup according to the module.
       It deploys only the players who have one role, delete the role from the
       roles to be covered and delete the player from the players to be
       deployed. It returns the lists of the non-deployed players and
       non-covered roles.'''
        
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
        and set(compatible_roles[role[0]]).intersection(new_schemes)):
            
            role_to_delete = set(compatible_roles[role[0]])\
                                             .intersection(new_schemes)
            role_to_delete = list(role_to_delete)[0]
            new_list.remove(player)
            new_schemes.remove(role_to_delete)
            
        # If the role is not present in the positions to be covered and we 
        # are looking for an adpted solution we do NOT do anything, just
        # skip it (it will be used later for malus)
        elif (len(role)==1 and role[0] not in new_schemes
        and solution == 'adapted'):
            pass
        
        # If we are looking for an optimal or efficient solution we return
        # False because it means it is not a valid candidate
        elif (len(role)==1 and role[0] not in new_schemes
        and solution == 'optimal'):
            return False
                
    return new_list,new_schemes

def transf_comb(atuple):
    res = []
    for i in atuple:
        res.append(i)
    
    return res
    
    
def find_solution(list_of_tuples,module,n_of_players_with_vote):
    
    '''This function checks if a solution is available, according to the module.
       It is used in the cases of optimal and efficient solution. For the
       optimal solution it is applied only to the module chosen by the
       fantaplayer while for the efficient solution it is applied to all the
       modules following the order of the players in the bench.
       A solution is found when all the players thah contributes to
       the final score (including the ones entered from the bench) can be
       arranged in a way consistent with possible roles defined by the module
       with NO malus.
       The input value 'n_of_players_with_vote' is used to calculate the
       combinations of the roles in the module. This is used when more than 3
       substitutions are needed and the algorithm tries to find a solution
       for each candidate with all the possible combinations of roles.
       It returns True in case a solution exists. Otherwise False.'''

    def same_roles_left(deployed_list,new_schemes):
        
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
    
    def calculate(candidate,roles_of_module):
        
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
            reduced_list = reduce_roles(candidate,roles_of_module,'optimal')
            to_deploy_list,roles_left = deploy_players(reduced_list,
                                                       roles_of_module,
                                                       'optimal')
            
            # If all players are deployed the lineup represents an optimal
            # solution and we return it
            if len(to_deploy_list) == 0:
                return True
            
            # If the function deploy_players is NOT able to deploy any player
            # but the roles to deploy are the same as the roles left, the
            # lineup represents an optimal solution and we return it
            elif (len(to_deploy_list) == len(candidate)
            and same_roles_left(to_deploy_list,roles_left)):
                return True
            
            # If the function deploy_players is NOT able to deploy any player
            # and the roles to deploy are different from the roles left, the
            # lineup is NOT an optimal solution and we return False
            elif (len(to_deploy_list) == len(candidate)
            and not same_roles_left(to_deploy_list,roles_left)):
                return False
            
            # Otherwise we repeat the process with the new lists as input
            else:
                return calculate(to_deploy_list,roles_left)
            
        except TypeError:
            return False
    
    # Generate all the combinations. Each combination will be made by
    # n_of_players_with_vote (integer) players. Up to 3 substitutions the value
    # of n_of_players_with_vote is 10 so there is only 1 possible combination
    # because len(schemes[module]) == 10, 'Por' is not included there. In case
    # of 4 subst for example, n_of_players_with_vote == 9 so there will be 10
    # possible combinations. Each group of players coming from the bench will
    # be tested with each of these combinations always following the order of
    # the bench.
    all_comb = combinations(schemes[module],n_of_players_with_vote)
    
    for comb in all_comb:
        # Change from tuple to list
        comb = transf_comb(comb)
        
        # If a solution is found we return True
        if calculate(list_of_tuples,comb):
            return True
    return False

    
def find_adapted_solution(list_of_tuples,module,n_of_players_with_vote):
    
    '''This function checks if an adapted solution is available, according to
       the module. By using all the functions defined inside it will return
       True if an adapted solution exists and False if not.'''
       
    
    def any_in_malus_role(roles_to_check,substitute):
        
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
    
    def malus_roles_left(players_left,roles_left):
        
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
        players_perm = permutations(players_left,len(players_left))
        
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
        
        # Initialize the number of malus
        n_malus = 0
        
        # For each permutation of players to be deployed        
        for perm in players_perm:
            
            # Number of malus is the len of the permutation. At this stage, in
            # fact, we get only in the case when the players left have to be
            # deployed with malus. This means that the number of players in
            # each permutation represents the number of malus in case that
            # specific permutation will be valid
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
            # the positions in the field we return the number of malus assigned,
            # otherwise we check the next permutation of players
            if len(copy_of_adapted_roles) == 0:
                return n_malus
        
        # If after all the permutaions we still have positions in the field
        # still to be covered, this means that it is not possible to find an
        # adapted solution for the original lineup and we return False
        if len(copy_of_adapted_roles) > 0:
            return False
        
    
    def calculate(candidate,roles_of_module):
        
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
            reduced_list = reduce_roles(candidate,roles_of_module,'adapted')
            to_deploy_list,roles_left = deploy_players(reduced_list,
                                                       roles_of_module,
                                                       'adapted')

            # If the function deploy_players is NOT able to deploy any player
            # but the roles to deploy can be covered with a malus we return the
            # number of malus assigned
            if (len(to_deploy_list) == len(candidate)
            and malus_roles_left(to_deploy_list,roles_left)):
                return malus_roles_left(to_deploy_list,roles_left)
            
            # If the function deploy_players is NOT able to deploy any player
            # and, even with malus applyied, it is NOT possible to cover the
            # roles left we return False
            elif (len(to_deploy_list) == len(candidate)
            and not malus_roles_left(to_deploy_list,roles_left)):
                return False
            
            # Otherwise we repeat the process
            else:
                return calculate(to_deploy_list,roles_left)
            
        except TypeError:
            return False
        
    all_comb = combinations(schemes[module],n_of_players_with_vote)
    
    for comb in all_comb:
        comb = transf_comb(comb)
        # If a solution is found we return the number of malus
        if calculate(list_of_tuples,comb):
            return calculate(list_of_tuples,comb)
    
    return False
    
    
def MANTRA_simulation(lineup,module,mode='ST'):
    
    '''This function returns the lineup chosen by the fantaplayer where all the
       players who contribute to the final score are uppercase and the others
       lowercase. It first tries to find an optimal solution. If it exists it
       will be returned otherwise the function will look for an efficient
       solution. Again, if it exists it will be returned otherwise the function
       will return an adapted solution.'''
       
    def try_optimal_solution(module,n_of_players_with_vote,n_subst):
        
        '''If an optimal solution exists this function assign it to the
           variable "final" which is defined inside MANTRA_simulation but not
           globally. That's why we refers to it later by using "nonlocal".'''
        
        nonlocal all_lineups   
        nonlocal final
        
        for candidate in all_lineups:
            if find_solution(candidate,module,n_of_players_with_vote):
                final = candidate
                break

            
    def try_efficient_solution(module,n_of_players_with_vote,n_subst):
        
        '''If an optimal solution is not found we look for an efficient one.
           In case an efficient solution exists we store the lineup and the
           module.'''
            
        modules_for_efficient_solution = copy.copy(all_modules)
        modules_for_efficient_solution.remove(module)
        
        nonlocal all_lineups
        nonlocal final
        nonlocal efficient_module
        
        # Iterate over all the candidates
        for candidate in all_lineups:
            
            # And over all the modules
            for a_module in modules_for_efficient_solution:
                
                if find_solution(candidate,a_module,n_of_players_with_vote):
                    final = candidate
                    efficient_module = a_module
                    break
                
            # This is to stop the iteration over the candidates in case we have
            # already found the solution
            if final:
                break
                
    def try_adapted_solution(module,n_of_players_with_vote,n_subst):
        
        '''If an efficient solution is not found we look for an adapted one.
           In case it exists we store the lineup, the module, the number of
           malus assigned and the other modules that are equally valid.'''
            
        modules_for_adapted_solution = copy.copy(all_modules)
        
        nonlocal all_lineups
        nonlocal final
        nonlocal adapted_module
        nonlocal malus
        nonlocal alternative_modules
        
        # As for the efficient case we iterate over all the candidates
        for candidate in all_lineups:
            
            # And over all the modules
            for a_module in modules_for_adapted_solution:
                
                # If a solution for this candidate with this module exists, we
                # store the number of malus for this specific case
                if find_adapted_solution(candidate, a_module,
                                         n_of_players_with_vote):
                    
                    n_malus = find_adapted_solution(candidate, a_module,
                                                    n_of_players_with_vote)
                    
                    # If it is lower than the last one (or less than 4 in the
                    # first case) we overwrite its value, the module and the
                    # lineup. In this way we check all the lineups and at the
                    # end we will have only the one with the lower number of
                    # malus
                    if n_malus < malus:
                        malus = n_malus
                        adapted_module = a_module
                        final = candidate
                        
                    # Store all the module which are also valid solutions
                    if n_malus == malus:
                        alternative_modules.append(a_module)
                        
            # Stop the iteration over the candidates if we have a final lineup
            if final:
                break
        
        if alternative_modules:
            # Remove the actual module chosen for the change in order to print only
            # the alternatives
            alternative_modules.remove(adapted_module)
            
    def look_for_solution(module,n_of_players_with_vote,n_subst):
        
        '''It sequentially applies the three functions to look for the right
           solution.'''

        try_optimal_solution(module,n_of_players_with_vote,n_subst)
        if not final:
            try_efficient_solution(module,n_of_players_with_vote,n_subst)
        if not final:
            try_adapted_solution(module,n_of_players_with_vote,n_subst)
            
    def solve_gkeeper():
        
        nonlocal field
        nonlocal bench
        nonlocal n_subst

        # Now we start considering the goal keeper issue. If the goal keeper
        # in the field received a vote we delete all the remaining goal keepers
        # from the bench
        if find_gkeeper(field):
            bench = delete_gkeeper(bench)
        
        # If the gkeeper in the field has no vote but the there is at least one
        # gkeeper in the bench with vote we make the substitution and delete
        # all the remaining gkeepers from the lineup, if there is any. We
        # finally decrease the n_subst
        elif not find_gkeeper(field) and find_gkeeper(bench):
            gkeeper = find_gkeeper(bench)
            bench = delete_gkeeper(bench)
            field.insert(0,gkeeper)
            n_subst -= 1
        
        # If there is no gkeeper with vote neither in the field nor in the
        # bench than we just decrease the n_subst     
        elif not find_gkeeper(field) and not find_gkeeper(bench):
            n_subst -= 1
            
            
    def aaa(a_number):
        
        nonlocal field
        nonlocal bench
        nonlocal module
        nonlocal n_subst
        nonlocal all_lineups
        
        
        # If n_subst is below the allowed limit
        if n_subst < 3:
            
            # Set the variable n_of_players_with_vote to be 10, like normal
            n_of_players_with_vote = a_number
            print(n_of_players_with_vote)
            print(n_subst)

            all_lineups = valid_lineups(field,bench,module,n_subst)
            look_for_solution(module,n_of_players_with_vote,n_subst)
    
        # If more than 3 subst are needed we are in a special case.
        else:
            # We first set the value for the combinations of players
            n_of_players_with_vote = a_number + 3 - n_subst
            
            # Then n_subst can not be more than 3
            n_subst = 3
            
            all_lineups = valid_lineups(field,bench,module,n_subst)
            look_for_solution(module,n_of_players_with_vote,n_subst)
                
        if not final:
            print('stocazzo')
            n_subst -= 1
            return aaa(a_number-1)

    
    # Select the players with vote and store the number of substitutions needed
    if mode == 'FG':
        field,bench = players_with_vote(lineup, 'FG')
        n_subst = n_of_subst(lineup, mode='FG')
    else:
        field,bench = players_with_vote(lineup)
        n_subst = n_of_subst(lineup)
    
    # Make a copy of the starting lineup. We will NOT modify this copy
    original = copy.copy(lineup)
    
    # Initialize all the parameters. Malus is initialized to be 4 because we
    # want to find the solution with the lower number of malus and 3 is the
    # maximum allowed
    
    final = 0                           # The final lineup
    efficient_module = 0                # Valid module in case of eff solution
    adapted_module = 0                  # Valid module in case of adp solution
    malus = 4                           # Number of malus assigned
    alternative_modules = []            # Modules equally valid in adp solution
    magic_number = 10
    all_lineups = 0
    
    # We need all the modules to be able to iterate over them in case of an
    # efficient solution is needed.
    all_modules = ['343','3412','3421','352','442','433',
                   '4312','4321','4231','4411','4222']
    
    # Handle the goal keeper issue
    solve_gkeeper()
    if find_gkeeper(field):
        gkeeper = field[0]
        field.remove(gkeeper)
    else:
        gkeeper = 0
                
    aaa(magic_number)
    
    if gkeeper:
        final.insert(0,gkeeper)
        
        
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
        print('Adapted solution found: module changed from %s to %s.'
              % (module, adapted_module))
        print('Players with malus: %d' % malus)
        print('\n')
        print('Equivalent modules were: %s.' % alternative_modules)
        print('\n')
    
    return printed_lineup







