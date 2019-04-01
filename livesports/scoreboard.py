import os
import dateutil.parser
from dateutil import tz

class Scoreboard(object):
    """
    Initilize by passing in api_key or setting it with the env var LS_API_KEY
    """

    FINISHED = ['COMPLETED','COMPLETED_PENDING_REVIEW']
    LIVE = 'LIVE'
    UNPLAYED = 'UNPLAYED'

    _EST_TIMEZONE=tz.gettz('America/New_York')

    def __init__(self, away_team, home_team, played_status, start_time, away_team_score=None, home_team_score=None):
        self.away_team = away_team
        self.home_team = home_team
        self.played_status = played_status
        self.start_time = self._parse_start_time(start_time)
        self.away_team_score = away_team_score
        self.home_team_score = home_team_score

    def get_scoreboard(self):
        if self.played_status in Scoreboard.FINISHED:
            return self.home_team + ' ' + str(self.home_team_score), self.away_team + ' ' + str(self.away_team_score), 'FINAL'
        if self.played_status == Scoreboard.LIVE:
            return self.home_team + ' ' + str(self.home_team_score), self.away_team + ' ' + str(self.away_team_score)
        if self.played_status == Scoreboard.UNPLAYED:
            return self.home_team, self.away_team, self.start_time

    def _parse_start_time(self, start_time):
        parsed_start_time = dateutil.parser.parse(start_time)
        parsed_time_est = parsed_start_time.astimezone(Scoreboard._EST_TIMEZONE)
        return parsed_time_est.strftime('%I:%M %p')