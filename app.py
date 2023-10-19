from tkinter import *
import customtkinter as ctk
from build_scrapper import get_one_champ_data, get_one_champ_image, champion_names, original_champion_names
from image_combiner import get_build_image, delete_image, get_concat_h
from PIL import Image
import random
import requests
import os

# FONTS 
CHAMP_LIST_FONT = ('Arial', 14, 'bold')
POP_UP_FONT = ("Corbel", 18, 'bold')

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		# configure window
		self.title("LoL - Buildle")
		self.resizable(False, False)
		self.bind('<Return>', self.selected_item)
		if os.path.isfile('mistake_champ_img.png'):
			delete_image('mistake_champ_img.png')


		random_champ = random.choice(champion_names)

		self.champ_data = get_one_champ_data(random_champ)
		get_build_image(self.champ_data)
		self.build_image = ctk.CTkImage(light_image=Image.open('result.jpg'), dark_image=Image.open('result.jpg'), size=(192, 128))
		self.mistakes_counter = 0 

		# FRAMES
		self.search_frame = ctk.CTkFrame(self, corner_radius=0)
		self.search_frame.grid(row=0, column=0, sticky='nswe')

		self.champs_frame = ctk.CTkFrame(self, corner_radius=0)
		self.champs_frame.grid(row=1, column=0, sticky='nswe')

		self.build_frame = ctk.CTkFrame(self, corner_radius=0)
		self.build_frame.grid(row=0, column=1, sticky='nswe')
		self.build_frame.grid_columnconfigure(0,weight=1)

		self.mistakes_frame = ctk.CTkFrame(self, corner_radius=0)
		self.mistakes_frame.grid(row=1, column=1, sticky='nswe')
		self.mistakes_frame.grid_columnconfigure(0,weight=1)

		# SEARCH FRAME WIDGETS
		ctk.CTkLabel(self.search_frame, text='Search:').grid(row=0, column=0, padx=20, pady=(50,5), sticky='nswe')
	   
		self.filter_box = ctk.CTkEntry(self.search_frame)
		self.filter_box.grid(row=0, column=1, sticky='nswe', padx=10, pady = (50,5))
		self.submit_button = ctk.CTkButton(self.search_frame, text = 'Submit', command=self.selected_item)
		self.submit_button.grid(row=1, column=0, sticky='nswe', padx=10, pady = 5, columnspan=2)
		self.submit_button.grid_columnconfigure(1, weight=1)

		# BUILD FRAME WIDGETS
		self.build_button = ctk.CTkButton(self.build_frame, image = self.build_image, text = '', fg_color = 'transparent', state='disabled', anchor='center')
		self.build_button.grid(row=0,column=0,sticky='nswe', padx = 20, pady = 20)

		# CHAMPS FRAME WIDGETS
		self.listbox = Listbox(self.champs_frame, font = CHAMP_LIST_FONT, borderwidth = 0)
		self.listbox.grid(row=1, column=0, sticky='nswe')

		yscrollbar = Scrollbar(self.champs_frame, orient='vertical')
		yscrollbar.grid(row=1, column=1, sticky='ns')
		yscrollbar.config(command=self.listbox.yview)

		# MISTAKES CHAMPIONS FRAME WIDGETS

		ctk.CTkLabel(self.mistakes_frame,text = "Mistakes: ", font = ('Arial', 14, 'bold')).grid(row=0,column=0,pady=10)
		
		# OTHER 
		self.selection = StringVar(self)
		self.curr_filter = None        	            # The current filter. Setting it to None initially forces the first update.
		self.items = original_champion_names        # All of the items for the listbox.
		self.on_tick()	    			            # The initial update.

	def on_tick(self):
		if self.filter_box.get() != self.curr_filter:
			# The contents of the filter box has changed.
			self.curr_filter = self.filter_box.get()

			# Refresh the listbox.
			self.listbox.delete(0, 'end')

			for item in self.items:
				if self.curr_filter.lower() in item.lower():
					self.listbox.insert('end', item)

		self.after(250, self.on_tick)

	def make_image(self, image_name, image_data):
		with open(f'{image_name}', 'wb') as handler:
			data = requests.get(image_data['image']).content
			handler.write(data)

	def selected_item(self, *args):
		try:
			index = self.listbox.curselection()[0]
			self.selection = self.listbox.get(index)
			#print(self.selection)
			self.filter_box.delete(0, END)

			#print(f"{self.selection} | {self.champ_data['name']}")
			if self.selection == self.champ_data['name']:
				ctk.CTkLabel(self.mistakes_frame, text = 'You Won!', text_color = 'green', font=('Arial', 20, 'bold')).grid(row=2,column=0)
				self.submit_button.configure(state='disabled')

			else:
				champ_data = get_one_champ_image(self.selection)
				image_name = f"mistake_champ_img.png"
				
				if os.path.isfile(image_name): # if the file already exists it means we have to concat the next image next to the previous one
					im1 = Image.open(image_name)
					self.make_image('tmp.png', champ_data)
					im2 = Image.open('tmp.png')
					final = get_concat_h(im1,im2)
					final.save(image_name)
					img = ctk.CTkImage(light_image=final, dark_image=final, size=((self.mistakes_counter+1)*48, 48))
				else:							# if the file doesn't exist we create it
					self.make_image(image_name, champ_data)
					img = ctk.CTkImage(light_image=Image.open(image_name), dark_image=Image.open(image_name), size=(48, 48))

				idx = self.listbox.get(0, END).index(self.selection)
				self.listbox.delete(idx)

				self.champ_mistake_button = ctk.CTkButton(self.mistakes_frame, text='', state='disabled', fg_color = 'transparent', image = img).grid(row=1,column=0, padx = 2, pady = 20)

				self.mistakes_counter += 1
		except IndexError:
			print("Error did not pick champ, try again.")

if __name__ == "__main__":
	app = App()
	ctk.set_appearance_mode("dark")

	app.mainloop()
