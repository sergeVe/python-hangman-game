import random
from string import ascii_lowercase


class Hangman:
    @staticmethod
    def print_welcome():
        print('H A N G M A N')

    def __init__(self):
        self.__state = 'welcome'
        self.__keyword = None
        self.__keywords = ['python', 'java', 'kotlin', 'javascript']
        self.__letters_number = None
        self.placeholder = '-'
        self.hint = []
        self.keyword_set = set()
        self.attempt = 8
        self.victory = False
        self.user_letters_set = set()
        self.deleted_letters_set = set()
        self.mistake_message = ''
        self.user_choice = ''

    @property
    def state(self) -> str:
        return self.__state

    @state.setter
    def state(self, state_string):
        self.__state = state_string

    @property
    def keyword(self) -> str:
        return self.__keyword

    @keyword.setter
    def keyword(self, new_word):
        self.__keyword = new_word

    @property
    def keywords(self) -> list:
        return self.__keywords

    @property
    def letters_number(self):
        return self.__letters_number

    @letters_number.setter
    def letters_number(self, number):
        self.__letters_number = number

    def print_query_message(self):
        self.user_choice = input('Type "play" to play the game, "exit" to quit:')

    def run(self):
        self.print_welcome()
        while True:
            if self.state == 'welcome':
                while self.user_choice not in ['play', 'exit']:
                    self.print_query_message()
                if self.user_choice == 'exit':
                    return None
                self.state = 'init'
            if self.state == 'init':
                self.init_func()
                self.state = 'on'
            if self.state == 'on':
                if not self.process_player():
                    self.state = 'off'
            if self.state == 'off':
                print(f'{self.get_analyze_result()}\n')
                self.user_choice = ''
                self.state = 'welcome'

    def process_player(self):
        print('\n' + ''.join(self.hint))
        answer = input('Input a letter: ')
        self.check_answer(answer)
        if len(self.keyword_set) == 0:
            self.victory = True
            return False
        if self.attempt == 0:
            return False
        return True

    def find_letter_pos(self, letter):
        letter_positions = []
        ind = 0
        while ind < len(self.keyword):
            pos = self.keyword.find(letter, ind)
            if pos == -1:
                break
            letter_positions.append(pos)
            ind = pos + 1

        return letter_positions

    def transform_hint(self, letter):
        positions = self.find_letter_pos(letter)
        temp = self.hint
        for ind in positions:
            temp[ind] = letter
        self.hint = temp

    def init_func(self):
        self.keyword = random.choice(self.keywords)
        self.keyword_set = set(self.keyword)
        self.hint = [self.placeholder for _i in range(len(self.keyword))]

    def check_answer(self, letter):
        if self.is_input_mistake(letter):
            print(self.mistake_message)
        elif letter in self.keyword_set:
            self.transform_hint(letter)
            self.keyword_set.discard(letter)
            self.deleted_letters_set.add(letter)
        else:
            if not self.victory:
                self.for_reduce_attempt(letter)
                print(self.mistake_message)

    def is_input_mistake(self, letter):
        if len(letter) != 1:
            self.mistake_message = 'You should print a single letter'
            return True
        if letter not in ascii_lowercase:
            self.mistake_message = 'It is not an ASCII lowercase letter'
            return True
        if any([letter in self.deleted_letters_set, letter in self.user_letters_set]):
            self.mistake_message = 'You already typed this letter'
            return True

        return False

    def get_analyze_result(self):
        if self.victory:
            return 'You guessed the word!\nYou survived!'
        return 'You are hanged!'

    def for_reduce_attempt(self, letter):
        self.user_letters_set.add(letter)
        self.mistake_message = 'No such letter in the word'
        self.attempt -= 1


hangman = Hangman()
hangman.run()
