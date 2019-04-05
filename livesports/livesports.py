from datetime import datetime
from pytz import timezone
import os
from ohmysportsfeedspy import MySportsFeeds
from livesports.scoreboard import Scoreboard

class LiveSportsClient(object):
    """
    Initilize by passing in api_key or setting it with the env var LS_API_KEY
    """
    EASTERN_TIMEZONE = timezone('America/New_York')

    def __init__(self, api_key=None):
        if api_key is None:
        	print("Api key is null, getting it from env var LS_API_KEY")
        	self.api_key = os.environ.get('LS_API_KEY')
        	if self.api_key is None:
        		raise ValueError("Api key not passed in and not available under env var LS_API_KEY")
        self.mysportsfeeds_client = MySportsFeeds('2.0',verbose=True)
        self.mysportsfeeds_client.authenticate(api_key, 'MYSPORTSFEEDS')
        self.scoreboards = []
        self.games_today = []

    def get_todays_nba_games(self, team_abbrev=None):
        todays_date = datetime.now(LiveSportsClient.EASTERN_TIMEZONE).strftime('%Y%m%d')
        return self.get_daily_games_data_for_date(todays_date, team_abbrev)

    def get_daily_games_data_for_date(self, the_date, team_abbrev=None):
    	if team_abbrev: #Philly = PHI
    		return self.mysportsfeeds_client.msf_get_data(league='nba',season='latest',feed='daily_games',date=the_date,team=team_abbrev, format='json',force='true')
    	else:
    		return self.mysportsfeeds_client.msf_get_data(league='nba',season='latest',feed='daily_games',date=the_date, format='json',force='true')

    def set_todays_scoreboard(self, team_abbrev=None):
        scoreboards = []
        todays_games_data = self.get_todays_nba_games(team_abbrev)
        for game in todays_games_data['games']:
            scoreboards.append(
                Scoreboard(
                    game['schedule']['homeTeam']['abbreviation'],
                    game['schedule']['awayTeam']['abbreviation'],
                    game['schedule']['playedStatus'],
                    game['schedule']['startTime'],
                    game['score']['awayScoreTotal'],
                    game['score']['homeScoreTotal']
                    )
                )
        self.scoreboards = []
        self.scoreboards = scoreboards

    def set_todays_nba_games_list(self):
        self.games_today = []
        todays_games = self.get_todays_nba_games()
        for game in todays_games['games']:
            self.games_today.append(game['schedule']['awayTeam']['abbreviation'])

    def get_scoreboard_for_todays_game(self, team_abbrev):
        todays_game_data = self.get_todays_nba_games(team_abbrev)
        return Scoreboard(
                    todays_game_data['games'][0]['schedule']['awayTeam']['abbreviation'],
                    todays_game_data['games'][0]['schedule']['homeTeam']['abbreviation'],
                    todays_game_data['games'][0]['schedule']['playedStatus'],
                    todays_game_data['games'][0]['schedule']['startTime'],
                    todays_game_data['games'][0]['score']['awayScoreTotal'],
                    todays_game_data['games'][0]['score']['homeScoreTotal']
                    )


