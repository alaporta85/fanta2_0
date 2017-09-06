import os
import pickle

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

f = open('all_players_per_team.pckl', 'rb')
all_players = pickle.load(f)
f.close()

g = open('SerieA_players_database.pckl', 'rb')
players_database = pickle.load(g)
g.close()

h = open('schedule.pckl', 'rb')
schedule = pickle.load(h)
h.close()

class Player(object):
    def __init__(self,name):
        self.name = name
        self.team = ''
        self.FG_avrg = 0
        self.ST_avrg = 0
        self.YC = 0
        self.RC = 0
        self.Gs = 0
        self.Gp = 0
        self.Gt = 0
        self.Ps = 0
        self.Pf = 0
        self.Og = 0
        self.As = 0
        self.Asf = 0
        
        def calculate_avrg(self):            
            list_of_votes_FG = []
            list_of_votes_ST = []
            matches_played = 0
            try:
                for day in players_database[self.name]:
                    matches_played += 1
                    if day[2] != 'n.e.':
                        list_of_votes_FG.append(day[2])
                    if day[3] != 'n.e.':
                        list_of_votes_ST.append(day[3])
            except KeyError:
                pass
            
            avrg_FG = sum(list_of_votes_FG)/matches_played
            avrg_ST = sum(list_of_votes_ST)/matches_played
            
            self.FG_avrg = round(avrg_FG,2)
            self.ST_avrg = round(avrg_ST,2)
                
        def update_player(self):
            for day in players_database[self.name]:
                self.team = day[1]
                self.YC += day[4]
                self.RC += day[5]
                self.Gs += day[6]
                self.Gp += day[7]
                self.Gt += day[8]
                self.Ps += day[9]
                self.Pf += day[10]
                self.Og += day[11]
                self.As += day[12]
                self.Asf += day[13]
            calculate_avrg(self)
            
        update_player(self)
        
class 
    
    
    
    
    
    
    
    
    