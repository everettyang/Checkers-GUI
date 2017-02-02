#!/usr/bin/python
from Tkinter import *
import tkFont

'''Checkers implementation by Everett Yang for Python 2.7'''

class Checkers(Frame):

	def __init__(self, parent, color1 = 'silver', color2 = 'black', columns = 8, rows = 8, size = 100):
		"""columns and rows are defined, the canvas is drawn, variables defined, and the squares are made."""
		self.jumpable = []
		self.jumped_piece = None
		self.history_len = 0
		self.state = 'maroon'
		self.pieces = {'cyan':[], 'maroon': []}
		self.color1 = color1
		self.color2 = color2
		self.rows = rows
		self.columns = columns
		self.size = size
		canvas_height = rows * size
		canvas_width =  columns * size
		Frame.__init__(self, parent)
		self.canvas = Canvas(self, width = canvas_width, height = canvas_height, cursor = 'cross')
		self.canvas.pack(side = 'top', fill = 'both', expand = True)
		self.make_squares()
		self.make_labels()
		self.placepiece()
		self.setup_newturn()
		self.canvas.tag_bind(self.state, '<1>', self.piece_clicked)

#--------------------------------------------Display-------------------------------------------------

	def create_piece(self, name, columns, rows):
		"""add piece to board"""
		y0 = (columns * self.size) + int(self.size * .20)
		x0 = (rows * self.size) + int(self.size * .20)
		y1 = (columns * self.size) + int(self.size * .80)
		x1 = (rows * self.size) + int(self.size * .80)
		if name == 'cyan':
			piece = self.canvas.create_oval(x0, y0, x1, y1, tags = (name, 'piece'), fill = 'cyan')
			self.pieces['cyan'].append(piece)
			
		else:				
			piece = self.canvas.create_oval(x0, y0, x1, y1, tags = (name, 'piece'), fill = 'maroon')
			self.pieces['maroon'].append(piece)

	def placepiece(self):
		'''Place pieces on board'''

		for rows in range(3):
			if rows % 2 == 0:
				for column in range(8):
					if column % 2 != 0: 
						self.create_piece("maroon", rows, column) 
			else:
				for column in range(8):
					if column % 2 == 0:
						self.create_piece("maroon", rows, column) 
		for rows in range(5,8):
			if rows % 2 == 0:
				for column in range(8):
					if column % 2 != 0: 
						self.create_piece("cyan", rows, column) 
			else:
				for column in range(8):
					if column % 2 == 0:
						self.create_piece("cyan", rows, column) 
				
	def make_squares(self):
		'''appends rectangles to the parent widget'''
		color = self.color2
		for rows in range(self.rows):
			if color == self.color1:
				color = self.color2
			else:
				color = self.color1
			for col in range(self.columns):
				x1 = col * self.size
				y1 = rows * self.size
				x2 = x1 + self.size
				y2 = y1 + self.size
				self.canvas.create_rectangle(x1, y1, x2, y2, fill = color, tags = 'SQUARE', outline = 'white')
				if color == self.color1:
					color = self.color2
				else:
					color = self.color1
	def make_labels(self):
		'''makes the various labels for displaying history, stats, etc..'''

		#initialize font
		font = tkFont.Font(family = 'Helvetica', size = 12, weight = 'bold')
		font1 = tkFont.Font(family = 'Times', size = 10)
		font2 = tkFont.Font(family = 'Times', size = 10)
		font3 = tkFont.Font(family = 'Times', size = 48)
		

		#title label
		title = Label(root, height = 2 , width = 20, text = 'CHECKERS', font = font, relief= 'groove', cursor = 'clock')
		title.pack(side = TOP, padx = 1, pady = 1)

		#turn label
		self.text = StringVar()
		self.text.set(self.state[0].upper() + self.state[1:] + "'s" + ' turn.')
		status_label = Label(root,\
					 font = font1,\
					 height = 2,\
					 width = 15,\
					 textvariable = self.text,\
					 relief = 'sunken')
		status_label.pack(side = TOP, padx = 1, pady = 1)

		#end game label
		self.endgame_text = StringVar()
		self.endgame_text2 = StringVar()
		self.endgame_text.set('MAROON WINS!!!') 
		self.endgame_text2.set('CYAN WINS!!!') 

		self.endgame = Label(root,\
				 font = font3,\
				 bg = 'maroon',\
				 height = self.rows*self.size,\
				 width = self.columns*self.size,\
				 textvariable = self.endgame_text)

		self.endgame2 = Label(root, font = font3, bg = 'cyan', height = self.rows*self.size, width = self.columns*self.size, textvariable = self.endgame_text2)
		
		#history panel
		self.historybox = Listbox(root, font = font2, cursor = 'heart')
		self.historybox.pack(anchor = W, expand = 'true', fill = BOTH, side = LEFT)
		
		#jump label
		self.jump_text = StringVar()
		self.jump_text.set(self.state[0].upper() + self.state[1:] + ' has a jump!')
		self.jump_tag = Label(root,\
					 font = font1,\
					 height = 2,\
					 width = 15,\
					 textvariable = self.jump_text,\
					 relief = 'sunken')
				
		
		
#--------------------------------------------------Game----------------------------------------------

	def piece_clicked(self,event):
		'''responds to a piece being clicked, assigns variables, makes square outline.'''

		try:
			self.piece_squares, self.piece = self.canvas.find_overlapping(event.x,\
											 event.y,\
											 event.x,\
											 event.y)
		except ValueError:
			return
		self.pc_cords = self.canvas.coords(self.piece_squares)

		#solves the outline problem
		self.canvas.tag_raise(self.piece_squares)
		self.canvas.tag_raise(self.piece)

		self.canvas.itemconfig('SQUARE', outline = 'white' , width = 1)

		self.canvas.itemconfig(self.piece_squares, outline = 'gold', width = 3)
		self.canvas.tag_bind('SQUARE', '<1>', self.square_clicked)

	
	def square_clicked(self, event):
		"""executes when a piece is gotten and then a square is clicked, self.square is the square destination of the previously clicked piece."""

		self.canvas.tag_unbind('SQUARE', '<1>')
		self.square = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)[0]
		self.square_cords = self.canvas.coords(self.square)	
		self.turn_manager()

	def setup_newturn(self):
		"""sets up the input from mouse, resets variables, and calls event handler"""

		self.text.set(self.state[0].upper() + self.state[1:] + "'s" + ' turn.')
		self.canvas.tag_unbind('piece', '<1>')
		self.square = None
		self.jumped = None
		self.jumpable = []

		for piece in self.pieces[self.state]:
			self.check_for_jumps(piece)

		if self.jumpable:
			self.jump_text.set(self.state[0].upper() + self.state[1:] + ' has a jump!')
			self.jump_tag.pack(fill = BOTH, side = BOTTOM, expand = 'true')
			
		for nbpiece in self.jumpable:
			self.canvas.tag_bind(nbpiece, '<1>', self.piece_clicked)
			

		if not self.jumpable:
			self.canvas.tag_bind(self.state, '<1>', self.piece_clicked)
		

	def gameover(self):
		'''if either list of pieces is empty, end game.'''

		if not self.pieces['cyan']:
			self.endgame.pack()
			
		if not self.pieces['maroon']:
			self.endgame2.pack()

		self.canvas.tag_unbind('piece', '<1>')

	def turn_manager(self):
		"""This function manages jumps. If there is a jump, check the jump move. If there isnt a jump then go onto checks_move, which checks normal moves."""

		if self.jumpable:
			if self.check_jump_move() == 1:
				self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)

		#emptyness check if jump check is good
			elif not self.check_jump_move():
				if self.square_empty():
					self.jumped = 1
					self.do_move() 

				else:
					self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)
		else:
		#no jump
			self.checks_move()


	def checks_move(self):
		"""This function checks for normal move validity. If there is a jump it calls the function that checks the validity of jump move"""


		#direction check; blue is king	

		if self.canvas.itemcget(self.piece, 'outline') != 'blue':

			if self.state == 'cyan':

				if self.square_cords[1] > self.pc_cords[1]:
					self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)
					return 1
			else:
				if self.square_cords[1] < self.pc_cords[1]:
					self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)
					return 1
		#distance check

		if abs(self.square_cords[0] - self.pc_cords[0]) != self.size:
	
			self.text.set('Wrong Way!')
			self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)
			return 1

		if abs(self.square_cords[1] - self.pc_cords[1]) != self.size:
			self.text.set('Wrong Way!')
			self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)
			return 1

		if abs(self.square_cords[2] - self.pc_cords[2]) != self.size:
			self.text.set('Wrong Way!')
			self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)
			return 1

		if abs(self.square_cords[3] - self.pc_cords[3]) != self.size:
			self.text.set('Wrong Way!')
			self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)
			return 1

		if not self.square_empty():
			self.text.set('Square Occupied.')
			self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)
			return 1
		self.do_move()

	
	def square_empty(self):

		if len(self.canvas.find_overlapping(self.square_cords[0] + 10,\
							 self.square_cords[1] + 10,\
							 self.square_cords[2] - 10,\
							 self.square_cords[3] - 10)) == 2:
			return 0
		return 1

	
	
	def check_jump_move(self):
		"""this function checks for validity of jump move if a jump is available."""

		try:
			self.jumped_piece = self.canvas.find_overlapping(((self.square_cords[0] + 10) + (self.pc_cords[0] + 10))/2,\
	((self.square_cords[1] + 10) + (self.pc_cords[1] + 10))/2,\
	((self.square_cords[2] - 10) + (self.pc_cords[2] - 10))/2,\
	((self.square_cords[3] - 10) + (self.pc_cords[3] - 10))/2)[1]
		except IndexError:
			self.square = None
			self.jumped_piece = None
			self.canvas.itemconfig('SQUARE', outline = 'white', width = 1)

		vector = [i - j for i,j in zip(self.square_cords, self.pc_cords)]


		if self.canvas.itemcget(self.jumped_piece, 'fill') != self.state:

			if self.canvas.itemcget(self.piece, 'outline') != 'blue':
				if self.state == 'maroon':
					if all(abs(x) == 2 * self.size for x in vector) and all(x > 0 for x in vector[1::2]):
						return 0
					else:
						self.text.set('You must jump!')
						return 1
				else:
					if all(abs(x) == 2 * self.size for x in vector) and all(x < 0 for x in vector[1::2]):
						return 0
					else:
						self.text.set('You must jump!')
						return 1
			else:
					if all(abs(x) == 2 * self.size for x in vector):
						return 0
					else:
						self.text.set('You must jump!')
						return 1
			
	def remove_jumped_piece(self):
		"""removes jumped piece"""

		self.canvas.delete(self.jumped_piece)

		#on cyan's turn maroon gets removed	
		if self.state == 'cyan':
			self.pieces['maroon'].remove(self.jumped_piece)
			self.jumped_piece = None
		else:
			self.pieces['cyan'].remove(self.jumped_piece)
			self.jumped_piece = None


			self.jumped_piece = None
			
	def do_move(self):
		"""this function does the move and does the necessary cleaning up"""
		
		for pc in self.jumpable:
			self.canvas.tag_unbind(pc, '<1>')

		#this part actually does the move
		self.piece_offset = int(self.size * .20)
		if self.square != None:
			self.new_x1 = self.canvas.coords(self.square)[0] + self.piece_offset
			self.new_y1 = self.canvas.coords(self.square)[1] + self.piece_offset
			self.new_x2 = self.canvas.coords(self.square)[2] - self.piece_offset
			self.new_y2 = self.canvas.coords(self.square)[3] - self.piece_offset
			self.canvas.coords(self.piece, self.new_x1, self.new_y1, self.new_x2, self.new_y2)

			#calls the remove piece function. If there is no piece to be removed, pass.
			try:
				self.remove_jumped_piece()
			except ValueError:
				pass

			#assigns the variables for some functions called below

			self.canvas.itemconfig(self.piece_squares, outline = 'white', width = 1)

			#stat update
			self.text.set(self.state[0].upper() + self.state[1:] + "'s" + ' turn.')
			self.historybox.insert(self.history_len, 'Move' + ' ' + str(self.history_len + 1) + ':' + ' ' + 'Sq ' + str(self.piece_squares) + ' ' + 'to' +  ' ' + 'Sq.' + ' ' + str(self.square))
			self.history_len += 1

			#multi-jump checker
			
			self.jumpable = []
			if self.check_for_jumps(self.piece) and self.jumped:

				self.jumped = 0
				self.canvas.tag_unbind(self.state, '<1>')
				self.canvas.tag_bind(self.piece, '<1>', self.piece_clicked)
				self.square = None
				return

			self.jump_tag.pack_forget()

			#game over check
			self.gameover()
	
			#turn switch
			self.canvas.tag_unbind(self.state, '<1>')
			self.turn_switcher()
			
			self.setup_newturn()


	def check_for_jumps(self, piece):
		"""this function checks to see if a jump is available around the clicked piece."""

		#the 10 at the end is to make sure only one square is captured.
		pc_cords = self.canvas.coords(piece)

		self.ns1c = [pc_cords[0] - self.size + 10,\
			  pc_cords[1] - self.size + 10,\
			  pc_cords[2] - self.size - 10,\
			  pc_cords[3] - self.size - 10] 

		self.ns2c = [pc_cords[0] + self.size + 10,\
			  pc_cords[1] - self.size + 10,\
			  pc_cords[2] + self.size - 10,\
			  pc_cords[3] - self.size - 10]

		self.ns3c = [pc_cords[0] - self.size + 10,\
			  pc_cords[1] + self.size + 10,\
			  pc_cords[2] - self.size - 10,\
			  pc_cords[3] + self.size -10]

		self.ns4c = [pc_cords[0] + self.size + 10,\
			  pc_cords[1] + self.size + 10,\
			  pc_cords[2] + self.size - 10,\
			  pc_cords[3] + self.size - 10]

		#below are the blocks directly adjacent diagonally to the piece the function is checking.

		block1 = self.canvas.find_overlapping(self.ns1c[0],\
							 self.ns1c[1],\
							 self.ns1c[2],\
							 self.ns1c[3])

		block2 = self.canvas.find_overlapping(self.ns2c[0],\
							 self.ns2c[1],\
							 self.ns2c[2],\
							 self.ns2c[3])

		block3 = self.canvas.find_overlapping(self.ns3c[0],\
							 self.ns3c[1],\
							 self.ns3c[2],\
							 self.ns3c[3])

		block4 = self.canvas.find_overlapping(self.ns4c[0],\
							 self.ns4c[1],\
							 self.ns4c[2],\
							 self.ns4c[3])

		#the following series of if statements checks each neighboring square for a piece. If there is a neighboring piece, then if that neighboring piece is not the same color as the clicked piece, it is added to the list of jumpable pieces.


		if len(block1) == 2:
			self.block1_cords = self.canvas.coords(block1[0])

			adj_block = [self.block1_cords[0] - self.size + 10,\
						self.block1_cords[1] - self.size + 10,\
						self.block1_cords[2] - self.size - 10,\
						self.block1_cords[3] - self.size - 10]


			self.piece1 = block1[1] 
			if self.canvas.itemcget(self.piece1, 'fill') != self.state:
				if self.state == 'cyan' or self.canvas.itemcget(piece, 'outline') == 'blue':
						if len(self.canvas.find_overlapping(adj_block[0],\
										 adj_block[1],\
										 adj_block[2],\
										 adj_block[3])) == 1 and not any(x < 0 or x > self.rows * self.size for x in adj_block):

							self.jumpable.append(piece)
						
		if len(block2) == 2:

			self.piece2 = block2[1]
			self.block2_cords = self.canvas.coords(block2[0])

			adj_block = [self.block2_cords[0] + self.size + 10,\
						self.block2_cords[1] - self.size + 10,\
						self.block2_cords[2] + self.size - 10,\
						self.block2_cords[3] - self.size - 10]


			if self.canvas.itemcget(self.piece2, 'fill') != self.state:

				if self.state == 'cyan' or self.canvas.itemcget(piece, 'outline') == 'blue':
						if len(self.canvas.find_overlapping(adj_block[0],\
										 adj_block[1],\
										 adj_block[2],\
										 adj_block[3])) == 1 and not any(x < 0 or x > self.rows * self.size for x in adj_block):

							self.jumpable.append(piece)

		if len(block3) == 2:

			self.piece3 = block3[1] 
			self.block3_cords = self.canvas.coords(block3[0])

			adj_block = [self.block3_cords[0] - self.size + 10,\
 						self.block3_cords[1] + self.size + 10,\
						self.block3_cords[2] - self.size - 10,\
						self.block3_cords[3] + self.size - 10]



			if self.canvas.itemcget(self.piece3, 'fill') != self.state:

				if self.state == 'maroon' or self.canvas.itemcget(piece, 'outline') == 'blue':
						if len(self.canvas.find_overlapping(adj_block[0],\
										 adj_block[1],\
										 adj_block[2],\
										 adj_block[3])) == 1 and not any(x < 0 or x > self.rows * self.size for x in adj_block):

							self.jumpable.append(piece)

		if len(block4) == 2:

			self.piece4 = block4[1]
			self.block4_cords = self.canvas.coords(block4[0])

			adj_block = [self.block4_cords[0] + self.size + 10,\
						self.block4_cords[1] + self.size + 10,\
						self.block4_cords[2] + self.size - 10,\
						self.block4_cords[3] + self.size - 10]


			if self.canvas.itemcget(self.piece4, 'fill') != self.state:

				if self.state == 'maroon' or self.canvas.itemcget(piece, 'outline') == 'blue':
						if len(self.canvas.find_overlapping(adj_block[0],\
										 adj_block[1],\
										 adj_block[2],\
										 adj_block[3])) == 1 and not any(x < 0 or x > self.rows * self.size for x in adj_block):

							self.jumpable.append(piece)
		if self.jumpable:
			return 1
		return 0

	def king_checker(self):
		"""if a piece reaches the opposite side, then it is crowned with the almighty blue outline of royalty."""

		if self.state == 'maroon':
			if self.canvas.coords(self.square)[3] == int(self.size * self.columns):
				self.canvas.itemconfig(self.piece, outline = 'blue', width = 3)
		else:
				
			if self.canvas.coords(self.square)[1] == 0:
				self.canvas.itemconfig(self.piece, outline = 'blue', width = 3)

	def turn_switcher(self):
		"""the name speaks for itself: switches active state. Also checks for any potential kings to be crowned."""

		self.king_checker()

		if self.state == 'maroon':
			self.canvas.tag_unbind('maroon', '<1>')
			self.state = 'cyan'
		else:
			self.canvas.tag_unbind('cyan', '<1>')
			self.state = 'maroon'
			

#this if statement ensures that the script is called directly and not imported.
if __name__ == '__main__':
	root = Tk()
	board = Checkers(root)
	board.pack(side = TOP, fill = BOTH, expand = 'true', padx = 4, pady = 4)
	root.mainloop()
