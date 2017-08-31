from schemes_allowed_changes import schemes, allowed_changes
import pickle

f=open('esempi_panchina.pckl', 'rb')
lineups = pickle.load(f)
f.close()

f=open('esempi_voti.pckl', 'rb')
player_database = pickle.load(f)
f.close()

def optimal_solution(list_of_tuples, integer):
    