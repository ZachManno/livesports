#!/usr/bin/env python3
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import platform
print(platform.python_version())
import livesports
from livesports import LiveSportsClient


class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        rotation = 0
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        #canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("../../../fonts/5x8.bdf")
        #font.CharacterWidth(500000)

        red = graphics.Color(255, 0, 0)
        #graphics.DrawLine(canvas, 5, 5, 22, 13, red)

        green = graphics.Color(0, 255, 0)
        #graphics.DrawCircle(canvas, 15, 15, 10, green)

        blue = graphics.Color(0, 0, 255)

        client = LiveSportsClient(api_key='my_key')
        scoreboard_index = 0
        client.set_todays_nba_games_list()
        length_of_games_today = len(client.games_today)
        home_score = ''
        away_score = ''
        final = ''

        while True:
            #if rotation % 2 == 0:
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

            #time.sleep(2)   # show display for 2 seconds before exit
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
    if (not graphics_test.process()):
        graphics_test.print_help()
