import random
import tkinter
import datetime
from datetime import time, date, datetime
from tkinter import *

class Game:
    #creating game settings label
    def __init__(self, tk):
        self.TURN=1
        self.dimensionX = 4
        self.dimensionY = 4
        self.streaks = 5
        self.seconds_left=0
        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.won=0
        self.gameStarted=0
        self.gameRestarted=0
        self.beginning = datetime.now()
        self.icons = {
            "plain": PhotoImage(file="icons/tile_plain.gif"),
            "computer": PhotoImage(file="icons/computer.gif"),
            "human": PhotoImage(file="icons/human.gif"),
        }
        self.timeLabel=tkinter.Label(self.frame, text = "Time left: unset")
        self.timeLabel.grid(row=self.dimensionX, column=0, columnspan=self.dimensionY)
        self.streaksLabel = tkinter.Label(self.frame, text="How many in a row:")
        var0=StringVar()
        self.streakSP = Spinbox(self.frame, from_=1, to=40,textvariable=var0)
        var0.set(5)
        self.streakSP.grid(row=self.dimensionX + 1, column=10, columnspan=self.dimensionX)
        self.streaksLabel.grid(row=self.dimensionX+1, column=0, columnspan=self.dimensionX)
        self.sizeLabel = tkinter.Label(self.frame, text="Size x:")
        self.sizeLabel.grid(row=self.dimensionX+2, column=0, columnspan=self.dimensionX)
        var = StringVar()
        self.sizeSP = Spinbox(self.frame, from_=7, to=30, textvariable=var)
        var.set(19)
        self.sizeSP.grid(row=self.dimensionX + 2, column=10, columnspan=self.dimensionX)

        self.sizeLabel2 = tkinter.Label(self.frame, text="Size y:")
        self.sizeLabel2.grid(row=self.dimensionX + 3, column=0, columnspan=self.dimensionX)
        var1 = StringVar()
        self.sizeSP2 = Spinbox(self.frame, from_=7, to=30,textvariable=var1)
        var1.set(19)
        self.sizeSP2.grid(row=self.dimensionX + 3, column=10, columnspan=self.dimensionX)

        self.timeLimitLabel = tkinter.Label(self.frame, text="Time limit:")
        self.timeLimitLabel.grid(row=self.dimensionX + 4, column=0, columnspan=self.dimensionX)
        self.timeEntry=tkinter.Entry(self.frame)
        self.timeEntry.grid(row=self.dimensionX + 4, column=10, columnspan=self.dimensionX)
        self.startBtn = tkinter.Button(self.frame, text="Start", command=self.start_game)
        self.startBtn.grid(row=self.dimensionX + 5, column=0, columnspan=self.dimensionX)

    def initialize(self):
        self.frame2 = Frame(self.tk)
        self.frame2.pack()
        self.board = [[None] * self.dimensionY for _ in range(self.dimensionX)]
        self.squares=[[None] * self.dimensionY for _ in range(self.dimensionX)]
        if self.gameStarted:
            for i in range(self.dimensionX):
                for j in range(self.dimensionY):
                    self.squares[i][j] = tkinter.Label(self.frame2, text='    ', image=self.icons["plain"])
                    self.squares[i][j].grid(row=i, column=j)
                    self.squares[i][j].bind('<Button-1>', lambda e, i=i, j=j: self.on_click(i, j, e))
                    self.squares[i][j].bind('<Button-3>', lambda e, i=i, j=j: self.right_click(i, j, e))


        for i in range(self.dimensionX):
            for j in range(self.dimensionY):
                self.board[i][j]=0


    def printBoard(self):
        for i in range(self.dimensionX):
            print(self.board[i])

    def on_click(self,i, j, event):
        if(self.board[i][j]==0 and self.TURN==1):
            self.squares[i][j].config(image=self.icons["human"])
            self.board[i][j]=1
            self.TURN=-1
            self.checkGame(1)
            self.computerMoves(1)
            self.checkGame(-1)
            self.printBoard()

    def computerMoves(self,difficulty):
        print("the computer moved")
        if(difficulty==1):
            self.computerMoves1()
        self.TURN=1

    def computerMoves1(self):
        print("easy peasy")
        i,j=self.get_rnd_mov()
        self.squares[i][j].config(image=self.icons["computer"])
        self.board[i][j]=-1

    def right_click(self,i,j,event):
        self.squares[i][j].config(image=self.icons["computer"])
        self.board[i][j]=-1
        self.printBoard()

    def countdown(self):
        if(self.won==0):
            self.timeLabel['text'] = "Time left: " + str(self.seconds_left)

            if self.seconds_left:
                self.seconds_left -= 1
                self.frame.after(1000, self.countdown)
            else:
                self.gameOverTime()

    def checkGame(self,player):
        #line
        for i in range(self.dimensionX):
            currentLength = 0
            for j in range(self.dimensionY):
                if(self.board[i][j]==player):
                    currentLength+=1
                    if(currentLength==5):
                        print("SOMEONE WON")
                else:
                    currentLength=0
        #column
        for j in range(self.dimensionX):
            currentLength = 0
            for i in range(self.dimensionY):
                if(self.board[i][j]==player):
                    currentLength+=1
                    if(currentLength==5):
                        print("SOMEONE WON")
                else:
                    currentLength=0

        #diagonally


    def gameOverTime(self):
        self.timeLabel['text'] ="Game Over"
        for i in range(self.dimensionX):
            for j in range(self.dimensionY):
                self.board[i][j]=88


    def gameWon(self):
        self.won=1
        self.timeLabel['text'] = "You won"

    def pos_moves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    moves.append((i, j))
        return moves

    def get_rnd_mov(self):
        moves = self.pos_moves()
        j = random.randint(0, len(moves) - 1)
        return moves[j]

    #starts/restart the game
    def start_game(self):
        self.won=0
        if(self.timeEntry.get()):
            self.seconds_left = int(self.timeEntry.get())
        else:
            self.seconds_left=100
        self.countdown()
        self.dimensionX=int(self.sizeSP.get())

        self.dimensionY=int(self.sizeSP2.get())
        self.streaks=int(self.streakSP.get())
        self.gameStarted = 1
        if(self.gameRestarted):
            self.frame2.destroy()
        self.initialize()
        self.gameRestarted=1;


if __name__ == '__main__':
    window = Tk()
    window.title("Minesweeper")
    minesweeper = Game(window)
    window.mainloop()