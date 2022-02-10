
from PIL import Image, ImageDraw, ImageFont, ImageColor

class WordleColors:
    # black = (18, 18, 18)
    # gray = (58, 58, 60)
    # green = (82, 141, 77)
    # yellow = (180, 159, 58)
    # lgray = (55, 55, 55)
    # white = (255, 255, 255)
    gray = (51, 51, 51)
    green = (0, 196, 75)
    yellow = (193, 143, 57)
    white = (255, 255, 255)
    blue = (14, 22, 33)
    lgray = (55, 55, 55)

class ImageExport():

    board_x: int
    board_y: int
    alphabet = "abcdefghijklmnopqrstuvwxyzßäöüABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ"+"Åå"

    def __init__(self, x: int, y: int):
        self.board_x = x
        self.board_y = y

    def get_image(self, color_matrix, guessed_words):
        fnt=ImageFont.truetype('./assets/FiraCode-SemiBold.ttf', size=40)
        letter_size = {}
        for c in self.alphabet:
            letter_size[c] = fnt.getsize(c)

        c = WordleColors()
        TILE = 80
        LINE_THICKNESS = 4
        board_width = TILE * self.board_x + LINE_THICKNESS
        board_height = TILE * self.board_y + LINE_THICKNESS
        colors = color_matrix
        LETTER_OFFSET = 4

        im = Image.new('RGB' , (board_width +  2, board_height + 2), color=c.blue)
        draw = ImageDraw.Draw(im)

        for i in range(0, self.board_x):
            for j in range(0, self.board_y):
                if j < len(guessed_words):
                    draw.rectangle(
                        [(i * TILE + LINE_THICKNESS / 2, j * TILE + LINE_THICKNESS / 2), ((i + 1) * TILE + LINE_THICKNESS / 2, (j + 1) * TILE + LINE_THICKNESS / 2)],
                        width=LINE_THICKNESS, fill=colors[j][i], outline=c.blue)
                if len(guessed_words) > j:
                    l_pos = (   i * TILE + TILE / 2 - letter_size[guessed_words[j][i]][0] / 2 + LINE_THICKNESS / 2,
                                j * TILE + TILE / 2 - letter_size[guessed_words[j][i]][1] / 2 - LETTER_OFFSET+LINE_THICKNESS / 2)
                else:
                    shrink_rec = 4
                    draw.rectangle(
                        [(
                            i * TILE + LINE_THICKNESS / 2 + shrink_rec,
                            j * TILE + LINE_THICKNESS / 2 + shrink_rec
                        ),
                        (
                            (i + 1) * TILE + LINE_THICKNESS / 2 - shrink_rec,
                            (j + 1) * TILE + LINE_THICKNESS / 2 - shrink_rec
                        )],
                        width=2, fill=c.blue, outline=c.lgray
                    )
                if len(guessed_words) > j:
                    draw.text(l_pos, guessed_words[j][i], fill=c.white, font=fnt)
        return im