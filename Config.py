good_word_text: str = "Good guess, keep trying!"
short_word_text: str = "The word is too short!"
long_word_text: str = "The word is too long!"
bad_word_text: str = "That word is not in the dictionary!"

# menu texts:
main_menu_text: str = "What do you want to do?"
settings_menu_text: str = "Choose what game settings you want to change:"
board_menu_text: str = "Choose the word length:"
feedback_menu_text: str = "Write your feedback in the chat:"
feedback_received_text: str = "Thank you for your feedback!"

help_text = "Game rules:\n" \
            "1. You need to guess a 5 letter word.\n" \
            "2. A yellow letter means that the letter is in the word, but in the wrong position.\n" \
            "3. A green letter means that the letter is in the word, and in the right position.\n" \
            "4. You have 6 guesses.\n" \
            "There are 3 different languages available: English, German and Swedish.\n" \
            "You can turn on hardmode, which makes the words to guess harder / less common\n" \
            "And you can change the word length to play games with words longer or shorter than 5 letters\n\n" \
            "Possible Commands:\n" \
            "/start - to reset the bot if something doesn't work\n" \
            "/help - Shows this message"

"""
    Commands for botfather:
    start - resets the bot
    new - starts a new game
    language - lets you choose another language
    help - shows this help message
"""