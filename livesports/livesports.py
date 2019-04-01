from datetime import date
import os
from ohmysportsfeedspy import MySportsFeeds

class LiveSportsClient(object):
    """
    Initilize by passing in api_key or setting it with the env var LS_API_KEY
    """

    def __init__(self, api_key=None):
        if api_key is None:
        	print("Api key is null, getting it from env var LS_API_KEY")
        	self.api_key = os.environ.get('LS_API_KEY')
        	if self.api_key is None:
        		raise ValueError("Api key not passed in and not available under env var LS_API_KEY")
        self.mysportsfeeds_client = MySportsFeeds('2.0',verbose=True)
        self.mysportsfeeds_client.authenticate(api_key, 'MYSPORTSFEEDS')

    def get_todays_nba_games(self, team_abbrev=None):
    	todays_date = date.today().strftime('%Y%m%d')
    	if team_abbrev: #Philly = PHI
    		return self.mysportsfeeds_client.msf_get_data(league='nba',season='latest',feed='daily_games',date=todays_date,team=team_abbrev, format='json',force='true')
    	else:
    		return self.mysportsfeeds_client.msf_get_data(league='nba',season='latest',feed='daily_games',date=todays_date, format='json',force='true')
