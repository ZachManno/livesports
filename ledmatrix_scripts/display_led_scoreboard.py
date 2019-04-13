#!/usr/bin/env python3
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import platform
print(platform.python_version())
import livesports
from livesports import LiveSportsClient

from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit

from threading import Timer


class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)
        self.refresh_weather()

    def refresh_weather(self):
        self.philly_weather = YahooWeather(APP_ID="RVSaie5a", api_key="my_key", 
                                api_secret="my_secret")
        self.philly_weather.get_yahoo_weather_by_city("philadelphia", Unit.fahrenheit)
        print("Updated weather")


    def run(self):
        rotation = 0
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        #canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("../../../fonts/5x8.bdf")

        weather_font = graphics.Font()
        weather_font.LoadFont("../../../fonts/4x6.bdf")

        green = graphics.Color(0, 255, 0)
        #graphics.DrawCircle(canvas, 15, 15, 10, green)

        blue = graphics.Color(0, 255, 213)

        yellow = graphics.Color(255, 255, 0)

        client = LiveSportsClient(api_key='my_key')
        scoreboard_index = 0
        client.set_todays_nba_games_list()
        length_of_games_today = len(client.games_today)
        home_score = ''
        away_score = ''
        final = ''

        while True:
            home_score, away_score, final = client.get_scoreboard_for_todays_game(client.games_today[scoreboard_index]).get_scoreboard()
            #home_score = "PHI 32"
            #away_score = "MIN 22"
            #final = "FINAL"
            if rotation % 2 == 0:
                graphics.DrawText(offscreen_canvas, font, 2, 9, blue, home_score)
                graphics.DrawText(offscreen_canvas, font, 2, 20, blue, away_score)
                graphics.DrawText(offscreen_canvas, font, 2, 30, blue, final)
            else:
                #home_score = "HHI 32"
                #away_score = "NNN 22"
                #final = "INALF"
                graphics.DrawText(offscreen_canvas, font, 2, 9, green, home_score)
                graphics.DrawText(offscreen_canvas, font, 2, 20, green, away_score)
                graphics.DrawText(offscreen_canvas, font, 2, 30, green, final)

            graphics.DrawText(offscreen_canvas, weather_font, 40, 6, yellow, self.philly_weather.condition.text)
            graphics.DrawText(offscreen_canvas, weather_font, 55, 13, yellow, str(self.philly_weather.condition.temperature))
            scoreboard_index = scoreboard_index + 1
            if scoreboard_index == length_of_games_today:
                scoreboard_index = 0
            rotation = rotation + 1
            if rotation == 90000:
                rotation = 0
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            offscreen_canvas = self.matrix.CreateFrameCanvas()
            time.sleep(5)
            home_score = ''
            away_score = ''
            final = ''


# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    # My "just get it working" solution after digging through python in-program cron scheduling forums:
    weather_update_interval = 900.0 #every 15 mins = 900.0
    for i in range(16): # 16 weather updates = assumes program runs for at max 4 hours. Also creates 16 threads
        Timer(weather_update_interval * i, graphics_test.refresh_weather).start()
    if (not graphics_test.process()):
        graphics_test.print_help()
