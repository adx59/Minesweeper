#!/usr/bin/env python

###Minesweeper 0.8###

"""A clone of Microsoft's Minesweeper. Now in Python Edition. It is recommended that this game is run on a PC with
minimum requirements of a Intel Core i7 6400k, and a NVIDIA EVGA GeForce GTX 1080Ti, with 64 GB of DDR4 RAM, and finally
a 1 GB/s read&write speed SSD. If these requirements are not met, this program will shoot your computer with a BSOD.
Just kidding. But the grid might take a few seconds to load."""

__author__    = 'AZX'
__maintainer__ = 'AZX'
__status__   = 'Development-Production'

from tkinter import *
from tkinter import messagebox
import random
import sys


class mineCell(Button):
    def __init__(self, master, x, y, bomb):
        Button.__init__(self, master, width = 2, height = 1, text= '', bg ='white', relief = 'raised', command = self.show)
        self.grid(row = x, column = y)
        self.hidden = True
        self.bomb = bomb
        self.coords = (x, y)
        self.numOfBombsVal = self.master.findBombs(self.coords)
        self.shown = False
        self.marked = False
        self.bind('<Button-3>', self.markAsBomb)

    def show(self, noErrMsg = False):
        self.numOfBombsVal = str(self.master.findBombs(self.coords))
        if not self.shown:
            if self.numOfBombsVal == '':
                self['relief'] = 'sunken'
                self['bg'] = 'light gray'
                self['text'] = str(self.numOfBombsVal)
                self.shown = True
                self.master.autoExpose(self.coords)
            if self.bomb:
                self['bg'] = 'red'
                self['relief'] = 'sunken'
                if not noErrMsg:
                    messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)
                    self.master.showAllBombs()
                self.shown = True
            else:
                self['relief'] = 'sunken'
                self['bg'] = 'light gray'
                self['text'] = str(self.numOfBombsVal)
                self.shown = True
                print(self.coords)
                print(self.shown)
                print(self.bomb)
        else:
            pass

    def markAsBomb(self, bind):

        if not self.shown:
            self.marked = True
            self['bg'] = 'yellow'
            self['text'] = '*'
            self.shown = True
            if self.bomb:
                self.master.amntBombs -= 1
                self.master.amntBombsTKvar.set(self.master.amntBombs)
            else:
                messagebox.showerror('Minesweeper', 'That cell wasn\'t a bomb.', parent=self)
                sys.exit()
            if self.master.amntBombs == 0:
                messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent=self)
                messagebox.showinfo('Minesweeper', 'Now you can pick up your prize at 37.263832, -122.023015!')
                sys.exit()



class mineGrid(Frame):
    def __init__(self, master, xl, yl, amntBombs):
        Frame.__init__(self, master)
        self.grid()
        self.width = xl
        self.height = yl   #purely for reference for the mineLabel Object
        self.amntBombs = amntBombs
        self.amntBombsTKvar = IntVar()
        self.amntBombsTKvar.set(self.amntBombs)
        self.cells = {}
        self.bombPosLi = []
        for a in range(amntBombs):
            randPosX = random.randrange(xl)
            randPosY = random.randrange(yl)
            while (randPosX, randPosY) in  self.bombPosLi:
                randPosX = random.randrange(xl)
                randPosY = random.randrange(yl)
            self.bombPosLi.append((randPosX, randPosY))
        print(self.bombPosLi)
        for x in range(xl):
            for y in range(yl):
                if (x, y) in self.bombPosLi:
                    self.cells[(x,y)] = mineCell(self, x, y, True)
                    self.cells[(x,y)].grid(row = x, column = y)
                else:
                    self.cells[(x,y)] = mineCell(self, x, y, False)
                    self.cells[(x,y)].grid(row = x, column = y)
        bombLabel = Label(textvariable = self.amntBombsTKvar, font = ('Comic Sans MS', 15))   #I'm sorry
        bombLabel.grid()


    def findBombs(self, coords):
        x = coords[0]
        y = coords[1]
        numBombs = 0
        adjCoords = [(x-1,y), (x+1,y), (x,y-1), (x,y+1), (x-1,y-1), (x+1,y+1), (x-1,y+1), (x+1, y-1)]
        for cell in adjCoords:
            if (cell[0],cell[1]) in self.bombPosLi:
                numBombs += 1
            else:
                 continue
        if coords in self.bombPosLi:
            return 'bomb'
        if numBombs == 0:
            return ''
        else:
            return numBombs

    def autoExpose(self, coords):
        x = coords[0]
        y = coords[1]
        adjCellCoords = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
        for coords in adjCellCoords:
            tempCell1 = self.cells.get(coords)
            if isinstance(tempCell1, mineCell):
                if tempCell1.shown:
                    adjCellCoords.remove(coords)
            else:
                adjCellCoords.remove(coords)

        print('======Coords======')
        print((x,y))
        print(adjCellCoords)
        print('==================')
        for coords in adjCellCoords:
            tempCell = self.cells.get(coords)
            if isinstance(tempCell, mineCell):
                if not tempCell.shown:
                    tempCell.show()
            else:       #the cells at the edges can include non-existent mineCell objects that are 'NoneType'
                pass
            self.cells[coords] = tempCell

    def showAllBombs(self):
        for coords in self.bombPosLi:
            self.cells.get(coords).show(True)



def playMinesweeper(length, width, bombs):
    root = Tk()
    grid = mineGrid(root, length, width, bombs)
    #label for bombs
    grid.mainloop()


playMinesweeper(24,24,99)     #classic ol' minesweeper 24x24 w/ 99 bombs i can't win that can you?



