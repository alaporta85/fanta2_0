# Spider to scrape:
#
#   1.  The names of all Serie A's teams. The names are stored inside a list
#       and saved inside a .pckl file. These teams' names are used by the
#       spider called "all_players_and_roles" to scrape all the players,
#       together with thier Mantra roles, of each Serie A's team.
#
#   2.  The names of the fantateams which will be used by the spider
#       'cday_lineups_votes' to scrape the lineups for each day. They will be
#       stored in a .pckl file inside a list.
#
#   3.  The schedule of the fantaleague ('Fantascandalo' in our case).
#       It will be stored in a .pckl file inside a dict: the keys are the days
#       (1, 2, 3, etc etc) and values are lists containing tuples. Each tuple
#       represent a match of that day.


import scrapy
from scrapy_splash import SplashRequest
import pickle
import os

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

class SerieA_fantateams_schedule(scrapy.Spider):
    
    name = 'serieA_fantateams_schedule'
            
    start_urls = ['https://www.fantagazzetta.com/squadre',
                  'http://leghe.fantagazzetta.com/fantascandalo/squadre',
                  'http://leghe.fantagazzetta.com/fantascandalo/calendario']

    def start_requests(self):
        for url in self.start_urls:
            if 'calendario' in url:
                yield SplashRequest(url, self.parse_schedule,
                    endpoint='render.html',
                    args={'wait': 0.5})
            elif 'fantascandalo/squadre' in url:
                yield SplashRequest(url, self.parse_fantateams,
                    endpoint='render.html',
                    args={'wait': 0.5})
            else:
                yield SplashRequest(url, self.parse_serieA,
                    endpoint='render.html',
                    args={'wait': 0.5})

    def parse_serieA(self, response):
        
        # Extract the list with all the names
        serieA_teams = response.xpath('//h3[contains(@class,"pull-left")]/'+
                                      'a/text()').extract()
        
        # Save the final result
        f = open('serieA_teams.pckl', 'wb')
        pickle.dump(serieA_teams, f)
        f.close()
        
        # This message will shown in the Terminal if scraping goes fine
        print('\n')
        print('Serie A teams scraped succefully.')
        print('\n')
        
    def parse_fantateams(self, response):
        
        # Extract the list with all the fantanames
        teams_names = response.xpath('//div[contains(@class,"teambox")]/'+
                                     'div/h3/text()').extract()
        
        # Save the final result
        f = open('fantateams_names.pckl', 'wb')
        pickle.dump(teams_names, f)
        f.close()
        
        # This message will shown in the Terminal if scraping goes fine
        print('\n')
        print('Fantateams scraped succefully.')
        print('\n')
        
    def parse_schedule(self, response):
        
        # This dict will be filled with final result
        schedule = {}
        
        # All the tables containing all the days of the schedule
        tables = response.xpath('//table[contains(@class,"tbblu")]')
        
        # For each day of the schedule
        for table in tables:
            
            # Initialize an empty list to store all the matches for this day
            fin_list = []
            
            # Extract the number representing the day
            day = table.xpath('.//h4/text()').extract_first().split()[0][0:-1]
            
            # All the matches of that specific day
            matches = table.xpath('.//td[contains(@class,"match")]')
            
            # For each match
            for match in matches:
                
                # Extract the names of both fantateams
                team1 = match.xpath('.//span[contains(@class,"tleft")]/'+
                                    'a/text()').extract_first()
                team2 = match.xpath('.//span[contains(@class,"tright")]/'+
                                    'a/text()').extract_first()
                
                # Append them as a single tuple
                fin_list.append((team1, team2))
            
            # Store the whole day inside the dict
            schedule[day] = fin_list
        
        # Save the final result
        f = open('schedule.pckl', 'wb')
        pickle.dump(schedule, f)
        f.close()
        
        # This message will shown in the Terminal if scraping goes fine
        print('\n')
        print('Schedule scraped succefully.')
        print('\n')