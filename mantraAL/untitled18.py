from schemes_allowed_changes import schemes, compatible_roles, malus_roles
import pickle
from itertools import combinations, permutations, product
import copy





def malus_roles_left(players_left,roles_left):
    
    '''This function is used to handle the case when for example there are
       still players to be deployed in players_left list but none of the
       roles of such players is in the roles_left list. So we check whether
       it is possible to deploy ALL of them with 1 or more malus.'''
    
    # To store the roles which are left to cover after modifing the
    # roles_left list according to the special modules
    
    # Permutations of the players still to be deployed. We do that because
    # we only want that combination of players in which ALL of them are
    # deployed
    players_perm = permutations(players_left,len(players_left))
        
    # Initialize the number of malus
    fin_malus = 4
    
    # For each permutation of players to be deployed        
    for perm in players_perm:
        
        temp_malus = 0
        
        # Make a copy of the roles to be covered so we can use it later to
        # delete roles that we are able to cover
        copy_of_adapted_roles = copy.copy(roles_left)
        
        # For each player in the permutation we make a copy of his roles
        # and for each of these roles we check if they are allowed to cover
        # (with a malus) any of the still uncovered positions in the field.
        # If yes we delete the role which is now covered from the list of
        # uncovered role, delete it also from the roles of the player and
        # finally break the loop to be able to go to the next player in the
        # permutation. If no we just break the loop
        for i in range(len(perm)):
            role_to_cover = roles_left[i]
            role_cand = perm[i][2]
            
            if role_to_cover in malus_roles[role_cand]:
                temp_malus += 1
                copy_of_adapted_roles.remove(role_to_cover)
            elif (role_to_cover not in malus_roles[role_cand]
            and role_to_cover in compatible_roles[role_cand]):
                copy_of_adapted_roles.remove(role_to_cover)
                

            
            if temp_malus < fin_malus and temp_malus != 0:
                fin_malus = temp_malus
                final = perm

        
    if fin_malus != 4:
        return perm,fin_malus
    else:
        return False