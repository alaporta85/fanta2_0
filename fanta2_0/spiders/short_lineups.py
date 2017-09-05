# This Spider scrapes:


#      All the lineups of the fantaplayers for each played day of the season.
#      The lineups will be saved inside a .pckl file and they will be stored
#      inside a dict. The keys of the dictionary are the players'names. Each
#      player has a value which is a list containing as many py lists as
#      the number of days of the season (already played). Each of these sublists
#      contains 23 tuples representing the players in the lineup for that
#      specific day. Each tuple has the form:
#
#             ('Day X', name_of_the_player)



import scrapy
from scrapy_splash import SplashRequest
import pickle
import os
import random

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

class Cday_lineups_votes(scrapy.Spider):
    
    def __init__(self):
        self.last_scraped_day = 0  # Last scraped day inside 'lineups.pckl'
        self.url_day = 0           # Day we are actually scraping
        self.cday = 0              # Days of Serie A already played
        self.count = 0             # Counter (see below inside parse_cday)
        
        # We load the names of the fanta-teams
        f = open('fantateams_names.pckl', 'rb')
        self.teams_names = pickle.load(f)
        f.close()
        
        # We set this condition to set properly the value of last day which is
        # already scraped. If the file 'lineups.pckl' doesn't exist inside the
        # wdir this value is 0, as initialized inside __init__. On the other
        # hand, if it is not the first time we run the script and there is
        # already a .pckl file containing the previous lineups what we do is:
        if os.path.isfile('short_lineups.pckl'):
            
            # We open the file containing the previous lineups
            f = open('short_lineups.pckl', 'rb')
            lineups = pickle.load(f)
            f.close()
            
            # Choose a random fanta-team from the lineups dict
            random_team = random.choice(list(lineups))
            
            # Take the value of the last day from which the lineup is scraped
            # and set it as last_scraped_day
            self.last_scraped_day = int(lineups[random_team][-1][0][0][3:])

    # To handle some 302 Redirecting issue
    handle_httpstatus_list = [302]
    
    name = 'short_lineups'
    
    # We divide all the links to scrape in three different lists. The reason
    # is that we need the value of self.cday to be scraped first because it
    # will be used later during the lineups' and votes' scraping. Putting all
    # the links inside start_urls would result in a random scraping
    start_urls = ['https://www.fantagazzetta.com/voti-fantacalcio-serie-a']
    
    lineups_urls = ['http://leghe.fantagazzetta.com/fantascandalo/'+
                    'formazioni?g=%d' % x for x in range(1,39)]

    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_cday,
                                endpoint='render.html',
                                args={'wait':0.5})
    
    def lineups_scraping(self, splash_response, teams_names):
        
        # Initialize the lineups dict
        lineups = {team:[] for team in teams_names}
        
        # All the tables containing the lineups
        tables = splash_response.xpath('//div[contains(@class, "col-lg-12")]'+
                                '/div[contains(@class, "row itemBox")]')
                
        for table in tables:
            
            # This is a counter we need because each table contains the lineups
            # of two fanta-teams. The counter is used to assign the correct
            # lineup to the correct fanta-team
            table_count = 0
            
            # Names of the fanta-teams
            team1 = table.xpath('.//h3/text()').extract()[0]
            team2 = table.xpath('.//h3/text()').extract()[2]
            
            # This element contains the two lineups
            lineups_container = table.xpath('.//tbody')
            
            for lineup in lineups_container:
                
                # Inside this list we will append the 23 tuples of the lineup
                fin_list = []
                
                # This element contains all the 23 players
                players_container = lineup.xpath('.//tr[contains(@class,'+
                                                 '"playerrow")]')
                
                for player in players_container:
                    
                    # Player's name
                    name = player.xpath('.//a/text()').extract_first()
                    

                    fin_tuple = ('Day %s' % self.url_day, name)
                        
                    fin_list.append(fin_tuple)
                
                # Depending on the value of the counter we assign the lineup
                # to the correct team
                if table_count == 0:
                    lineups[team1].append(fin_list)
                else:
                    lineups[team2].append(fin_list)
                
                # Increase the counter for the second team
                table_count += 1
        
        return lineups

    def parse_cday(self, response):
        
        # From the first link scraped (inside start_urls) we extract the
        # number of days of Serie A already played
        self.cday = int(response.xpath('//h3[contains(@class,"visible-sm-'+
                                       'block")]/span/text()').extract()[1])
        
        # Print to check in Terminal that everything is fine
        print('\n')
        print('Matches played in Serie A until today: %d.' % self.cday)
        print('\n')
                
        # Now we can start scraping the links inside lineups_urls. After some
        # work on the link we remove it from the list. The process will be
        # finished when lineups_urls is empy
        while len(self.lineups_urls) > 0:
            
            url = self.lineups_urls[0]
            # url_day is the day extracted from the link from which we want to
            # scrape. We extract it by using the actual string representing the
            # link, not from the html of the webpage
            self.url_day = int(url.split('=')[1])
            self.lineups_urls.remove(url)
                
            # First we check if url_day is a day not yet scraped
            if self.url_day > self.last_scraped_day:
                
                # If not, we check that url_day is a day not yet played
                if self.url_day < self.cday:
                    yield SplashRequest(url, self.parse_lineups,
                                        endpoint='render.html',
                                        args={'wait': 0.5})
                    
                # If we want scrape the page of the last day played we have to
                # be careful and do it only once. Doing it a second time would
                # cause wrong results all the links related to non played days
                # point to the page of the last played days
                elif self.url_day == self.cday and self.count == 0:
                    self.count = 1
                    yield SplashRequest(url, self.parse_lineups,
                                        endpoint='render.html',
                                        args={'wait': 0.5})
    
    def parse_lineups(self, response):
        
        # Here we need to extract again the url_day but not from the link we
        # want to scrape like before. This time we extract it directly from
        # the html we are scraping. We do this way because this parse_lineup
        # function is called after all the SplashRequests are sent. This means
        # that the value of url_day before entering in this function will be
        # the last value extracted from the string of the last link to which
        # the SplashRequest is sent (38 in our case). So if we don't set again
        # the correct value for url_day for each webpage we are scraping the
        # result will be that all the lineups will be scraped correctly but in
        # all the tuples the first element would be 'Day 38', which is wrong.
        self.url_day = response.xpath('//span[contains(@id,"LabelGiornata")]'+
                                      '/text()').extract_first().split()[0]
        self.url_day = int(self.url_day)
        
        # If there is no file created yet, we scrape and then store the result
        if not os.path.isfile('short_lineups.pckl'):
            lineups = self.lineups_scraping(response, self.teams_names)
            f = open('short_lineups.pckl', 'wb')
            pickle.dump(lineups, f)
            f.close()
        
        # If there is already the file with some already scraped data inside
        # then we first open it and load the content. Then we scrape the new
        # data, append them to the loaded variable and overwrite the old file
        # with the updated one.
        else:
            f = open('short_lineups.pckl', 'rb')
            lineups = pickle.load(f)
            f.close()
            
            new_lineups = self.lineups_scraping(response, self.teams_names)
            
            for team in lineups:
                lineups[team].append(new_lineups[team][0])
            
            f = open('short_lineups.pckl', 'wb')
            pickle.dump(lineups, f)
            f.close()
            
        # Print to check in Terminal that everything is fine
        print('\n')
        print('Lineups from day %d scraped successfully.' % self.url_day)
        print('\n')
        
                

            
                

            
            
        
                
                
        
        