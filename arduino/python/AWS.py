from tkinter import *
import serial

class App():

    #constructor
    def __init__(self, port = 'COM3', baudrates = 19200):

        #init een nieuwe TKinter instantie, zet deze in self.root, zodat hij in alle methodes gebruikt kan worden
        self.root = Tk()

        #Zet de titel van de window
        self.root.title('Arduino Window Shutter')

        #Zet de layout op de goede plek. Alle containers, inputs, buttons, etc. worden in deze method neergezet
        self.setlayout()

        #maak een nieuwe connectie aan met poort COM3, zodat een verbinding met de arduino mogelijk is
        #Als er geen arduino is aangesloten, wordt de except clause opgeroepen en wordt er een error laten zien
        try:
            #Connectie met arduino
            # throws SeralException
            self.connection = serial.Serial(port, baudrates)

            #Lees de input vanaf de arduino
            self.readArduino()
        except serial.SerialException:
            self.output.insert(END, 'Can\'t connect to port {0}'.format(port))
            self.output.pack()

        self.root.mainloop()
    #Layout van de window
    #return void
    def setlayout(self):

        #Frame voor de output
        outputContainer = Frame(height=5, width=200, background='white')
        outputContainer.pack(fill=Y, padx=5, pady=5, side=LEFT)

        #Tekstveld waar alle output van de arduino terecht komt
        self.output = Text(outputContainer, width=90)
        self.output.pack()

        #Frame voor de controls
        controls = Frame(height=200, width=200, background='blue')
        controls.pack(fill=Y, padx=5, pady=5, side=RIGHT)

    #krijg alle output van de arduino binnen
    # return void
    def readArduino(self):

        while True:
            #lees de inkomende packets
            message = self.connection.read()

            #Laat de inkomende packets zien in hex-formaat
            self.output.insert(END, '{0}\n'.format(message.hex()))

            #update de root
            self.root.update()

#Nieuwe instantie van app

if __name__ == "__main__":
    app = App()