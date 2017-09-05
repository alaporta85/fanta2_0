import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

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
                        
        fin_data = []
                
        team_name = response.xpath('//h1/text()').extract_first()
        
        table = response.xpath('//table[contains(@id,"DataTables_Table_0")]'+
                               '/tbody/tr')
        
        for player in table:
                                    
            name = player.xpath('.//a/text()').extract_first()
            
            role = player.xpath('.//span').xpath('.//text()').extract()[1:]
            
            fin_data.append((name, role))
                                        
            f = open('all_players_per_team.pckl', 'rb')
            players_dict = pickle.load(f)
            f.close()
            players_dict[team_name].append(name)
            f = open('all_players_per_team.pckl', 'wb')
            pickle.dump(players_dict, f)
            f.close()
            
            
            f = open('all_roles.pckl', 'rb')
            roles_dict = pickle.load(f)
            f.close()
            roles_dict[name] = role
            f = open('all_roles.pckl', 'wb')
            pickle.dump(roles_dict, f)
            f.close()    
            
            
            
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        
                
    
    