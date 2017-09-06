# Spider to scrape:
#
#   1.  The players of each Serie A team. They will be stored in a dict and
#       saved inside a .pckl file. The keys of the dict are the names of the
#       teams in Serie A (Atalanta, Benevento etc etc) while the values are
#       lists containing all the players of that team.
#
#   2.  The roles of each player in Serie A. They will be stored in a dict and
#       saved inside a .pckl file. The keys of the dict are the names of the
#       players while the values are lists containing the mantra roles.


import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

# These two conditions to initialize the files that will be used later
if not os.path.isfile('all_players_per_team.pckl'):
    adict = {}
    f = open('all_players_per_team.pckl', 'wb')
    pickle.dump(adict, f)
    f.close()
    
if not os.path.isfile('all_roles.pckl'):
    adict = {}
    f = open('all_roles.pckl', 'wb')
    pickle.dump(adict, f)
    f.close()

# The "try" method is used to avoid errors while launching the spider
# 'serieA_fantateams_schedule' to create those .pckl files.
try:
    class Players_Roles(scrapy.Spider):
        
        name = 'all_players_and_roles'
    
        f = open('serieA_teams.pckl', 'rb')
        serieA_teams = pickle.load(f)
        f.close()
        
        f = open('all_players_per_team.pckl', 'wb')
        players_dict = {team:[] for team in serieA_teams}
        pickle.dump(players_dict, f)
        f.close()
        
        start_urls = ['https://www.fantagazzetta.com/squadre/%s#rosa'
                      % team for team in serieA_teams]
    
        
        def start_requests(self):
            for url in self.start_urls:
                yield SplashRequest(url, self.parse,
                                    endpoint='render.html',
                                    args={'wait': 0.5})
    
        def parse(self, response):
                        
            # Name of Serie A team
            team_name = response.xpath('//h1/text()').extract_first()
            
            # Table containing all the players of that team
            table = response.xpath('//table[contains(@id,"DataTables_Table_0")]'+
                                   '/tbody/tr')
            # For each player
            for player in table:
                
                # Extract the name                        
                name = player.xpath('.//a/text()').extract_first()
                
                # Exctract the role
                role = player.xpath('.//span').xpath('.//text()').extract()[1:]
                
                # Store the name in the dict
                f = open('all_players_per_team.pckl', 'rb')
                players_dict = pickle.load(f)
                f.close()
                players_dict[team_name].append(name)
                f = open('all_players_per_team.pckl', 'wb')
                pickle.dump(players_dict, f)
                f.close()
                
                # Store the role in the dict
                f = open('all_roles.pckl', 'rb')
                roles_dict = pickle.load(f)
                f.close()
                roles_dict[name] = role
                f = open('all_roles.pckl', 'wb')
                pickle.dump(roles_dict, f)
                f.close()
                
except FileNotFoundError:
    pass
            
            
            
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        
                
    
    