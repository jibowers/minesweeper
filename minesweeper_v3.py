from tkinter import *
import random
import tkinter.messagebox
from datetime import datetime
import time

## game settings
game = [1,1,1]
diff = input("Difficulty level e/m/h/c :  ")
if diff == "e":
	game = [9,9,10]
elif diff == "m":
	game = [16, 16, 40]
elif diff =="h":
	game = [30, 16, 99]
else:
	game[1] = int(input("Number of rows: "))
	game[0] = int(input ("Number of colums: "))
	game[2] = int(input("Number of mines: "))

#print (game)
r = game[0]
c = game[1]
m = game[2]

numpressed = []

begin_time = datetime.now()


## grid stuff
root = Tk()
frame=Frame(root)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N+S+E+W)
grid=Frame(frame)
grid.grid(sticky=N+S+E+W, column=0, row=7, columnspan=2)
Grid.rowconfigure(frame, 7, weight=1)
Grid.columnconfigure(frame, 0, weight=1)
	
def with_callback(control, fun):
	def inner():
		return fun(control)
	control['command'] = inner
	return control

## what happens when you press
def test_callback(button):
	
	if not btn_map[str(button)][2]:
		btn_map[str(button)][2] = True
		numpressed.append("a")
		#print ("button instance:", button)
		what = str(btn_map[str(button)][1])
		if what == "X":
			button.config(bg = 'red', text = "XX", relief=GROOVE)
			print ("You blew up! at: ", button)
			#clear the board
			for x in range(r):
				for y in range(c):
					btn_list[x][y].config(bg = 'red', relief=GROOVE, text = str(btn_map[str(btn_list[x][y])][1]))
			tkinter.messagebox.showerror("Game over", "You blew up! :(")
			
		elif what == "0":
			button.config(relief=SUNKEN, bg= 'white', fg = 'yellow', text=what)
			clear_around(button)
		elif what == "1":
			button.config(relief=SUNKEN, bg= 'white', fg = 'cyan', text=what)
		elif what == "2":
			button.config(relief=SUNKEN, bg= 'white', fg = 'green', text=what)
		elif what == "3":
			button.config(relief=SUNKEN, bg= 'white', fg = 'orange', text=what)
		elif what == "4":
			button.config(relief=SUNKEN, bg= 'white', fg = 'magenta', text=what)
		else:
			button.config(relief=SUNKEN, bg= 'white', fg = 'black', text=what)
		##check if you win
		if len(numpressed) >= (r*c) - m:
			for x in range(r):
				for y in range(c):
					btn_list[x][y].config(text = ":)", bg = 'blue', relief=RIDGE)
			now_time = datetime.now()
			tdelta = now_time - begin_time
			sec = tdelta.total_seconds()
			tkinter.messagebox.showinfo("You won!", "Congraduations :D. You won in " + str(sec) + " seconds")
	
##supposed to be used to clear around "0"s, not functioning yet
def clear_around(button):
	#print("clear around")
	#print(type(button))
	x = btn_map[str(button)][0][0]
	y = btn_map[str(button)][0][1]
	#print(x,y)
	if x != 0: #not in left x=0 column
		if not btn_map[str(btn_list[x-1][y])][2]:
			test_callback(btn_list[x-1][y]) #uncover directly to left
	if x != r-1: # not in right x=8 column
		if not btn_map[str(btn_list[x+1][y])][2]:
			test_callback(btn_list[x+1][y]) #catch directly to right 
	if y != 0: # not in top y=0 row
		if not btn_map[str(btn_list[x][y-1])][2]:
			test_callback(btn_list[x][y-1]) #catch directly up
	if y != c-1: # not in bottom y=8 row
		if not btn_map[str(btn_list[x][y+1])][2]:
			test_callback(btn_list[x][y+1]) #catch directly down
	if x != 0 and y != 0: # not in y=0 or x=0 row
		if not btn_map[str(btn_list[x-1][y-1])][2]:
			test_callback(btn_list[x-1][y-1]) #catch upleft
	if x != 0 and y != c-1: # not in y=8 or x=0 row
		if not btn_map[str(btn_list[x-1][y+1])][2]:
			test_callback(btn_list[x-1][y+1]) #catch downleft
	if x != r-1 and y != 0: # not in y=0 or x=8 row
		if not btn_map[str(btn_list[x+1][y-1])][2]:
			test_callback(btn_list[x+1][y-1]) #catch upright
	if x != r-1 and y != c-1: # not in y=8 or x=8 row
		if not btn_map[str(btn_list[x+1][y+1])][2]:
			test_callback(btn_list[x+1][y+1]) #catch downright

def is_mine(button):
	#x = btn_map[str(button)][0][0]
	#y = btn_map[str(button)][0][1]
	#if "lamba" in str(btn_list[x][y]['command']):
		#return True
	if btn_map[str(button)][1] == "X":
		return True
	#btn_map[str(btn_list[x][y])][1]
		
field = [[0 for x in range(c)] for x in range(r)]
def record_field():
	for x in range(r):
		for y in range(c):
			count = 0
			#print ("recording field!")
			b = str(btn_list[x][y])
			if btn_map[str(btn_list[x][y])][1] == "X":
				field[x][y] = "X"
				#print("MINE")
				#print (field[x][y])
			else:
				if x != 0: #not in left x=0 column
					if is_mine(btn_list[x-1][y]):
						count += 1 #catch directly to left
				if x != r-1: # not in right x=8 column
					if is_mine(btn_list[x+1][y]):
						count += 1 #catch directly to right 
				if y != 0: # not in top y=0 row
					if is_mine(btn_list[x][y-1]):
						count += 1 #catch directly up
				if y != c-1: # not in bottom y=8 row
					if is_mine(btn_list[x][y+1]):
						count += 1 #catch directly down
				if x != 0 and y != 0: # not in y=0 or x=0 row
					if is_mine(btn_list[x-1][y-1]):
						count += 1 #catch upleft
				if x != 0 and y != c-1: # not in y=8 or x=0 row
					if is_mine(btn_list[x-1][y+1]):
						count += 1 #catch downleft
				if x != r-1 and y != 0: # not in y=0 or x=8 row
					if is_mine(btn_list[x+1][y-1]):
						count += 1 #catch upright
				if x != r-1 and y != c-1: # not in y=8 or x=8 row
					if is_mine(btn_list[x+1][y+1]):
						count += 1 #catch downright
				field[x][y] = str(count)
				btn_map[str(b)][1] = count
	return field

"""
def you_lost(button):
	print ("blew up! at:", button)
	tkMessageBox.showerror("You lost", "game over")
	button.config(bg = 'red', text = "XX")
"""
def set_mines(btn_list, mines):
	mines_placed = 0
	while mines_placed < mines:
		y = random.randint(0,c-1)#
		x = random.randint(0,r-1)#
		if btn_map[str(btn_list[x][y])][1] != "X": ###
			#btn_list[x][y].config(command = lambda: you_lost(btn_list[x][y]))
			#btn_list[x][y]['command'] = lambda: you_lost(btn_list[x][y])
			btn_map[str(btn_list[x][y])][1] =  "X"
			mines_placed += 1
	



#example values
btn_list = [[0 for x in range(c)] for x in range(r)] 
btn_map = {}

for x in range(r):
	for y in range(c):
		b = with_callback(Button(text="   "), test_callback)
		btn_list[x][y] = b
		btn_map[str(b)] = [[x, y], 0, False] #has not been pressed
		#print (b)
	
		b.grid(column=x, row=y, sticky=N+S+E+W)
#print (type(btn_list[0][0]))
#print(btn_list)
#print(btn_map)
#btn_list[0][0].config(relief=SUNKEN)
#

set_mines(btn_list, m)
#print (btn_map)
my_field = record_field()
#print (my_field)

		
for x in range(r):
	Grid.columnconfigure(frame, x, weight=1)

for y in range(c):
	Grid.rowconfigure(frame, y, weight=1)

root.mainloop()