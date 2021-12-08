from tkinter import *


def main():
	master = Tk()
	Label(master, text="Choose the service which you want to use from the given options").grid(row=0)
	
	def Server():
		master.quit()
		import ServerReceive
		
	def Client():
		master.quit()
		import ClientSend
		
	Button(master, text='Server', command=Server).grid(row=3, column=0, sticky=W, pady=4)
	Button(master, text='Client', command=Client).grid(row=5, column=0, sticky=W, pady=4)
		
	master.mainloop()
	
	
if __name__ == "__main__":
	main()