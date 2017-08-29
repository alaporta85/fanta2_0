import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

class Current_day(scrapy.Spider):
    
    name = 'current_day'
    
    start_urls = ['https://www.fantagazzetta.com/voti-fantacalcio-serie-a']
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint='render.html',
                                args={'wait':0.5})
            
    def parse(self, response):
        
        current_day = int(response.xpath('//h3[contains(@class,"visible-sm-'+
                                         'block")]/span/text()').extract()[1])
        
        f = open('current_day.pckl', 'wb')
        pickle.dump(current_day, f)
        f.close()