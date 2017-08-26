# Spider to scrape all the data of each player in Serie A from Fantagazzetta.
# The data will be saved in .pckl file called "serieA_votes" and they will be
# stored inside a dictionary. The keys of the dictionary are the players'
# names. Each player has a value which is a py list containing tuples. There is
# a tuple for each day of the season in which the player has on official vote
# from Fantagazzetta. Each tuple contains 14 values which are:

#  1. Day of the season                         (day)
#  2. Player's team name                        (name)
#  3. Vote from Fantagazzetta                   (FG_vote)
#  4. Alvin482 vote                             (ST_vote)
#  5. Yellow card                               (YC)
#  6. Red card                                  (RC)
#  7. Goals scored                              (Gs)
#  8. Goals scored on penalty                   (Gp)
#  9. Goals taken                               (Gt)
# 10. Penalty saved                             (Ps)
# 11. Penalty failed                            (Pf)
# 12. Owngoal                                   (Og)
# 13. Assist                                    (As)
# 14. Assist from free kick                     (Asf)


import scrapy
from scrapy_splash import SplashRequest
import pickle
import os
import random

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

# Create an empty .pckl file if it doesn't exist otherwise I get an error
# from Scrapy.

if not os.path.isfile('serieA_votes.pckl'):                
    players_database = {}
    f = open('serieA_votes.pckl', 'wb')
    pickle.dump(players_database, f)
    f.close()

class Players_votes(scrapy.Spider):
    
    name = 'serieA_votes'
            
    start_urls = ['https://www.fantagazzetta.com/voti-'+
                  'fantacalcio-serie-a/2017-18/%d' % x for x in range(1,39)]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
#                args={'wait': 0.5},
            )
            
    def votes_scraping(self, splash_response):
        '''This function scrapes all the data for each player in Serie A, 
           creates the final tuple and store all the data in a .pckl file.'''
        
        day = int(splash_response.css('input[id="hGiornata"]::attr(value)')\
        .extract_first())                                                      # Day of the season.
        
        tables = splash_response.css('table.no-footer')                        # 20 tables containing the data of the players
                                                                               # for a specific day of the season.
        
        if len(tables) != 0:                                                   # To be sure to scrape only valid days of the season.
        
            f = open('serieA_votes.pckl', 'rb')
            players_database = pickle.load(f)
            f.close()
                    
            for table in tables:
                
                team_name = table.css('span.txtbig::text').extract_first()     # Name of the team (Atalanta, Benevento, etc.).
                
                players = table.css('tbody').css('tr')                         # All players who have vote in that specific day.
                            
                for player in players:
                    
                    role = player.css('td').css('span.role::text')\            # We extract the role of the player to make sure
                    .extract_first()                                           # we don't scrape data related to the coach.
                    
                    if role != 'ALL':                                          # So for every role which is different from
                                                                               # 'ALL' (coach) we start the scraping.
                        
                        data = player.css('tr').css('td')
                        
                        name = data[0].css('a::text').extract_first()
                        
                        try:
                            FG_vote = float(data[2].css('span::text')\         # If the vote is integer we don't have any problem.
                                            .extract_first())
                        except ValueError:
                            FG_vote = data[2].css('span::text').extract_first()# If it is a decimal number we have to replace the ','
                            FG_vote = float(FG_vote.replace(',', '.'))         # with a '.' before converting to float, otherwise
                                                                               # we get a ValueError.
                        try:
                            ST_vote = float(data[4].css('span::text')\
                                            .extract_first())
                        except ValueError:
                            ST_vote = data[4].css('span::text').extract_first()
                            ST_vote = float(ST_vote.replace(',', '.'))
                            
                        if len(data[4].css('span')) == 1:                      # If in the element data[4] we have only one span
                            YC = 0                                             # element that means that the player didn't receive
                            RC = 0                                             # any card (yellow or red).
                        
                        else:                                                  # On the other hand, two span elements inside data[4]
                            card = data[4].css('span')[1].css('::attr(class)')\# mean that the player DID receive a card. To know
                            .extract_first()                                   # which card we extract the class attribute of the 
                                                                               # second span element.
                            if 'trn-ry' in card:
                                YC = 1
                                RC = 0
                            elif 'trn-rr' in card:
                                YC = 0
                                RC = 1
                            
                        if len(data[8].css('td').css('span')) == 0:            # This element and the following ones have a span
                            Gs = 0                                             # element associated only in the case the value is
                        else:                                                  # != 0. In this case (goals scored), if the player
                            Gs = int(data[8].css('td').css('span::text')\      # scored any goal we extract the number from the
                                     .extract_first())                         # span element.
                        
                        if len(data[9].css('td').css('span')) == 0:            # Same condiderations.
                            Gp = 0
                        else:
                            Gp = int(data[9].css('td').css('span::text')\
                                     .extract_first())
                            
                        if len(data[10].css('td').css('span')) == 0:           # Same condiderations.
                            Gt = 0
                        else:
                            Gt = int(data[10].css('td').css('span::text')\
                                     .extract_first())
                            
                        if len(data[11].css('td').css('span')) == 0:           # Same condiderations.
                            Ps = 0
                        else:
                            Ps = int(data[11].css('td').css('span::text')\
                                     .extract_first())
                            
                        if len(data[12].css('td').css('span')) == 0:           # Same condiderations.
                            Pf = 0
                        else:
                            Pf = int(data[12].css('td').css('span::text')\
                                     .extract_first())
                            
                        if len(data[13].css('td').css('span')) == 0:           # Same condiderations.
                            Og = 0
                        else:
                            Og = int(data[13].css('td').css('span::text')\
                                     .extract_first())
                            
                        if len(data[14].css('td').css('span')) == 0:           # This element can have zero, one or two span elements
                            As = 0                                             # associated. Zero means no assist of any kind.
                            Asf = 0
                        elif len(data[14].css('td').css('span')) == 1:         # One means the player did a certain number of normal
                            As = int(data[14].css('td').css('span')[0]\        # assists (not from free kick) and we extract that
                                     .css('::text').extract_first())           # number.
                            Asf = 0
                        else:
                            As = int(data[14].css('td').css('span')[0]\        # Two means the player did a certain number of assists
                                     .css('::text').extract_first())           # and some or all of them are from free kick. In this
                            Asf = int(data[14].css('td').css('span')[1]\       # case we extract both numbers.
                                     .css('::text').extract_first())
                            
                        fin_tuple = (day,team_name,FG_vote,ST_vote,            # Create the final tuple.
                                     YC,RC,Gs,Gp,Gt,Ps,Pf,Og,As,Asf)
                            
                            
                        if name not in players_database:                       # If the player is not in the database we create his
                            players_database[name] = [fin_tuple]               # key and attach the value.
                        else:                                                  # If the player is already in the database we simply
                            players_database[name].append(fin_tuple)           # append the new tuple to the list of the previous ones.
                        
            f = open('serieA_votes.pckl', 'wb')                                # Save the updated version of the database.
            pickle.dump(players_database, f)
            f.close()

    def parse(self, response):
        
        f = open('serieA_votes.pckl', 'rb')
        players_database = pickle.load(f)
        f.close()
        
        day = int(response.css('input[id="hGiornata"]::attr(value)')\
        .extract_first())
        
        def check_day(players_database, day):
            '''This function checks if the votes of a specific day of the
               season have already been scraped. To do that, it takes 50
               random players from the database and store the last day
               they receive a vote. If the current day appears even only
               once in those values that means that the data for this day
               have already been scraped. On the other hand, if it does
               not appear it means that we need to scrape the new data.
               It return False if we don't need to scrape and True if we do.'''
               
            values = []
            for trial in range(50):
                random_player = random.choice(list(players_database))
                players_database[random_player][-1][0].append(values)
            if day in values:
                return False
            else:
                return True
            
        if len(players_database) == 0 or check_day(players_database, day):     # If the database is empty or the check function
            self.votes_scraping(response)                                      # returns True, we scrape.
        
        
        
                    
                    
                        
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            