import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

class AllLineups(scrapy.Spider):
    
    name = 'lineups'
            
    start_urls = ['http://leghe.fantagazzetta.com/fantascandalo/'+
                  'formazioni?g=2']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
                args={'wait': 0.3},
            )
            
    def teams_names_scraping(self, splash_response):
        
        teams_names = splash_response.xpath('//div[contains(@class,"darkgreybox")]/'+
                                    'div[contains(@class,"col-lg-5")]/h3/'+
                                    'text()').extract()
        
        return teams_names
    
    def lineups_scraping(self, splash_response, teams_names):
        
        day = splash_response.xpath('//ul[contains(@class,"mgiornate")]/'+
                                    'li[contains(@class,"active")]/a/'+
                                    'text()').extract_first()
        
        lineups = {team:[] for team in teams_names}
        
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
                    
                    malus = len(player.xpath('.//td[contains(@class,"tdrole")]'+
                                             '/img'))
                    
                    if player_class == 'playerrow' and malus == 0:
                        fin_tuple = ('Day %s' % day, name, 'YES', 'no_malus')
                    elif player_class == 'playerrow' and malus == 1:
                        fin_tuple = ('Day %s' % day, name, 'YES', '-0.5')
                    elif player_class == 'playerrow bnc' and malus == 0:
                        fin_tuple = ('Day %s' % day, name, 'NO', 'no_malus')
                    elif player_class == 'playerrow bnc' and malus == 1:
                        fin_tuple = ('Day %s' % day, name, 'NO', '-0.5')
                        
                    fin_list.append(fin_tuple)
                
                if count == 0:
                    lineups[team1].append(fin_list)
                else:
                    lineups[team2].append(fin_list)
                
                count += 1
        
        return lineups

    def parse(self, response):
        
        teams_names = self.teams_names_scraping(response)
        
        day = response.xpath('//ul[contains(@class,"mgiornate")]/'+
                             'li[contains(@class,"active")]/a/'+
                             'text()').extract_first()
        
        if not os.path.isfile('lineups.pckl'):
            lineups = self.lineups_scraping(response, teams_names)
            f = open('lineups.pckl', 'wb')
            pickle.dump(lineups, f)
            f.close()
        else:
            try:
                f = open('lineups.pckl', 'rb')
                lineups = pickle.load(f)
                f.close()
                
                new_day = 'Day %s' % day
                last_scraped_day = lineups[teams_names[0]][-1][0][0]
                
                if new_day != last_scraped_day:
                    new_lineups = self.lineups_scraping(response, teams_names)
                    
                    for team in lineups:
                        lineups[team].append(new_lineups[team])
                    
                    f = open('lineups.pckl', 'wb')
                    pickle.dump(lineups, f)
                    f.close()
            except IndexError:
                pass
                
            
            
        
                
                
        
        