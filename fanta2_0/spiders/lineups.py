import scrapy
from scrapy_splash import SplashRequest
import pickle
import os
import random

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

class AllLineups(scrapy.Spider):
    
    def __init__(self):
        self.last_scraped_day = 0
        self.day = 0
        
        f = open('teams_names.pckl', 'rb')
        self.teams_names = pickle.load(f)
        f.close()
    
    name = 'lineups'
            
    start_urls = ['http://leghe.fantagazzetta.com/fantascandalo/'+
                  'formazioni?g=%d' % x for x in range(1,39)]
    
    if os.path.isfile('lineups.pckl'):
        f = open('lineups.pckl', 'rb')
        lineups = pickle.load(f)
        f.close()
        
        random_team = random.choice(list(lineups))
        
        last_scraped_day = int(lineups[random_team][-1][0][0][3:])
    
    
    def start_requests(self):
        for url in self.start_urls:
            
            url_day = int(url.split('=')[1])
            
            if url_day > self.last_scraped_day:            
                yield SplashRequest(url, self.parse,
                    endpoint='render.html',
                    args={'wait': 0.5})
    
    def lineups_scraping(self, splash_response, ateams_names):
                
        lineups = {team:[] for team in ateams_names}
        
        tables = splash_response.xpath('//div[contains(@class, "col-lg-12")]'+
                                '/div[contains(@class, "row itemBox")]')
        
        for table in tables:
            
            count = 0
                        
            team1 = table.xpath('.//h3/text()').extract()[0]
            team2 = table.xpath('.//h3/text()').extract()[2]
            
            lineups_container = table.xpath('.//tbody')
            
            for lineup in lineups_container:
                
                fin_list = []
                
                players_container = lineup.xpath('.//tr[contains(@class,'+
                                                 '"playerrow")]')
                
                for player in players_container:
                    
                    player_class = player.xpath('@class').extract_first()
                    
                    name = player.xpath('.//a/text()').extract_first()
                    
                    malus = len(player.xpath(
                            './/td[contains(@class,"tdrole")]/img'))
                    
                    if player_class == 'playerrow' and malus == 0:
                        fin_tuple = ('Day %s' % self.day, name,
                                     'YES', 'no_malus')
                    elif player_class == 'playerrow' and malus == 1:
                        fin_tuple = ('Day %s' % self.day, name,
                                     'YES', '-0.5')
                    elif player_class == 'playerrow bnc' and malus == 0:
                        fin_tuple = ('Day %s' % self.day, name,
                                     'NO', 'no_malus')
                    elif player_class == 'playerrow bnc' and malus == 1:
                        fin_tuple = ('Day %s' % self.day, name,
                                     'NO', '-0.5')
                        
                    fin_list.append(fin_tuple)
                
                if count == 0:
                    lineups[team1].append(fin_list)
                else:
                    lineups[team2].append(fin_list)
                
                count += 1
        
        return lineups

    def parse(self, response):
        
        self.day = int(response.xpath('//span[contains(@id,"LabelGiornata")]'+
                                      '/text()').extract_first().split()[0])
        
        if not os.path.isfile('lineups.pckl'):
            lineups = self.lineups_scraping(response, self.teams_names)
            f = open('lineups.pckl', 'wb')
            pickle.dump(lineups, f)
            f.close()
            
        else:
            f = open('lineups.pckl', 'rb')
            lineups = pickle.load(f)
            f.close()
            
            new_day = 'Day %d' % self.day
            new_day = int(new_day[3:])
            
            if new_day > self.last_scraped_day:
                new_lineups = self.lineups_scraping(response, self.teams_names)
                
                for team in lineups:
                    lineups[team].append(new_lineups[team])
                
                f = open('lineups.pckl', 'wb')
                pickle.dump(lineups, f)
                f.close()
            
                

            
            
        
                
                
        
        