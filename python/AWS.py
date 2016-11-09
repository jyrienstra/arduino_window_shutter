from tkinter import *

import serial, threading

class App():

    #constructor
    def __init__(self, port = 'COM3', baudrates = 19200):

        self.on = False

        self.port = port
        self.baudrates = baudrates
        self.averageTemp = tuple()

        # init een nieuwe TKinter instantie, zet deze in self.root, zodat hij in alle methodes gebruikt kan worden
        self.root = Tk()

        # Zet de titel van de window
        self.root.title('Arduino Window Shutter')

        # Zet de layout op de goede plek. Alle containers, inputs, buttons, etc. worden in deze method neergezet
        self.setlayout()
        # maak een nieuwe connectie aan met poort COM3, zodat een verbinding met de arduino mogelijk is
        # Als er geen arduino is aangesloten, wordt de except clause opgeroepen en wordt er een error laten zien

        self.initEverything()

        self.root.mainloop()
    # Layout van de window
    # return void

    def initEverything(self):
        if self.on:
            buttonstate = NORMAL

            # Tekstveld waar alle output van de arduino terecht komt
            Label(self.outputContainer, text='Temperatuur', background='white').grid(row=0, column=0)
            self.tempOut = Entry(self.outputContainer, width=30)
            self.tempOut.grid(row=0, column=1, pady=4)
            Label(self.outputContainer, text='Gemiddelde temperatuur', background='white').grid(row=1, column=0)

            Label(self.outputContainer, text='Lichtsterkte', background='white').grid(row=2, column=0, pady=4)
            self.lightOut = Entry(self.outputContainer, width=30)
            self.lightOut.grid(row=2, column=1, pady=4)

            self.initControlButtons(buttonstate)

            try:
                # Connectie met arduino
                # throws SeralException
                self.connection = serial.Serial(self.port, self.baudrates)

                # Lees de input vanaf de arduino
                self.readArduino()

                self.calculateAverage()
            except serial.SerialException:
                # TODO: create a global notification bar
                self.tempOut.insert(END, 'Can\'t connect to port {0}'.format(self.port))


        else:
            buttonstate = DISABLED
            self.connection = None
            self.outputContainer.destroy()
            self.controls.destroy()
            self.setlayout()
            self.initControlButtons(buttonstate)

    def initControlButtons(self, buttonstate):
        self.tempUpButon = Button(self.controls, text='Up', state=buttonstate, command=self.changeTemp('up'), width=10)
        self.tempUpButon.grid(row=2, column=0)

        Label(self.controls, text="Temperatuur", background='white').grid(row=3, column=0)

        self.tempDownButton = Button(self.controls, text="Down", state=buttonstate, command=self.changeTemp('down'),
                                     width=10)
        self.tempDownButton.grid(row=4, column=0, pady=(0, 16))

        self.lightUpButton = Button(self.controls, text="Up", state=buttonstate, command=self.changeLight('up'),
                                    width=10)
        self.lightUpButton.grid(row=2, column=1)

        Label(self.controls, text="Lichtintensiteit", background='white').grid(row=3, column=1)

        self.lightDownButton = Button(self.controls, state=buttonstate, text="Down", command=self.changeLight('down'),
                                      width=10)
        self.lightDownButton.grid(row=4, column=1, pady=(0, 16))

    def setlayout(self):

        # Frame voor de output
        self.outputContainer = Frame(height=5, width=200, background='white', borderwidth=1, relief='groove')
        self.outputContainer.pack(fill=Y, padx=5, pady=5, side=LEFT)


        #Frame voor de controls
        self.controls = Frame(height=200, width=200, background='white', borderwidth=1, relief='groove')
        self.controls.pack(fill=Y, padx=5, pady=5, side=RIGHT)

        #on button
        self.onButton = Button(self.controls, text="Aan", command=self.turnOn, width=10)
        self.onButton.grid(row=0, column=0, pady=(0, 16))

        #off button
        self.offButton = Button(self.controls, text="Uit", command=self.turnOff, width=10, state=DISABLED)
        self.offButton.grid(row=0, column=1, pady=(0, 16))

    def turnOn(self):
        if self.on:
            return

        self.on = True
        self.offButton['state'] = NORMAL
        self.onButton['state'] = DISABLED
        self.initEverything()

    def turnOff(self):
        if self.on:
            self.on = False
            self.offButton['state'] = DISABLED
            self.onButton['state'] = NORMAL
            self.initEverything()
        return

    def changeTemp(self, direction):
        print('Temp' + direction)

    def changeLight(self, direction):
        print('Light' + direction)

    #krijg alle output van de arduino binnen
    # return void
    def readArduino(self):

        while True and self.connection is not None:
            #lees de inkomende packets
            message = self.connection.read()

            self.averageTemp = self.averageTemp + (int(message.hex()),)
            #Laat de inkomende packets zien in hex-formaat, maar verwijder eerst de input
            self.tempOut.delete(0, END)
            self.tempOut.insert(END, '{0}\n'.format(message.hex()))

            #update de root
            self.root.update()

    def calculateAverage(self):
        if(len(self.averageTemp) > 0):
            all = 0
            for i in self.averageTemp:
                all = all + i
            print(all // len(self.averageTemp))
            self.averageTemp = tuple()

        threading.Timer(5, self.calculateAverage).start()

#Nieuwe instantie van app

if __name__ == "__main__":
    app = App()