# This Spider scrapes two sets of data:


#   1. All the lineups of the fantaplayers for each played day of the season.
#      The lineups will be saved inside a .pckl file and they will be stored
#      inside a dict. The keys of the dictionary are the players'names. Each
#      player has a value which is a list containing as many py lists as
#      the number of days of the season (already played). Each of these sublists
#      contains 23 tuples representing the players in the lineup for that
#      specific day. Each tuple has the form:
#
#             ('Day X', name_of_the_player, 'YES'/'NO', 'no-malus'/'-0.5')
#
#      'YES' if the player is part of the 11 ones who contribute to the final
#      score, 'NO' if he isn't. 'no-malus' if, entering from the bench, he did
#      not receive any malus for wrong position, '-0.5' if he did.



#   2. All the data of each player in Serie A from Fantagazzetta.
#      The data will be saved in .pckl file called "serieA_votes" and they will
#      be stored inside a dictionary. The keys of the dictionary are the
#      players' names. Each player has a value which is a list containing
#      tuples. There is a tuple for each day of the season in which the player
#      has on official vote from Fantagazzetta. Each tuple contains 14 values
#      which are:
#
#               1. Day of the season                         (day)
#               2. Player's team name                        (name)
#               3. Vote from Fantagazzetta                   (FG_vote)
#               4. Alvin482 vote                             (ST_vote)
#               5. Yellow card                               (YC)
#               6. Red card                                  (RC)
#               7. Goals scored                              (Gs)
#               8. Goals scored on penalty                   (Gp)
#               9. Goals taken                               (Gt)
#              10. Penalty saved                             (Ps)
#              11. Penalty failed                            (Pf)
#              12. Owngoal                                   (Og)
#              13. Assist                                    (As)
#              14. Assist from free kick                     (Asf)
#
#      In case the player took part at the match but he has no vote because he
#      played not enough minutes to be evaluated, the value for FG_vote or
#      ST_vote will be 'n.e'.


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
        f = open('teams_names.pckl', 'rb')
        self.teams_names = pickle.load(f)
        f.close()
        
        # We set this condition to set properly the value of last day which is
        # already scraped. If the file 'lineups.pckl' doesn't exist inside the
        # wdir this value is 0, as initialized inside __init__. On the other
        # hand, if it is not the first time we run the script and there is
        # already a .pckl file containing the previous lineups what we do is:
        if os.path.isfile('lineups.pckl'):
            
            # We open the file containing the previous lineups
            f = open('lineups.pckl', 'rb')
            lineups = pickle.load(f)
            f.close()
            
            # Choose a random fanta-team from the lineups dict
            random_team = random.choice(list(lineups))
            
            # Take the value of the last day from whoich the lineup is scraped
            # and set it as last_scraped_day
            self.last_scraped_day = int(lineups[random_team][-1][0][0][3:])

    # To handle some 302 Redirecting issue
    handle_httpstatus_list = [302]
    
    name = 'cday_lineups_votes'
    
    # We divide all the links to scrape in two different py lists. The reason
    # is that we need the value of self.cday to be scraped first because it
    # will be used later during the lineups' scraping. Putting all the links
    # inside start_urls would result in a random scraping
    start_urls = ['https://www.fantagazzetta.com/voti-fantacalcio-serie-a']
    
    lineups_urls = ['http://leghe.fantagazzetta.com/fantascandalo/'+
                    'formazioni?g=%d' % x for x in range(1,3)]

    
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
                    
                    # We need the css class of the player because based on that
                    # we will assign a value of 'YES' or 'NO' inside the tuple
                    player_class = player.xpath('@class').extract_first()
                    
                    # Player's name
                    name = player.xpath('.//a/text()').extract_first()
                    
                    # To assign the malus we extract the len of the element:
                    # len == 0 means no-malus, len == 1 means '-0.5'
                    malus = len(player.xpath(
                            './/td[contains(@class,"tdrole")]/img'))
                    
                    if player_class == 'playerrow' and malus == 0:
                        fin_tuple = ('Day %s' % self.url_day, name,
                                     'YES', 'no_malus')
                    elif player_class == 'playerrow' and malus == 1:
                        fin_tuple = ('Day %s' % self.url_day, name,
                                     'YES', '-0.5')
                    elif player_class == 'playerrow bnc' and malus == 0:
                        fin_tuple = ('Day %s' % self.url_day, name,
                                     'NO', 'no_malus')
                    elif player_class == 'playerrow bnc' and malus == 1:
                        fin_tuple = ('Day %s' % self.url_day, name,
                                     'NO', '-0.5')
                        
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
        if not os.path.isfile('lineups.pckl'):
            lineups = self.lineups_scraping(response, self.teams_names)
            f = open('lineups.pckl', 'wb')
            pickle.dump(lineups, f)
            f.close()
        
        # If there is already the file with some already scraped data inside
        # then we first open it and load the content. Then we scrape the new
        # data, append them to the loaded variable and overwrite the old file
        # with the updated one.
        else:
            f = open('lineups.pckl', 'rb')
            lineups = pickle.load(f)
            f.close()
            
            new_lineups = self.lineups_scraping(response, self.teams_names)
            
            for team in lineups:
                lineups[team].append(new_lineups[team][0])
            
            f = open('lineups.pckl', 'wb')
            pickle.dump(lineups, f)
            f.close()
            
                
        print('\n')
        print('Lineups from day %d scraped successfully.' % self.url_day)
        print('\n')
                

            
                

            
            
        
                
                
        
        