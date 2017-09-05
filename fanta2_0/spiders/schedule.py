import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

class Schedule(scrapy.Spider):
    
    name = 'schedule'
    
    start_urls = ['http://leghe.fantagazzetta.com/fantascandalo/calendario']
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                args={'wait':0.5})
            
    def parse(self, response):
        
        schedule = {}
        
        tables = response.xpath('//table[contains(@class,"tbblu")]')
        for table in tables:
            fin_list = []
            day = table.xpath('.//h4/text()').extract_first().split()[0][0:-1]
            
            matches = table.xpath('.//td[contains(@class,"match")]')
            for match in matches:
                team1 = match.xpath('.//span[contains(@class,"tleft")]/'+
                                    'a/text()').extract_first()
                team2 = match.xpath('.//span[contains(@class,"tright")]/'+
                                    'a/text()').extract_first()
                
                fin_list.append((team1, team2))
            
            schedule[day] = fin_list
            
        print('\n')
        print('Schedule scraped succefully.')
        print('\n')
        
        f = open('schedule.pckl', 'wb')
        pickle.dump(schedule, f)
        f.close()