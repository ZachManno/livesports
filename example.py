import time
from livesports import LiveSportsClient
client = LiveSportsClient(api_key='b2804be3-284c-4ab2-b085-892879')

# Rotating scoreboard example
scoreboard_index = 0
client.set_todays_nba_games_list()
while True:
    print(str(client.get_scoreboard_for_todays_game(client.games_today[scoreboard_index]).get_scoreboard()))
    scoreboard_index = scoreboard_index + 1
    if scoreboard_index == len(client.games_today):
        scoreboard_index = 0
    time.sleep(1)
