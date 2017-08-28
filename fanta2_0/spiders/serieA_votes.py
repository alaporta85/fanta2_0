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
                  'fantacalcio-serie-a/2017-18/%d' % x for x in range(1,3)]

    def start_requests(self):
        
        # We define the current day in the real league.
        current_day = 2
        
        f = open('serieA_votes.pckl', 'rb')
        players_database = pickle.load(f)
        f.close()
        
        for url in self.start_urls:
            # We extract the day from the url.
            url_day = int(url[::-1].split('/')[0])
            
            last_day = self.last_scraped_day(players_database)
            
            # 
            if ((url_day <= current_day and last_day < current_day)
            or len(players_database) == 0):
                yield SplashRequest(url, self.parse,
                    endpoint='render.html',
                    args={'wait': 0.5})
                
    def last_scraped_day(self, players_database):
        
        if len(players_database) == 0:
            return 0
        else:        
            fin_list = [data for player in players_database for data in
                        players_database[player]]
            
            last_scraped_day = sorted(fin_list, key=lambda x : x[0])[-1][0]
            
            return last_scraped_day
            
    def votes_scraping(self, splash_response):
        '''This function scrapes all the data for each player in Serie A, 
           creates the final tuple and store all the data in a .pckl file.'''
        
        # Day of the season.
        day = int(splash_response.xpath('//input[contains'+
                    '(@id,"hGiornata")]/@value').extract_first())
        
        # 20 tables containing the data of the players for a specific day of
        # the season.
        tables = splash_response.xpath('//table[contains(@class,"no-footer")]')
        
        f = open('serieA_votes.pckl', 'rb')
        players_database = pickle.load(f)
        f.close()
                
        for table in tables:
            
            # Name of the team (Atalanta, Benevento, etc.).
            team_name = table.xpath('.//span[contains(@class,"txtbig")]/'+
                                    'text()').extract_first()
            
            # All players who have vote in that specific day.
            players = table.xpath('.//tbody/tr')
                        
            for player in players:
                
                # We extract the role of the player to make sure we don't
                # scrape data related to the coach.
                role = player.xpath('.//span[contains(@class,"role")]/text()')\
                                    .extract_first()
                
                # So for every role which is different from 'ALL' (coach)
                # we start the scraping.
                if role != 'ALL':
                    
                    data = player.xpath('.//td')
                    
                    name = player.xpath('.//a/text()').extract_first()
                    
                    labelFG = data[2].xpath('.//span/@class').extract_first()\
                              .split(' ')[1]
                              
                    labelST = data[4].xpath('.//span/@class').extract_first()\
                              .split(' ')[1]
                    
                    try:
                        # If the vote is integer we don't have any problem.
                        FG_vote = float(data[2].xpath('.//span/text()')\
                                        .extract_first())
                        if 'grey' in labelFG:
                            FG_vote = 'n.e.'
                    except ValueError:
                        # If it is a decimal number we have to replace the
                        # ',' with a '.' before converting to float,
                        # otherwise we get a ValueError.
                        FG_vote = data[2].xpath('.//span/text()')\
                                        .extract_first()
                                        
                        if FG_vote == '-' or 'grey' in labelFG:
                            FG_vote = 'n.e.'
                        else:
                            FG_vote = float(FG_vote.replace(',', '.'))

                    try:
                        ST_vote = float(data[4].xpath('.//span/text()')\
                                        .extract_first())
                        if 'grey' in labelST:
                            ST_vote = 'n.e.'
                    except ValueError:
                        ST_vote = data[4].xpath('.//span/text()')\
                                        .extract_first()
                                        
                        if ST_vote == '-' or 'grey' in labelST:
                            ST_vote = 'n.e.'
                        else:
                            ST_vote = float(ST_vote.replace(',', '.'))
                        
                    # If in the element data[4] we have only one span
                    # element that means that the player didn't receive
                    # any card (yellow or red).
                    if len(data[4].xpath('.//span')) == 1:
                        YC = 0
                        RC = 0
                    
                    # On the other hand, two span elements inside data[4]
                    # mean that the player DID receive a card. To know
                    # which card we extract the class attribute of the
                    # second span element.
                    else:
                        card = data[4].xpath('.//span')[1].xpath('@class')\
                        .extract_first()

                        if 'trn-ry' in card:
                            YC = 1
                            RC = 0
                        elif 'trn-rr' in card:
                            YC = 0
                            RC = 1
                        
                    # This element and the following ones have a span
                    # element associated only in the case the value is
                    # != 0. In this case (goals scored), if the player
                    # scored any goal we extract the number from the
                    # span element.
                    if len(data[8].xpath('.//span')) == 0:
                        Gs = 0
                    else:
                        Gs = int(data[8].xpath('.//span/text()')\
                                 .extract_first())
                    
                    if len(data[9].xpath('.//span')) == 0:
                        Gp = 0
                    else:
                        Gp = int(data[9].xpath('.//span/text()')\
                                 .extract_first())
                        
                    if len(data[10].xpath('.//span')) == 0:
                        Gt = 0
                    else:
                        Gt = int(data[10].xpath('.//span/text()')\
                                 .extract_first())
                        
                    if len(data[11].xpath('.//span')) == 0:
                        Ps = 0
                    else:
                        Ps = int(data[11].xpath('.//span/text()')\
                                 .extract_first())
                        
                    if len(data[12].xpath('.//span')) == 0:
                        Pf = 0
                    else:
                        Pf = int(data[12].xpath('.//span/text()')\
                                 .extract_first())
                        
                    if len(data[13].xpath('.//span')) == 0:
                        Og = 0
                    else:
                        Og = int(data[13].xpath('.//span/text()')\
                                 .extract_first())
                        
                    # This element can have zero, one or two span elements
                    # associated. Zero means no assist of any kind.
                    if len(data[14].xpath('.//span')) == 0:
                        As = 0
                        Asf = 0
                    
                    # One means the player did a certain number of normal
                    # assists (not from free kick) and we extract that
                    # number.
                    elif len(data[14].xpath('.//span')) == 1:
                        As = int(data[14].xpath('.//span')[0]\
                                 .xpath('.//text()').extract_first())
                        Asf = 0
                    
                    # Two means the player did a certain number of assists
                    # and some or all of them are from free kick. In this
                    # case we extract both numbers.
                    else:
                        As = int(data[14].xpath('.//span')[0]\
                                 .xpath('.//text()').extract_first())
                        Asf = int(data[14].xpath('.//span')[1]\
                                  .xpath('.//text()').extract_first())
                        
                    # Create the final tuple.
                    fin_tuple = (day,team_name,FG_vote,ST_vote,
                                 YC,RC,Gs,Gp,Gt,Ps,Pf,Og,As,Asf)
                        
                    # If the player is not in the database we create his
                    # key and attach the value.
                    if name not in players_database:
                        players_database[name] = [fin_tuple]
                    
                    # If the player is already in the database we simply
                    # append the new tuple to the previous ones.
                    else:
                        players_database[name].append(fin_tuple)
                        
        # Save the updated version of the database.
        f = open('serieA_votes.pckl', 'wb')
        pickle.dump(players_database, f)
        f.close()

    def parse(self, response):
        
        self.votes_scraping(response)
        
        
        
                    
                    
                        
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            