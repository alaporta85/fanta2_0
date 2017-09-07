import os
import pickle
import copy

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

l = open('all_roles.pckl', 'rb')
all_roles = pickle.load(l)
l.close()

m = open('short_lineups.pckl', 'rb')
lineups = pickle.load(m)
m.close()

n = open('all_players_per_fantateam.pckl', 'rb')
fantaplayers = pickle.load(n)
n.close()

class Player(object):
    def __init__(self,name):
        self.name = name
        self.team = ''
        self.role = []
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
        self.matches_played = 0
        
        def calculate_avrg(self):            
            list_of_votes_FG = []
            list_of_votes_ST = []
            try:
                for day in players_database[self.name]:
                    self.matches_played += 1
                    if day[2] != 'n.e.':
                        list_of_votes_FG.append(day[2])
                    if day[3] != 'n.e.':
                        list_of_votes_ST.append(day[3])
            except KeyError:
                pass
            
            avrg_FG = sum(list_of_votes_FG)/self.matches_played
            avrg_ST = sum(list_of_votes_ST)/self.matches_played
            
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
            if self.name in all_players[self.team]:
                self.role = all_roles[self.name]
            
        update_player(self)
    
class Fantateam(object):
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.victories = 0
        self.draws = 0
        self.defeats = 0
        self.malus = 0
        self.players = []
        
        self.lineups = lineups[self.name]
        self.players = fantaplayers[self.name]
        
    def lineup(self, day):
        return self.lineups[day-1]
                
    def players(self):
        return self.players
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    