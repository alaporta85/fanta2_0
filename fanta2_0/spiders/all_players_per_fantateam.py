# Spider to scrape the players of each fantateam. They will be stored in a dict
# and saved inside a .pckl file. The keys of the dict are the names of the
# fantateams while the values are lists containing a tuple for each player. The
# tuple is:
#
#                       (name_of_the_player, roles)

import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

# The "try" method is used to avoid errors while launching the spider
# 'serieA_fantateams_schedule' to create those .pckl files.
try:
    class Players_Roles(scrapy.Spider):
        
        name = 'all_players_per_fantateam'
        
        start_urls = ['http://leghe.fantagazzetta.com/fantascandalo/'+
                      'tutte-le-rose']
    
        
        def start_requests(self):
            for url in self.start_urls:
                yield SplashRequest(url, self.parse,
                                    endpoint='render.html',
                                    args={'wait': 0.5})
    
        def parse(self, response):
            
            f = open('fantateams_names.pckl', 'rb')
            fantateams = pickle.load(f)
            f.close()
            
            players_dict = {team:[] for team in fantateams}
                        
            # Tables containing all the players, one table each fantateam
            all_tables = response.xpath('//table[contains(@class,"tbpink")]')
            
            # For each table
            for table in all_tables:
                
                # Extract the fantateam
                fantateam = table.xpath('.//h3/text()').extract_first()
                
                # All the players of the fantateam
                players = table.xpath('.//tbody/tr')
                
                # For each player
                for player in players:
                    
                    # Extract the role
                    roles = player.xpath('.//span[contains(@class,"role")]/'+
                                         'text()').extract()
                    
                    # Extract the name
                    name = player.xpath('.//a/text()').extract_first()
                    
                    # Extract the team
                    team = player.xpath('.//td[contains(@class,"aleft")]/'+
                                        'text()').extract_first()
                    
                    # Store the result in the dict
                    players_dict[fantateam].append((name,roles,team))
                
            # Save inside a .pckl file
            f = open('all_players_per_fantateam.pckl', 'wb')
            pickle.dump(players_dict, f)
            f.close()
            
            # Print at the end to confirm everything is fine
            print('\n')
            print('Players of all fantateams scraped correctly.')
            print('\n')
                
except FileNotFoundError:
    pass
            
            
            
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        
                
    
    