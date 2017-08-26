import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

class NamesOfSerieATeams(scrapy.Spider):
    
    name = 'serieA_teams'
            
    start_urls = ['https://www.fantagazzetta.com/squadre']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
#                args={'wait': 0.5},
            )

    def parse(self, response):
        
        serieA_teams = []
        
        h3elem = response.css('h3.pull-left')
        
        for team in h3elem:
            
            team_name = team.css('::text').extract_first()
            
            serieA_teams.append(team_name)
            
        serieA_teams = serieA_teams[0:-1]
        
        f = open('serieA_teams.pckl', 'wb')
        pickle.dump(serieA_teams, f)
        f.close()