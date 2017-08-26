import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

try:

    class PlayersOfEachRealTeam(scrapy.Spider):
        
        name = 'real_teams_players'
            
        f = open('serieA_teams.pckl', 'rb')
        serieA_teams = pickle.load(f)
        f.close()
        
        start_urls = ['https://www.fantagazzetta.com/squadre/%s#rosa'
                      % team for team in serieA_teams]
    
        def start_requests(self):
            for url in self.start_urls:
                yield SplashRequest(url, self.parse,
                    endpoint='render.html',
    #                args={'wait': 0.5},
                )
    
        def parse(self, response):
            
            fin_data = []
                    
            team_name = response.css('h1::text').extract_first()
            
            table = response.css('table.dataTable').css('tbody')[0].css('tr')
            
            for player in table:
                
                data = player.css('td')
                
                name = data[0].css('::text').extract_first()
                
                role = data[2].css('::text').extract()
                
                fin_data.append((name, role))
                                
            if not os.path.isfile('real_teams_players.pckl'):
                
                fin_dict = {}
                fin_dict[team_name] = fin_data            
                f = open('real_teams_players.pckl', 'wb')
                pickle.dump(fin_dict, f)
                f.close()
                
            else:
                
                f = open('real_teams_players.pckl', 'rb')
                fin_dict = pickle.load(f)
                f.close()
                fin_dict[team_name] = fin_data
                f = open('real_teams_players.pckl', 'wb')
                pickle.dump(fin_dict, f)
                f.close()
                
except FileNotFoundError:
    pass
            
            
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        
                
    
    