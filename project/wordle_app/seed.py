from wordle_account.models import CustomUser
from wordle_word.models import Word


class StartGame:
    def __init__(self):
        pass

    def reset_words(self):
        Word.dangerously_reset()

    def reset_preface_users(self):
        CustomUser.delete_preface_users()
        CustomUser.create_preface_users()

    @staticmethod
    def reset_game():
        game = StartGame()
        game.reset_words()
        game.reset_preface_users()
