import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

class Teams_names(scrapy.Spider):
    
    name = 'fantateams_names'
    
    start_urls = ['http://leghe.fantagazzetta.com/fantascandalo/squadre']
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                args={'wait':0.5})
            
    def parse(self, response):
        
        teams_names = response.xpath('//div[contains(@class,"teambox")]/'+
                                     'div/h3/text()').extract()
        
        f = open('fantateams_names.pckl', 'wb')
        pickle.dump(teams_names, f)
        f.close()