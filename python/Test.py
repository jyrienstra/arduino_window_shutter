from tkinter import *

class App():
    def __init__(self):
        self.root = Tk()

        Button(self.root, text="Aan", command=lambda: self.power('on'), width=10).pack()
        Button(self.root, text="Off", command=self.powerOff, width=10).pack()

        self.root.mainloop()

    def power(self, state):
        print(state, " deze is zonder klikken ")

    def powerOff(self):
        print('powered off deze is met klikken')

app = App()