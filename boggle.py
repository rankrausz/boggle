##############################################################################
# FILE : boggle.py
# WRITERS : Ran Krausz & Shai Wachtel
##############################################################################

import tkinter as tk
import datetime
from boggle_board_randomizer import *

class Boggle:
    """
    This class object is the boggle game. It contains the GUI plus the methods
    responsible for running the game correctly.
    """
    TIME = 180  # seconds
    GAME_TITLE = "Boggle Game"
    REGULAR_COLOR = 'lavender'
    HOVER_COLOR1 = "white"
    HOVER_COLOR2 = "tan1"
    LAST_COLOR = '#FFB821'
    PREVIOUS_COLOR = '#FCD481'
    BG_COLOR = '#F0F0F0'
    BOARD_SIZE = 4
    POSSIBLE_INDEXES = [i for i in range(BOARD_SIZE)]
    MOVES_DICT = {'right': (0, 1),
                  "left": (0, -1),
                  "up": (-1, 0),
                  "down": (1, 0),
                  "down_left": (1, -1),
                  "down_right": (1, 1),
                  "up_right": (-1, 1),
                  "up_left": (-1, -1)}

    def __init__(self, words):
        """
        Initialize a game object
        :param words: Words list from dictionary file
        """
        root = tk.Tk()
        root.title(Boggle.GAME_TITLE)
        root.resizable(False, False)

        self._main_window = root
        self._words = words

        self._buttons = {}
        self._current_path = []
        self._found_paths = []
        self._found = []
        self._score = 0
        self._start_screen()
        self._main_window.mainloop()

    def _start_screen(self):
        """
        Creates the GUI features on the opening screen of the game
        :return: None
        """
        self._start_text = tk.Label(self._main_window,
                                    text="Welcome to our Boggle game!")
        self._start_text.pack(anchor=tk.CENTER, padx=25, pady=25)
        self._b = tk.Button(self._main_window, command=self.game_screen,
                            text="Start Game!", width=13, height=2,
                            font=('Tahoma', 14, 'bold'), bg='#9DF55F')
        self._b.pack(anchor=tk.CENTER, padx=25, pady=25)

    def game_screen(self):
        """
        Creates the game screen GUI, containing all frames, labels and buttons.
        :return: None
        """
        self._new_game()

        self._start_timer(Boggle.TIME)
        self._score_label = tk.Label(self._main_window, text='Score: 0')
        self._score_label.pack(side=tk.TOP, anchor=tk.NE, padx=8)

        self._game_frame = tk.Frame(self._main_window)
        self._game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        self._build_board()

        self._lower_frame = tk.Frame(self._main_window)
        self._lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self._found_words = tk.Label(self._lower_frame, text='Found words: ',
                                     wraplength=360)

        self._found_words.pack(side=tk.BOTTOM, anchor=tk.SW)

        self._current_word = tk.Label(self._lower_frame, text="",
                                      font=("Courier", 32))
        self._current_word.pack(anchor=tk.CENTER)

        self._check_button = tk.Button(self._lower_frame, text='Check word',
                                       bg='sky blue', height=1, width=12,
                                       font=('Tahoma', 12, 'bold'),
                                       command=self._check_function)
        self._check_button.pack(anchor=tk.CENTER)

        self._clear_button = tk.Button(self._lower_frame, text='Clear choice',
                                       fg='red', width=9,
                                       command=self._clear_board)
        self._clear_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=5)

    def _clear_frame(self, frame):
        """
        Clear all widgets from the given frame
        :param frame: tk.Frame object
        :return:None
        """
        for widgets in frame.winfo_children():
            widgets.destroy()

    def _new_game(self):
        """
        Restart all parameters of the game, in order to start a new game from
        scratch
        :return: None
        """
        self._clear_frame(self._main_window)
        self._score = 0
        self._current_path = []
        self._found_paths = []
        self._words += self._found
        self._found = []

    def _flash(self, color):
        """
        Iterate over all cubes buttons, and make them flash twice by changing
        their color to red/green (given color), wait, and change again.
        :param color: chosen flashing color
        :return: None
        """
        for b in self._current_path:
            self._buttons[b]['bg'] = color  # 'chartreuse3'

        var = tk.IntVar()
        self._main_window.after(150, var.set, 1)
        self._main_window.wait_variable(var)

        for b in self._current_path:
            self._buttons[b]['bg'] = Boggle.REGULAR_COLOR

        self._main_window.after(150, var.set, 1)
        self._main_window.wait_variable(var)

        for b in self._current_path:
            self._buttons[b]['bg'] = color

        self._main_window.after(150, var.set, 1)
        self._main_window.wait_variable(var)

        for b in self._current_path:
            if b == self._current_path[-1]:
                self._buttons[b]['bg'] = Boggle.LAST_COLOR
            elif b in self._current_path:
                self._buttons[b]['background'] = Boggle.PREVIOUS_COLOR

    def _clear_board(self):
        """
        Get the board (cubes buttons) to a starting state, initialize current
        path and current word.
        :return: None
        """
        for b in self._buttons.values():
            b['bg'] = Boggle.REGULAR_COLOR
            b['state'] = tk.NORMAL
        self._current_path = []
        self._current_word['text'] = ''

    def _check_function(self):
        """
        The function binded to the 'Check word' button. It checks if the
        current word is in the dictionary. if not, calls flash function with
        red color. if yes, updates score, found words and dictionary.
        :return: None
        """
        if self._current_word['text'] not in self._words:
            self._flash('red')
        else:
            self._found_paths.append(self._current_path)
            self._score += (len(self._current_path)) ** 2
            self._score_label['text'] = 'Score: ' + str(self._score)
            self._flash('chartreuse3')

            self._found.append(self._current_word['text'])
            self._words.remove(self._current_word['text'])

            if len(self._found_paths) > 1:
                self._found_words['text'] += ', ' + self._current_word['text']
            else:
                self._found_words['text'] += self._current_word['text']
            self._clear_board()

    def _make_button(self, name, row, col):
        """
        The function creates a button and places it in the game frame.
        Then adds the button to buttons list
        :param name: the button name
        :param row: int - the row to place the button
        :param col: int - the column to place the button
        :return: None
        """
        button = tk.Button(self._game_frame, text=name, font=('Calbiri', 20),
                           height=2, width=4, bg=Boggle.REGULAR_COLOR)
        button.grid(row=row, column=col, sticky=tk.NSEW)
        self._buttons[(row, col)] = button

        def _on_enter(event):
            """
            When moving over a button of the board game the function changes
            the color of the button
            :return:
            """
            if button['stat'] == 'normal':
                button['background'] = Boggle.HOVER_COLOR1

        def _on_leave(event):
            """
            when the mouse pointer left the widget it changes the color of
            the button according to the last color the button had
            :return: None
            """
            if self._current_path:
                if (row, col) == self._current_path[-1]:
                    button['background'] = Boggle.LAST_COLOR
                elif (row, col) in self._current_path:
                    button['background'] = Boggle.PREVIOUS_COLOR
                else:
                    button['background'] = Boggle.REGULAR_COLOR
            else:
                button['background'] = Boggle.REGULAR_COLOR

        def _click(event):
            """
            when a button is pressed it changes its color and sets the buttons
            that can be pressed only to buttons next to the selected button
            :return: None
            """
            if button['state'] == tk.DISABLED:
                return

            if (row, col) not in self._current_path:  # empty clicked
                button['background'] = Boggle.LAST_COLOR
                self._current_path.append((row, col))
                self._current_word['text'] += name
                self._color_neighbors(row, col)
            else:  # red clicked
                self._current_path.remove((row, col))
                if self._current_path:
                    self._buttons[self._current_path[-1]]['bg'] = \
                        Boggle.LAST_COLOR
                    self._color_neighbors(self._current_path[-1][0],
                                          self._current_path[-1][1])
                else:
                    self._clear_board()
                new = self._current_word['text'][:-1]
                self._current_word['text'] = new

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        button.bind("<Button-1>", _click)
        return button

    def _color_neighbors(self, row, col):
        """
        Prevents pressing on all buttons and then allows to click only the
        nearby buttons to the selected button - the ones which are legal
        :param row: int - the row of the selected button
        :param col: int - the column of the selected button
        :return: None
        """
        for b in self._buttons.values():
            b['state'] = tk.DISABLED
        for i, j in Boggle.MOVES_DICT.values():
            if row + i in Boggle.POSSIBLE_INDEXES and col + j in Boggle.POSSIBLE_INDEXES:
                self._buttons[(row + i, col + j)]['state'] = tk.NORMAL
                if (row + i, col + j) in self._current_path:
                    self._buttons[(row + i, col + j)]['bg'] = \
                        Boggle.PREVIOUS_COLOR
                    self._buttons[(row + i, col + j)]['state'] = tk.DISABLED

        self._buttons[(row, col)]['state'] = tk.NORMAL

    def _build_board(self):
        """
        the function builds the board and calls _make_button function
        with the values it received from randomize_board function
        :return: None
        """
        board = randomize_board()
        for i in range(BOARD_SIZE + 1):
            tk.Grid.columnconfigure(self._game_frame, i, weight=1)
            tk.Grid.rowconfigure(self._game_frame, i, weight=1)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self._make_button(board[i][j], i, j)

    def _start_timer(self, seconds):
        """
        makes the timer label and starts the timer
        :param seconds: int - how many  seconds for the game to run
        :return: None
        """
        self._done_time = datetime.datetime.now() + \
                          datetime.timedelta(seconds=seconds)
        self._timer = tk.Label(text="sdf")
        self._timer.pack()
        self._countdown()

    def _countdown(self):
        """
        The function measures the time according to real times and
        changes the color of the timer according to the time that left
        :return: None
        """
        elapsed = self._done_time - datetime.datetime.now()
        m, s = elapsed.seconds / 60, elapsed.seconds % 60

        if s > Boggle.TIME:
            self._times_up()
        if m < 1:
            if s == 20:
                self._timer.configure(fg="orange")
            if s == 10:
                self._timer.configure(fg="red")
            if s == 0:
                self._times_up()
                return

        self._timer.configure(text="%02d:%02d" % (m, s))
        self._main_window.after(1000, self._countdown)

    def _times_up(self):
        """
        the function shows the player his score and opens new labels and
        buttons, that asks if he wants to play again or to quit
        :return: None
        """
        self._timer.configure(text="Time's up!", fg="blue")
        for widgets in self._lower_frame.winfo_children():
            widgets.destroy()
        for b in self._buttons.values():
            b['state'] = tk.DISABLED

        score_label1 = tk.Label(self._lower_frame, text='Your final score is:')
        score_label2 = tk.Label(self._lower_frame, text=str(self._score),
                                font=('Courier', 20, 'bold'),
                                fg='green', pady=10)

        score_label1.pack()
        score_label2.pack()

        again = tk.Label(self._lower_frame, text='Do you want to play again?')
        again.pack()

        yes_play = tk.Button(self._lower_frame, text='Yes', fg='green',
                             width=10, height=2, command=self.game_screen)
        no_play = tk.Button(self._lower_frame, text='No', fg='red', width=10,
                            height=2, command=self._main_window.destroy)
        yes_play.pack(side=tk.RIGHT, padx=(20, 90), pady=15)
        no_play.pack(side=tk.LEFT, padx=(90, 20), pady=15)


if __name__ == '__main__':
    with open('boggle_dict.txt') as f:
        words1 = f.readlines()

    words2 = [x.strip() for x in words1]

    start = Boggle(words2)
