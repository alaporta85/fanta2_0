from schemes_allowed_changes import schemes, compatible_roles, malus_roles
import pickle
from itertools import combinations, permutations, product
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
    
    '''Returns the number of substitutions needed by the team.'''
    
    if mode == 'FG':
        field, bench = players_with_vote(list_of_tuples,mode='FG')
    else:
        field, bench = players_with_vote(list_of_tuples)
    
    # Set the number of substitutions needed        
    n_subst = 11 - len(field)
        
    return n_subst

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

def all_lineups_single_role(list_of_tuples):
    
    '''Returns a list of lineups and in each of them every player has only one
       role. If the input is for example [('MESSI',[T,A]), ('BELOTTI', [Pc])]
       than the output will be
       
          [(('MESSI',T), ('BELOTTI', Pc)), (('MESSI',A), ('BELOTTI', Pc))]
       
       The final list contains all the combinations of players' roles.'''
    
    players_single_role = []
    players_multiple_roles = []
    players_multiple_roles_modified = []
    
    final_cand = []
    
    # First separate players with 1 role and players with more roles
    for player in list_of_tuples:
        if len(player[2])==1:
            players_single_role.append((player[0],player[1],player[2][0]))
        else:
            players_multiple_roles.append(player)
    
    # Than for each multirole player create a list with as many tuples as the
    # number of roles of the players
    for multirole_player in players_multiple_roles:
        res = []
        for role in multirole_player[2]:
            res.append((multirole_player[0],multirole_player[1],role))
        players_multiple_roles_modified.append(res)
    
    # Create all the products between them    
    all_products = product(*players_multiple_roles_modified)
    
    # Combine each product with the single role players in order to form the
    # lineups and append the result in the final list
    for comb in all_products:
        cand = tuple(players_single_role) + comb
        final_cand.append(list(cand))
    
    return final_cand

def valid_lineups(field,bench,n_of_players_with_vote,n_subst):
    
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

    
def deploy_players(reduced_list,roles_of_module,solution):
        
    '''This function deploys the players in the lineup according to the module.
       It deploys the players, delete the role from the roles to be covered and
       delete the player from the players to be deployed. It returns the lists
       of the non-deployed players and non-covered roles.'''
        
    new_list = copy.copy(reduced_list)
    new_schemes = copy.copy(roles_of_module)
    
    for player in reduced_list:
        role = player[2]
        
        # First we try to delete the same role: if player is a 'M' than we
        # look for 'M' in the positions to be covered
        if role in new_schemes:
            new_list.remove(player)
            new_schemes.remove(role)
        
        # If there is no 'M' than we look for the compatible roles, which
        # are the roles where 'M' is contained ('M/C' in our case)
        elif (role in compatible_roles
              and set(compatible_roles[role]).intersection(new_schemes)):
            
            role_to_delete = set(compatible_roles[role])\
                                             .intersection(new_schemes)
            role_to_delete = list(role_to_delete)[0]
            new_list.remove(player)
            new_schemes.remove(role_to_delete)
            
        # If the role is not present in the positions to be covered and we 
        # are looking for an adpted solution we do NOT do anything, just
        # skip it (it will be used later for malus)
        elif role not in new_schemes and solution == 'adapted':
            pass
        
        # If we are looking for an optimal or efficient solution we return
        # False because it means it is not a valid candidate
        elif role not in new_schemes and solution == 'optimal':
            return False
                
    return new_list,new_schemes


def transf_wings(roles_left, module):
    
    '''Transforms the 'W' in the module (if any) according to the compatibility
       table of the roles. It returns the modified roles.'''
    
    special_modules = ['352', '442', '4411']
    adapted_roles = []
        
    # For modules in special_modules the rules for the substitutions of
    # the role 'W' are different. So here we take the roles inside the
    # input roles_left and directly append them in adapted roles if they
    # are != 'W'. In case there is a 'W' between the positions to be covered
    # we than modify it to be either 'W1' or 'W2' depending on the module
    # and append them
    for role in roles_left:
        new_role = copy.copy(role)
        if 'W' in role and module in special_modules:
            new_role = new_role.replace('W','W2')
            adapted_roles.append(new_role)
        elif 'W' in role and module not in special_modules:
            new_role = new_role.replace('W','W1')
            adapted_roles.append(new_role)
        else:
            adapted_roles.append(new_role)
            
    return adapted_roles

def order_by_role(list_of_tuples):
    
    '''Order the players according to their roles. We do this because it is
       much more efficient to deploy the players starting from positions which
       are more advanced in the field (Pc, A...). Random deployment causes
       errors.'''
    
    reference = ['Pc','A','T','W','C','M','E','Dc','Dd','Ds']
    
    final = []
    
    for role in reference:
        for player in list_of_tuples:
            if player[2] == role:
                final.append(player)
                
    return final

    
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

    
    def calculate(candidate,roles_of_module):
        
        '''This function applies the deploy_players function to look for the
           solution, if it exists. If all the players are deployed it returns
           True, otherwise False.'''
        
        # "try" method is used to handle the cases when the function
        # deploy_players returns False instead of the two lists (to_deploy_list
        # and roles_left). In that case we would have
        #
        #            to_deploy_list,roles_left = False
        #
        # which gives a TypeError. In our case the error means that the
        # candidate can not be a solution and it returns False.
        try:
            to_deploy_list,roles_left = deploy_players(candidate,
                                                       roles_of_module,
                                                       'optimal')
            
            # If all players are deployed the lineup represents an optimal
            # solution and we return it
            if len(to_deploy_list) == 0:
                return True
            else:
                return False
            
        except TypeError:
            return False
    
    
    # Order the players in the lineup according to their roles
    ordered_lineup = order_by_role(list_of_tuples)
    
    # Generate all the combinations of positions to be covered in the module.
    # Each combination will be made by n_of_players_with_vote (integer) players.
    # Up to 3 substitutions the value of n_of_players_with_vote is 10 so there
    # s only 1 possible combination because len(schemes[module]) == 10, 'Por'
    # is not included there. In case of 4 subst for example,
    # n_of_players_with_vote == 9 so there will be 10 possible combinations.
    # Each ordered (single role) lineup will be tested with each of these
    # combinations
    all_comb = combinations(schemes[module],n_of_players_with_vote)
    
    for comb in all_comb:
        
        # Change from tuple to list and check wings
        comb = transf_wings(list(comb), module)
        
        # If a solution is found we return True
        if calculate(ordered_lineup,comb):
            return True
    return False

    
def find_adapted_solution(list_of_tuples,module,n_of_players_with_vote):
    
    '''This function checks if an adapted solution is available, according to
       the module. By using all the functions defined inside it will return
       the number of malus assigned if an adapted solution exists and False if
       not.'''

    
    def malus_roles_left(players_left,roles_left):
        
        '''Checks whether it is possible to deploy all the players by assinging
           a certain number of malus.'''
        
        # Permutations of the players still to be deployed. We do that because
        # we only want that combination of players in which ALL of them are
        # deployed
        players_perm = permutations(players_left,len(players_left))
        
        # Initialize the number of malus (just a number high enough)
        fin_malus = 10
        
        # For each permutation of players to be deployed        
        for perm in players_perm:
            
            # Initialize two parameters: a counter and the number of malus for
            # this specific permutation. Counter is used to be sure all the
            # players in the permutation are checked
            count = 0
            temp_malus = 0
            
            # Make a copy of the roles to be covered so we can use it later to
            # delete roles that we are able to cover
            copy_of_adapted_roles = copy.copy(roles_left)
            
            # For each element in the permutation we select the corresponding
            # role and try to cover it
            for i in range(len(perm)):
                role_to_cover = roles_left[i]
                role_cand = perm[i][2]
                
                # If it is possible to cover it with a malus we increase the
                # number of malus and the counter and then remove the role from
                # the list of the roles still uncovered
                if role_to_cover in malus_roles[role_cand]:
                    temp_malus += 1
                    count += 1
                    copy_of_adapted_roles.remove(role_to_cover)
                    
                # If it is possible to cover it with no malus we just increase
                # the counter and delete the role
                elif (role_to_cover not in malus_roles[role_cand]
                and role_to_cover in compatible_roles[role_cand]):
                    count += 1
                    copy_of_adapted_roles.remove(role_to_cover)
                    
                # Else we interrupt checking this permutation and go to the
                # one
                else:
                    break
            
            # If we checked ALL the elements in the permutation and the number
            # of malus is lower than the previous value we store it
            if count == len(perm) and temp_malus < fin_malus:
                fin_malus = temp_malus
        
        # If this value is different from the default one it means we found a
        # solution and we return it
        if fin_malus != 10:
            return fin_malus
        else:
            return False
        
    
    def calculate(candidate,roles_of_module):
        
        '''This function applies the deploy_players function to look for the
           solution, if it exists. If all the players are deployed it returns
           True, otherwise False.'''

        # See find_solution for explanation on the try method
        try:
            to_deploy_list,roles_left = deploy_players(candidate,
                                                       roles_of_module,
                                                       'adapted')
            
            # If the roles to deploy can be covered with a malus we return the
            # number of malus assigned
                
            if malus_roles_left(to_deploy_list,roles_left):
                return malus_roles_left(to_deploy_list,roles_left)
            else:
                return False
            
        except TypeError:
            return False
    
    ordered_lineup = order_by_role(list_of_tuples)
    
    all_comb = list(combinations(schemes[module],n_of_players_with_vote))
    
    for comb in all_comb:
        
        # Change from tuple to list and check wings
        comb = transf_wings(list(comb), module)
        
        # If a solution is found we return the number of malus
        if calculate(ordered_lineup,comb):
            return calculate(ordered_lineup,comb)
    
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
        
        # For each candidate
        for candidate in all_lineups:
            
            # We create the list where each player in the combination has only
            # 1 role
            candidates_single_role = all_lineups_single_role(candidate)
            
            # And test each of these combinations
            for new_cand in candidates_single_role:
                
                # If we find a solution we store the result
                if find_solution(new_cand,module,n_of_players_with_vote):
                    final = candidate
                    break
                
            # And stop the iteration over the other condidates
            if final:
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
            candidates_single_role = all_lineups_single_role(candidate)
            for new_cand in candidates_single_role:
                
                # And over all the modules
                for a_module in modules_for_efficient_solution:
                    
                    # If we find a solution we store the result
                    if find_solution(new_cand,a_module,n_of_players_with_vote):
                        final = candidate
                        efficient_module = a_module
                        break
                
                # Stop the iteration over the other permutations
                if final:
                    break
                
            # Stop the iteration over the other candidates
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
            candidates_single_role = all_lineups_single_role(candidate)
            for new_cand in candidates_single_role:

                # And over all the modules
                for a_module in modules_for_adapted_solution:
                    
                    # If a solution for this candidate with this module exists,
                    # we store the number of malus for this specific case
                    if find_adapted_solution(new_cand, a_module,
                                             n_of_players_with_vote):
                        
                        n_malus = find_adapted_solution(new_cand, a_module,
                                                        n_of_players_with_vote)
                        
                        # If it is <= than the last one (or less than 4 in
                        # the first case) we overwrite its value, the module
                        # and the lineup. In this way we check all the lineups
                        # and at the end we will have only the one with the
                        # lower number of malus
                        if n_malus <= malus:
                            malus = n_malus
                            adapted_module = a_module
                            final = candidate
    
                            alternative_modules.append((a_module,n_malus))

            # Stop the iteration over the other candidates
            if final:
                break
        
        # Delete from the alternative module
        copy_of_modules = copy.copy(alternative_modules)
        for x in alternative_modules:
            if x[0] == adapted_module or x[1]!= malus:
                copy_of_modules.remove(x)
                
        alternative_modules = list(set([x[0] for x in copy_of_modules]))
            
    
    def look_for_solution(module,n_of_players_with_vote,n_subst):
        
        '''It sequentially applies the three functions to look for the right
           solution.'''

        try_optimal_solution(module,n_of_players_with_vote,n_subst)
        if not final:
            try_efficient_solution(module,n_of_players_with_vote,n_subst)
        if not final:
            try_adapted_solution(module,n_of_players_with_vote,n_subst)
            
    
    def solve_gkeeper():
        
        '''Goal keeper substitution has to be the first thing to solve, if
           needed. Here we modify field, bench and n_subst depending on whether
           the gkeepers has vote or not.'''
        
        nonlocal field
        nonlocal bench
        nonlocal n_subst

        # If the goal keeper n the field received a vote we delete all the
        # remaining goal keepers from the bench
        if find_gkeeper(field):
            bench = delete_gkeeper(bench)
        
        # If the gkeeper in the field has no vote but the there is at least one
        # gkeeper in the bench with vote we make the substitution and delete
        # all the remaining gkeepers from the lineup, if there is any. We
        # finally decrease the n_subst
        elif not find_gkeeper(field) and find_gkeeper(bench):
            gkeeper = find_gkeeper(bench)
            field.insert(0,gkeeper)
            bench = delete_gkeeper(bench)
            n_subst -= 1
        
        # If there is no gkeeper with vote neither in the field nor in the
        # bench than we just decrease the n_subst     
        elif not find_gkeeper(field) and not find_gkeeper(bench):
            n_subst -= 1
            
            
    def calculation(a_number):
        
        '''This is the function that is recursively applied to find the correct
           lineup. The input 'a_number' is an integer which represents the
           number of players (gkeeper excluded) who will partecipate in the
           lineup calculation. In case the algorithm does not find any solution
           after the first iteration it repeats the process considering 1
           substitution and 1 player less.'''
        
        nonlocal field
        nonlocal bench
        nonlocal module
        nonlocal n_subst
        nonlocal all_lineups

        all_lineups = valid_lineups(field,bench,module,n_subst)
        look_for_solution(module,a_number,n_subst)
                
        if not final:
            n_subst -= 1
            return calculation(a_number-1)

    
    # Select the players with vote and store the number of substitutions needed
    if mode == 'FG':
        field,bench = players_with_vote(lineup, 'FG')
        n_subst = n_of_subst(lineup, mode='FG')
    else:
        field,bench = players_with_vote(lineup)
        n_subst = n_of_subst(lineup)
        
    
    # Make a copy of the starting lineup. We will NOT modify this copy
    original = copy.copy(lineup)
    
    # Initialize all the parameters. We chose 10 for malus just because it is
    # a number high enough and we look for the solution with the lower number
    # of malus
    final = 0                          # The final lineup
    efficient_module = 0               # Valid module in case of eff solution
    adapted_module = 0                 # Valid module in case of adp solution
    malus = 10                         # Number of malus assigned
    alternative_modules = []           # Modules equally valid in adp solution
    magic_number = 10                  # N. of players considered in the lineup
    all_lineups = 0                    # All candidates
    
    # We need all the modules to be able to iterate over them in case of an
    # efficient or adapted solution is needed
    all_modules = ['343','3412','3421','352','442','433',
                   '4312','4321','4231','4411','4222']
    
    # Handle the goal keeper issue
    if n_subst <= 3:
        solve_gkeeper()
        if find_gkeeper(field):
            gkeeper = field[0]
            field.remove(gkeeper)
        else:
            gkeeper = 0
                                
        calculation(magic_number)
        
    else:
        magic_number = 13 - n_subst
        n_subst = 3
        
        solve_gkeeper()
        if find_gkeeper(field):
            gkeeper = field[0]
            field.remove(gkeeper)
        else:
            gkeeper = 0
                    
        calculation(magic_number)
    
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







