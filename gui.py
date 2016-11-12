from Tkinter import *
import webscraper

class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        """
        self.SEMESTER = Entry(self)
        self.SEMESTER["text"] = "QUIT"
        self.SEMESTER["fg"]   = "red"
        self.SEMESTER["command"] = webscraper.__main__()

        self.SEMESTER.pack({"side": "left"})

        """
        self.but = Button(self)
        self.but["text"] = "Create Database",
        if __name__ == '__main__':
            self.but["command"] = webscraper.__main__()

        self.but.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()