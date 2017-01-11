#!/usr/bin/env python

###Minesweeper 1.0###

"""A clone of Microsoft's Minesweeper. Now in Python Edition. It is recommended that this game is run on a PC with
minimum requirements of a Intel Core i7 6400k, and a NVIDIA EVGA GeForce GTX 1080, with 64 GB of DDR4 RAM, a 900W power supply, and finally
a 1 GB/s read&write speed SSD. If these requirements are not met, this program will shoot your computer with a BSOD(Blue Screen of Death).
Just kidding. But the grid might take a few seconds to load."""

__author__    = 'AZX'
__maintainer__ = 'AZX'
__status__   = 'Finished'

from tkinter import *
from tkinter import messagebox
import os
import random
import sys


class mineCell(Button):
    def __init__(self, master, x, y, bomb):
        """an object representing a cell in Minesweeper
            === methods ===
            show() -> exposes self
            markAsBomb() -> marks itself as a bomb"""
        #init button
        Button.__init__(self, master, width = 2, height = 1, text= '', bg ='white', relief = 'raised', command = self.show)
        #create attributes
        self.colorDict = {'bomb':'red', '':'light gray', '1':'blue', '2':'darkgreen', '3':'red', '4':'purple', '5':'maroon', '6':'cyan', '7':'black', '8':'gray'}
        self.grid(row = x, column = y)
        self.hidden = True
        self.bomb = bomb
        self.coords = (x, y)
        self.numOfBombsVal = self.master.findBombs(self.coords)
        self.shown = False
        self.marked = False
        #create binds
        self.bind('<Button-3>', self.markAsBomb)
        self.bind('<Button-1>', self.exitWhenLost)

    def show(self, showBombs = False):
        """a method of the mineCell class that exposes the cell
            if the cell is a bomb, creates a err message and
            exits process"""
        self.numOfBombsVal = str(self.master.findBombs(self.coords))
        #if it isn't marked with a bomb marker
        if not self.marked:
            self['fg'] = self.colorDict[self.numOfBombsVal]     #set the text color to the number of bombs key value in the colorDict
        #if it's not already shown
        if not self.shown:
            #if there are no bombs around it
            if self.numOfBombsVal == '':
                #cosmetic stuff
                self['relief'] = 'sunken'
                self['bg'] = 'light gray'
                self['text'] = str(self.numOfBombsVal)
                #make itself shown so there's no recursive loop
                self.shown = True
                #call on the autoExpose func
                self.master.autoExpose(self.coords)
            # if it's a bomb
            if self.bomb:
                #if the game's already ended and this is for the showAllBombs func
                if showBombs == True:
                    #cosmetic stuff only
                    self['bg'] = 'red'
                    self['relief'] = 'sunken'
                    self.shown = True
                #if the game is still going on
                else:
                    #cosmetics
                    self['bg'] = 'red'
                    self['relief'] = 'sunken'
                    self.shown = True
                    #lose the game
                    self.master.lose()

            else:
                #if it's not a bomb and we're just showing the number
                #cosmetic
                self['relief'] = 'sunken'
                self['bg'] = 'light gray'
                self['text'] = str(self.numOfBombsVal)
                #make itself shown
                self.shown = True
        else:
            #if it's already shown, just do nothing - pass
            pass
            

    def markAsBomb(self, bind):
        """marks the cell as a bomb
            triggered when the cell
            is right clicked
            changes the cell to a yellow color and makes the text an asterisk"""
        # if it's not shown
        if not self.shown:
            #change the marked attribute to true
            self.marked = True
            #cosmetics
            self['bg'] = 'yellow'
            self['text'] = '*'
            #change attribute shown
            self.shown = True
            #if it is a bomb
            if self.bomb:
                #subtract the amnt of bombs by 1
                self.master.amntBombs -= 1
                #make the tk variable for the label 1 less
                self.master.amntBombsTKvar.set(self.master.amntBombs)
            else:
                #lose(marked a not bomb)
                self.master.lose('markedNonBomb')
            if self.master.amntBombs == 0:
                #if we discover that they have 0 bombs now- marked em all
                #win
                self.master.win()     
                
    def exitWhenLost(self, bind):
        """Makes sure that the player isn't trying to click when they've already lost
            mineCell.exitWhenLost() -> None"""
        # if they've already lost but tried clicking on a cell
        if self.master.lost == True:     
            #exit
            sys.exit()


class mineGrid(Frame):
    def __init__(self, master, xl, yl, amntBombs):
        """A grid of mineCells is generated with nested for loops
            bombs are picked as a random coord and placed into a list
            mineCells are put in a dictionary with coords as keys
            === methods ===
            findBombs() -> finds the amount of bombs adjacent to a coordinate
            autoExpose() -> automatically exposes the cells surrounding an empty cell
            showAllBombs() -> shows all the bombs in the grid
            """
        #init frame
        Frame.__init__(self, master)
        self.grid()
        #set attributes
        self.width = xl
        self.height = yl
        self.lost = False
        self.amntBombs = amntBombs
        self.amntBombsTKvar = IntVar()    #label variable
        self.amntBombsTKvar.set(self.amntBombs)
        self.cells = {}   # cells dictionary key is coords
        self.bombPosLi = []    # bomb position list
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
        """finds the bombs in the region surrounding a cell
            used to find the number to label a exposed cell
            findBombs(coords) -> amnt of surrounding bombs"""
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
        """automatically exposes the cells around a empty cell.
            if the cells include another empty cell, recursion
            takes care of that. 
            autoExpose(coords) -> None"""
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
        """shows all the bombs in the grid
            simply uses show function
            showAllBombs -> None"""
        for coords in self.bombPosLi:
            self.cells.get(coords).show(True)

            
    def lose(self, type = 'openedBomb'):
        if type == 'openedBomb':
            self['bg'] = 'red'
            self['relief'] = 'sunken'            
            messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)
            self.showAllBombs()
        elif type == 'markedNonBomb':
            messagebox.showerror('Minesweeper', 'That cell wasn\'t a bomb! You lose!', parent=self)
            sys.exit()
        self.lost = True
            
    def win(self):
        messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent=self)
        messagebox.showinfo('Minesweeper', 'Haha, no. You don\'t need any congratulations. You probably made a custom size and bomb amount, and made it really easy.', parent=self)
        sys.exit()        
        
def loadConfigFile():
    """"""
    if os.path.isfile('configGrid.in'):
        configFile = open('configGrid.in', 'r')
        lineNum = 1
        xlen, ylen, amntBombs = 0, 0, 0
        for line in configFile:
            if lineNum == 1:
                xlen = int(line)
            elif lineNum == 2:
                ylen = int(line)
            elif lineNum == 3:
                amntBombs = int(line)
            elif lineNum == 4:
                break
            lineNum += 1
        return (xlen, ylen, amntBombs)
    else:
        messagebox.showerror('The file \'configGrid.in\' was not found. Please create this file, and put values in.')
        sys.exit()



def playMinesweeper(length, width, amntBombs):
    """plays minesweeper
        creates a grid and customizes the window
        the icon was proudly made by me"""
    info = loadConfigFile()
    root = Tk()
    root.title('Minesweeper')
    root.iconbitmap('favicon.ico')
    load = messagebox.askquestion('Minesweeper', 'Would you like to load the config file?')
    if load == 'yes':
        grid = mineGrid(root, info[0], info[1], info[2])
        grid.grid()
        root.mainloop()
    else:
        grid = mineGrid(root, length, width, amntBombs)
        grid.grid()
        root.mainloop()
    

playMinesweeper(24,24,99)     #default size, but can be set in the configGrid.in file
    
