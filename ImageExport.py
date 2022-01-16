from PIL import Image, ImageDraw, ImageFont, ImageColor
import sys


class WordleColors:
    black = (18, 18, 18)
    gray = (58, 58, 60)
    green = (82, 141, 77)
    yellow = (180, 159, 58)
    lgray = (55, 55, 55)
    white = (255, 255, 255)

class ImageExport():

    board_x: int
    board_y: int

    def __init__(self, x: int, y: int):
        self.board_x = x
        self.board_y = y

    def get_image(self, color_matrix, guessed_words):
        # font stuff
        fnt=ImageFont.truetype('./res/FiraCode-SemiBold.ttf', size=40)
        letter_size = {}
        for c in "abcdefghijklmnopqrstuvwxyzäöüABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ":
            letter_size[c] = fnt.getsize(c)

        c = WordleColors()
        # board_x = len(color_matrix[0])
        # board_y = len(color_matrix)

        TILE = 80
        LINE_THICKNESS = 4
        board_width = TILE * self.board_x + LINE_THICKNESS
        board_height = TILE * self.board_y + LINE_THICKNESS
        colors = color_matrix
        LETTER_OFFSET = 4

        im = Image.new('RGB' , (board_width +  2, board_height + 2), color=c.black)
        draw = ImageDraw.Draw(im)



        # fnt=ImageFont.truetype('arial.ttf', size=40)
        # Todo scalability
        for i in range(0, 5):
            for j in range(0, 6):
                if len(guessed_words) > j: l_pos = (i*TILE+TILE/2 - letter_size[guessed_words[j][i]][0]/2+LINE_THICKNESS/2, j*TILE+TILE/2 - letter_size[guessed_words[j][i]][1]/2-LETTER_OFFSET+LINE_THICKNESS/2)
                draw.rectangle([(i*TILE+LINE_THICKNESS/2, j*TILE+LINE_THICKNESS/2), ((i+1)*TILE+LINE_THICKNESS/2, (j+1)*TILE+LINE_THICKNESS/2)], width=LINE_THICKNESS, fill=colors[j][i], outline=c.black)
                if len(guessed_words) > j: draw.text(l_pos, guessed_words[j][i], fill=c.white, font=fnt)
        # im.show()
        return im