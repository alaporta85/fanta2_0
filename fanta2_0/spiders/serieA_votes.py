import scrapy
from scrapy_splash import SplashRequest
import pickle
import os
import random

path = '/Users/andrea/Desktop/fanta2_0'
os.chdir(path)

if not os.path.isfile('serieA_votes.pckl'):                
    players_database = {}
    f = open('serieA_votes.pckl', 'wb')
    pickle.dump(players_database, f)
    f.close()

class Players_votes(scrapy.Spider):
    
    name = 'serieA_votes'
            
    start_urls = ['https://www.fantagazzetta.com/voti-'+
                  'fantacalcio-serie-a/2017-18/1']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
#                args={'wait': 0.5},
            )
            
    def votes_scraping(self, splash_response):
        
        day = int(splash_response.css('input[id="hGiornata"]::attr(value)')\
        .extract_first())
        
        tables = splash_response.css('table.no-footer')
        
        f = open('serieA_votes.pckl', 'rb')
        players_database = pickle.load(f)
        f.close()
                
        for table in tables:
            
            team_name = table.css('span.txtbig::text').extract_first()
            
            players = table.css('tbody').css('tr')
                        
            for player in players:
                
                role = player.css('td').css('span.role::text').extract_first()
                
                if role != 'ALL':
                    
                    data = player.css('tr').css('td')
                    
                    name = data[0].css('a::text').extract_first()
                    
                    try:
                        FG_vote = float(data[2].css('span::text')\
                                        .extract_first())
                    except ValueError:
                        FG_vote = data[2].css('span::text').extract_first()
                        FG_vote = float(FG_vote.replace(',', '.'))
                        
                    try:
                        ST_vote = float(data[4].css('span::text')\
                                        .extract_first())
                    except ValueError:
                        ST_vote = data[4].css('span::text').extract_first()
                        ST_vote = float(ST_vote.replace(',', '.'))
                        
                    if len(data[4].css('span')) == 1:
                        YC = 0
                        RC = 0
                    else:
                        card = data[4].css('span')[1].css('::attr(class)')\
                        .extract_first()
                        if 'trn-ry' in card:
                            YC = 1
                            RC = 0
                        elif 'trn-rr' in card:
                            YC = 0
                            RC = 1
                        
                    if len(data[8].css('td').css('span')) == 0:
                        Gf = 0
                    else:
                        Gf = int(data[8].css('td').css('span::text')\
                                 .extract_first())
                    
                    if len(data[9].css('td').css('span')) == 0:
                        Gr = 0
                    else:
                        Gr = int(data[9].css('td').css('span::text')\
                                 .extract_first())
                        
                    if len(data[10].css('td').css('span')) == 0:
                        Gs = 0
                    else:
                        Gs = int(data[10].css('td').css('span::text')\
                                 .extract_first())
                        
                    if len(data[11].css('td').css('span')) == 0:
                        Rp = 0
                    else:
                        Rp = int(data[11].css('td').css('span::text')\
                                 .extract_first())
                        
                    if len(data[12].css('td').css('span')) == 0:
                        Rs = 0
                    else:
                        Rs = int(data[12].css('td').css('span::text')\
                                 .extract_first())
                        
                    if len(data[13].css('td').css('span')) == 0:
                        Au = 0
                    else:
                        Au = int(data[13].css('td').css('span::text')\
                                 .extract_first())
                        
                    if len(data[14].css('td').css('span')) == 0:
                        As = 0
                        Asf = 0
                    elif len(data[14].css('td').css('span')) == 1:
                        As = int(data[14].css('td').css('span')[0]\
                                 .css('::text').extract_first())
                        Asf = 0
                    else:
                        As = int(data[14].css('td').css('span')[0]\
                                 .css('::text').extract_first())
                        Asf = int(data[14].css('td').css('span')[1]\
                                 .css('::text').extract_first())
                        
                    fin_tuple = (day,team_name,FG_vote,ST_vote,
                                 YC,RC,Gf,Gr,Gs,Rp,Rs,Au,As,Asf)
                        
                        
                    if name not in players_database:
                        players_database[name] = [fin_tuple]
                    else:
                        players_database[name].append(fin_tuple)
                        
        f = open('serieA_votes.pckl', 'wb')
        pickle.dump(players_database, f)
        f.close()

    def parse(self, response):
        
        f = open('serieA_votes.pckl', 'rb')
        players_database = pickle.load(f)
        f.close()
        
        day = int(response.css('input[id="hGiornata"]::attr(value)')\
        .extract_first())
        
        def check_day(players_database, day):
            values = []
            for trial in range(50):
                random_player = random.choice(list(players_database))
                players_database[random_player][-1][0].append(values)
            if day in values:
                return False
            else:
                return True
            
        if len(players_database) == 0 or check_day(players_database, day):
            self.votes_scraping(response)
        
        
        
                    
                    
                        
                    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            