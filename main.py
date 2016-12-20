#!/usr/bin/env python

###Minesweeper 0.8###

"""A clone of Microsoft's Minesweeper. Now in Python Edition. It is recommended that this game is run on a PC with
minimum requirements of a Intel Core i7 6400k, and a NVIDIA EVGA GeForce GTX 1080Ti, with 64 GB of DDR4 RAM, and finally
a 1 GB/s read&write speed SSD. If these requirements are not met, this program will shoot your computer with a BSOD(Blue Screen of Death).
Just kidding. But the grid might take a few seconds to load."""

__author__    = 'AZX'
__maintainer__ = 'AZX'
__status__   = 'Development-Production(can still be played, but needs cosmetic changes).'

from tkinter import *
from tkinter import messagebox
import random
import sys


class mineCell(Button):
    def __init__(self, master, x, y, bomb):
        '''an object representing a cell in Minesweeper
            === methods ===
            show() -> exposes self
            markAsBomb() -> marks itself as a bomb'''
        Button.__init__(self, master, width = 2, height = 1, text= '', bg ='white', relief = 'raised', command = self.show)
        self.colorDict = {'bomb':'red', '':'light gray', '1':'blue', '2':'darkgreen', '3':'red', '4':'purple', '5':'maroon', '6':'cyan', '7':'black', '8':'gray'}
        self.grid(row = x, column = y)
        self.hidden = True
        self.bomb = bomb
        self.coords = (x, y)
        self.numOfBombsVal = self.master.findBombs(self.coords)
        self.shown = False
        self.marked = False
        self.bind('<Button-3>', self.markAsBomb)

    def show(self, noLoseMechanism = False):
        '''a method of the mineCell class that exposes the cell
            if the cell is a bomb, creates a err message and
            exits process'''
        self.numOfBombsVal = str(self.master.findBombs(self.coords))
        self['fg'] = self.colorDict[self.numOfBombsVal]
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
                if not noLoseMechanism:
                    messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)
                    self.master.showAllBombs()
                self.shown = True
            else:
                self['relief'] = 'sunken'
                self['bg'] = 'light gray'
                self['text'] = str(self.numOfBombsVal)
                self.shown = True
        else:
            pass

    def markAsBomb(self, bind):
        '''marks the cell as a bomb
            triggered when the cell
            is right clicked
            changes the cell to a yellow color and makes the text an asterisk'''
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
        '''A grid of mineCells is generated with nested for loops
            bombs are picked as a random coord and placed into a list
            mineCells are put in a dictionary with coords as keys
            === methods ===
            findBombs() -> finds the amount of bombs adjacent to a coordinate
            autoExpose() -> automatically exposes the cells surrounding an empty cell
            showAllBombs() -> shows all the bombs in the grid
            '''
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
        '''finds the bombs in the region surrounding a cell
            used to find the number to label a exposed cell
            findBombs(coords) -> amnt of surrounding bombs'''
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
        '''automatically exposes the cells around a empty cell.
            if the cells include another empty cell, recursion
            takes care of that. 
            autoExpose(coords) -> None'''
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


        for coords in adjCellCoords:
            tempCell = self.cells.get(coords)
            if isinstance(tempCell, mineCell):
                if not tempCell.shown:
                    tempCell.show()
            else:       #the cells at the edges can include non-existent mineCell objects that are 'NoneType'
                pass
            self.cells[coords] = tempCell

    def showAllBombs(self):
        '''shows all the bombs in the grid
            simply uses show function
            showAllBombs -> None'''
        for coords in self.bombPosLi:
            self.cells.get(coords).show(True)



def playMinesweeper(length, width, bombs):
    root = Tk()
    root.title('Minesweeper(Python)')
    root.iconbitmap('favicon.ico')
    grid = mineGrid(root, length, width, bombs)
    #label for bombs
    grid.mainloop()


playMinesweeper(24,24,99)     #classic ol' minesweeper 24x24 w/ 99 bombs i can't win that can you?



