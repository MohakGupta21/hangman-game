from tkinter import *
from random import choice
from words import word_list
import re

class CreateWindow(Canvas):
    """
        This class inherits of the class Canvas and creates the window where all the elements are displayed.
        """

    def __init__(self, parent, w, h, c, n):
        Canvas.__init__(self, width=w, height=h, bg=c)
        self.__numbermoves = n  # number of available moves.

    def displayImage(self):
        """
        Dispayed the different texts and shapes of the window.
        """
        # Images that represents the hangman.
        self.delete(ALL)
        # Depending on the number of moves available, displays the image of the hangman.
        nameImage = 'hangman{}.gif'.format(8 - self.__numbermoves)
        self.photo = PhotoImage(file=nameImage)
        self.create_image(0, 0, anchor=NW, image=self.photo)
        self.config(height=self.photo.height(), width=self.photo.width())

    def getnumbermovesavailable(self):
        """
        Return the number of moves available.
        """
        return self.__numbermoves

    def setnumbermovesavailable(self, n):
        """
        Set the number of moves available and give it the value n.
        """
        self.__numbermoves = n


class Player:
    """
    This class allows to create the profile of a player named "name" and with the score "scores".
    """

    def __init__(self, name, scores):
        self.__name = name
        self.__scores = scores

    def get_name(self):
        """
        Return the name of the player.
        """
        return self.__name

    def set_name(self, name):
        """
        CHange the name of the player with the given name "name".
        """
        self.__name = name

    def get_score(self):
        """
        Return the player's score.
        """
        return self.__scores

    def set_score(self, score):
        """
        Change the score of the player with the given score "score".
        """
        self.__scores = score

    def PlayerScoreName(self):
        """
        Return a string including the name and the score of the player.s
        """
        text = str(self.get_name()) + ' ' * 5 + str(self.get_score()) + '\n'
        return text


class Hangman(Tk, Player):
    """
    This class inherits of the class Tk and Player,
    implements the logic of the game and modifies the elements of the window.
    """
    def __init__(self):
        Tk.__init__(self)

        f2 = Frame(self)
        f2.pack(side=TOP, padx=5, pady=5)

        # Create a text area for the rules of the games and a few explanations.
        self.__instructions = Label(self)
        self.__instructions.pack(side=LEFT)
        self.__instructions.config(text=
                                   'Welcome dear user.' +
                                   '\n\nHere are the rules of the hangman game : ' +
                                   '\nYour goal is to find out the hidden word' +
                                   '\nin the bottom of the window, before the man ' +
                                   '\nis completely hanged. You can, if you want, give up' +
                                   '\nthe game by clicking on the button "Give up".' +
                                   '\nIf you are new around here, you can sign up' +
                                   '\nby clicking the button "Add a new player".' +
                                   '\nIf you are already registered, you can use again' +
                                   '\nyour profil by clicking on the button "Choose a player".' +
                                   '\nYou can whenever you wnt check your score and' +
                                   '\nthe scores of the other players by clicking on the button' +
                                   '\n"Players and scores". Each winning game gives you ' +
                                   '\n5 points plus the number of moves left behind.' +
                                   '\n\n Good luck and have fun ! ')

        self.__newWindow = CreateWindow(self, 480, 320, 'white', 7)
        self.title('Hangman game')
        self.__newWindow.pack(padx=5, pady=5)

        f1 = Frame(self)
        f1.pack(side=TOP, padx=5, pady=5)

        # Add the different buttons
        self.__NewGame = Button(f2, text='New game', width=15, command=self.NewGame).grid(row=0, column=0)
        self.__QuitGame = Button(f2, text='Exit', command=self.destroy).grid(row=0, column=1)
        self.__lmot = Label(self)
        self.__toGuess = ''
        self.__displayedWord = ''
        self.__lmot.pack(side=TOP)
        self.__lmot.config(text='Welcome, you can play by clicking on the button New Game')
        self.__buttons = []
        self.__buttonAbandon = Button(f2, text='Give up', width=30, command=self.abandon).grid(row=0, column=2)
        # Add the buttons to choose the letters
        for i in range(26):
            button = MyButton(self, f1, chr(ord('A') + i))
            button.grid(row=(i // 7) + 2, column=i - 7 * (i // 7) + 2)
            self.__buttons.append(button)
            self.__buttons[i].config(command=self.__buttons[i].click, state=DISABLED)
        self.__ListofPlayers = []
        self.__buttonplayers = Button(f2, text='Players and scores', width=30, command=self.Player_Scores).grid(row=0,
                                                                                                                column=4)
        self.__addnewplayer = Button(f2, text='Add a new player', width=30, command=self.AddNewPlayer).grid(row=0,
                                                                                                            column=5)
        self.__chooseplayer = Button(f2, text='Choose a player', width=30, command=self.ChoosePlayer).grid(row=0,
                                                                                                           column=6)
        self.__playerindex = 0
        self.__player = Label(self)
        self.__player.pack(side=TOP)
    def set_score(self, score):
        """
        Modify the score value of the current player with the given score.
        """
        self.__ListofPlayers[self.__playerindex].set_score(score)
    def get_score(self):
        """
        Return the score of the current player and None if it doesn't exist.
        """
        if self.__playerindex <= len(self.__ListofPlayers) - 1:
            return self.__ListofPlayers[self.__playerindex].get_score()
        return None
    def set_playerindex(self, name):
        """
        Search in the list of player the player with the given name and register the index in the list
        in a variable.
        """
        for i in range(len(self.__ListofPlayers)):
            if self.__ListofPlayers[i].get_name() == name:
                self.__playerindex = i
                return
    def get_playerindex(self):
        """
        Return the index of the current player in the list of players.
        """
        return self.__playerindex
    def AddName(self, fun, name):
        """
        Add the name of the wrote by the player and close the window.
        """
        name = name.get()
        fun.destroy()
        self.__ListofPlayers.append(Player(name, 0))
    def AddNewPlayer(self):
        """
        Allow a new player to sign up in the database.
        He become the game with a null score.
        """
        root = Tk()
        root.title('Add a player')
        label = Label(root, text='name : ')
        label.pack(side=LEFT, padx=5, pady=5)
        name = StringVar()
        text2 = Entry(root, bg='bisque', fg='maroon')  # textvariable= name,
        text2.focus_set()
        text2.pack(side=LEFT, padx=5, pady=5)
        button1 = Button(root, text='OK', command=lambda: self.AddName(root, text2)).pack(side=LEFT, padx=5, pady=5)
    def Player_Scores(self):
        """
        Display the latest players and their score.
        """
        text3 = 'Names:     Scores:\n'
        for i in self.__ListofPlayers:
            text3 += i.PlayerScoreName()
        root2 = Tk()
        root2.title('Players and scores')
        bouton = Button(root2, text='Exit', command=root2.destroy)
        bouton.pack(side=LEFT, padx=5, pady=5)
        lab = Label(root2, text=text3)
        lab.pack(side="left")
    def modif_player(self, player):
        """
        Modify the variable including the current player name and
        display his name on the window.
        """
        self.set_playerindex(player.get_name())
        self.__player.config(text='You are playing with : {}'.format(player.get_name()))
    def ChoosePlayer(self):
        """
        Display a window with a button for each signed up player
        and allow a player to chooose an existing profil.
        """
        root3 = Tk()
        root3.title('Choose a player')
        l = len(self.__ListofPlayers)
        for n in range(len(self.__ListofPlayers)):
            i = self.__ListofPlayers[n]
            Button(root3, text='{}'.format(i.get_name()), command=lambda i=i: self.modif_player(i)).grid(
                row=self.__ListofPlayers.index(i), column=0)
        Button(root3, text='Validate choice', command=root3.destroy).grid(row=l, column=0)
    def abandon(self):
        """
        Display the word in case of given up.
        :return:
        """
        self.__lmot.config(text='The word was - {} '.format(self.__mot))
        self.EndTheGame()
    def EndTheGame(self):
        """
        End the game.
        """
        for elt in self.__buttons:
            elt.config(state=DISABLED)
    def NewGame(self):
        """
        Start a new game : reboote the number of available moves,
        the window and generate a new word
        """
        self.__newWindow.delete(ALL)
        for elt in self.__buttons:
            elt.config(state=NORMAL)
        w = self.RandomWord()
        self.__newWindow.setnumbermovesavailable(7)
        self.__newWindow.displayImage()
        self.setGuess(w)
        self.setDisplayedWord('*' * len(w))
        self.__lmot.config(text='Word : {}'.format(self.__displayedWord))
    def setGuess(self, word):
        """Modify the word to guess by word."""
        self.__toGuess = word
    def setDisplayedWord(self, word):
        """Modify the displayed word by word."""
        self.__displayedWord = word
    def treatment(self, letter):
        """Implement the game logic when the player press a button."""
        x = re.findall(letter, self.__toGuess)
        if self.__newWindow.getnumbermovesavailable() >= 1:

            if len(x) == 0:  # if the lettter wasn't in the hidden word
                self.__newWindow.setnumbermovesavailable(self.__newWindow.getnumbermovesavailable() - 1)
                self.__newWindow.displayImage()
                if self.__newWindow.getnumbermovesavailable() == 0:
                    self.__lmot.config(text='{} - Sorry, you lost'.format(self.__toGuess))
                    self.EndTheGame()

            else:  # if one or more moves available
                for i in range(len(self.__toGuess)):
                    if self.__toGuess[i] == letter:  # if the choosen letter was on the hidden word

                        if i == len(self.__toGuess) - 1:
                            self.setDisplayedWord(self.__displayedWord[:i] + letter)
                        elif i == 0:
                            self.setDisplayedWord(letter + self.__displayedWord[1:])
                        else:
                            self.setDisplayedWord(self.__displayedWord[:i] + letter + self.__displayedWord[i + 1:])

                        self.__lmot.config(text='{}'.format(self.__displayedWord))

        if "*" not in self.__displayedWord:  # if no more hidden letters on the word to guess, that's a win
            self.__lmot.config(text='{} - Congratulations, you have won'.format(self.__displayedWord))
            if len(self.__ListofPlayers) > 0:
                self.set_score(5 + self.get_score() + self.__newWindow.getnumbermovesavailable())
            self.EndTheGame()
    def RandomWord(self):
        """
        Return a random word of the list.
        """
        word = choice(word_list)
        return word.upper()


class MyButton(Button):
    """
    This class inherits of the class Button and allows to create a button
    with text inside and to implement actions when the button is pressed.
    """

    def __init__(self, fen, f, tex):
        Button.__init__(self, master=f, text=tex)
        self.__t = tex
        self.fen = fen
        self.config(command=self.click)

    def click(self):
        """
        Run the game logic whenever the button is pressed.
        """
        self.config(state=DISABLED)
        self.fen.treatment(self.__t)


# Run the game
if __name__ == "__main__":
    fun = Hangman()
    fun.mainloop()
