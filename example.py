import time
from livesports import LiveSportsClient
client = LiveSportsClient(api_key='your_key')

# Rotating scoreboard example
scoreboard_index = 0
client.set_todays_nba_games_list()
while True:
    print(str(client.get_scoreboard_for_todays_game(client.games_today[scoreboard_index]).get_scoreboard()))
    scoreboard_index = scoreboard_index + 1
    if scoreboard_index == len(client.games_today):
        scoreboard_index = 0
    time.sleep(2)
