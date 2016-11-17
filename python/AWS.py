from tkinter import *

import serial

class App():

    #constructor
    def __init__(self, port='COM3', baudrates=19200):

        """
        @var {bool} on Laat zien of het programma aan of uit staat.
        """
        self.on = False

        """
        var {String} port De poort waar de Serial connectie op loopt. Standaardwaarde is COM3
        """
        self.port = port

        """
        var {int} boudrates De boudrates waar de Serial connectie op loopt. Standaardwaarde is 19200
        """
        self.baudrates = baudrates

        """
        var {array} averageTemp De lijst met temperaturen waar het gemiddelde over wordt berekend
        """
        self.averageTemp = []

        """
        var {int} temperatuurDrempel De drempel qua temperatuur waarop het scherm in of uitrold. Als deze drempel overschreden wordt rolt het scherm uit, anders in.
        """
        self.temperatuurDrempel = 15

        """
        var {int} lichtDrempel De drempel qua lichtfelheid (lux) waarop het scherm in of uitrold. Als deze drempel overschreden wordt rolt het scherm uit, anders in.
        """
        self.lichtDrempel = 40

        """
        var {Tk} root Een nieuwe TKinter instantie. Deze vormt de basis voor het hele programma. Alle componenten (teksten, buttons, etc.) worden in deze instantie gezet.
        """
        self.root = Tk()

        # Zet de titel van het programma
        self.root.title('Arduino Window Shutter')

        # Zet de layout op de goede plek. Er wordt hier nog (nauwelijks) gekeken naar de inhoud, maar de indeling wordt gemaakt in deze functie
        self.setlayout()

        # Alle compontente (teksten, entries, buttons, etc.) worden in deze functie neergezet.
        self.initEverything()

        # Begin met het maken van het design.
        self.root.mainloop()

    def initEverything(self):
        """
        Alle compontente (teksten, entries, buttons, etc.) worden in deze functie neergezet.

        return {void}
        """
        if self.on:
            buttonstate = NORMAL

            # Tekstveld waar alle output van de arduino terecht komt
            Label(self.outputContainer, text='Temperatuur', background='white').grid(row=0, column=0)
            self.tempOut = Entry(self.outputContainer, width=30, state=DISABLED)
            self.tempOut.grid(row=0, column=1, pady=4)

            Label(self.outputContainer, text='Gemiddelde temperatuur', background='white').grid(row=1, column=0)
            self.averageTempOut = Entry(self.outputContainer, width=30, state=DISABLED)
            self.averageTempOut.grid(row=1, column=1)

            Label(self.outputContainer, text='Lichtsterkte', background='white').grid(row=2, column=0, pady=4)
            self.lightOut = Entry(self.outputContainer, width=30, state=DISABLED)
            self.lightOut.grid(row=2, column=1, pady=4)

            Label(self.outputContainer, text="Scherm uitgerold", background='white').grid(row=3, column=0, pady=4)
            self.rolledOut = Entry(self.outputContainer, width=30, state=DISABLED)
            self.rolledOut.grid(row=3, column=1, pady=4)

            Label(self.outputContainer, text="Inrollen scherm bij temperatuur:", background='white').grid(row=4, column=0, pady=4)
            self.tempVeld = Entry(self.outputContainer, width=30, state=DISABLED)
            self.tempVeld.grid(row=4, column=1, pady=4)

            Label(self.outputContainer, text="Inrollen scherm bij lichtintensiteit", background='white').grid(row=5, column=0, pady=4)
            self.lichtVeld = Entry(self.outputContainer, width=30, state=DISABLED)
            self.lichtVeld.grid(row=5, column=1, pady=4)

            # Zet de knoppen goed. Dit moet in een aparte functie om leesbaarheid te voorkomen.
            # Tevens hoeft er hierdoor geen codes dubbel geschreven te worden (omdat deze functie in de else-statement ook voorkomt)
            self.initControlButtons(buttonstate)

            try:
                # Connectie met arduino via Serial
                self.connection = serial.Serial(self.port, self.baudrates, timeout=0.5)


                # Lees de input vanaf de arduino
                self.readArduino()

            except serial.SerialException:
                self.tempOut['state'] = NORMAL
                self.tempOut.delete(0, END)
                self.tempOut.insert(END, 'Kan niet met poort {0} verbinden'.format(self.port))
                self.tempOut['state'] = DISABLED
                self.initControlButtons(DISABLED)


        else:
            buttonstate = DISABLED
            self.connection = None
            self.outputContainer.destroy()
            self.controls.destroy()
            self.setlayout()
            self.initControlButtons(buttonstate)

    def initControlButtons(self, buttonstate):
        """
        Zorgt ervoor dat de knoppen goed staan en in hun goede staat. Deze staat kan NORMAL en DISABLED zijn

        param {const} buttonstate De staat van de buttons. NORMAL: de knoppen zijn actief | DISABLED: de knoppen zijn niet actief
        return {void}
        """
        self.tempUpButon = Button(self.controls, text='Omhoog', state=buttonstate, command=lambda: self.changeTemp('up'), width=10)
        self.tempUpButon.grid(row=2, column=0)

        Label(self.controls, text="Temperatuur", background='white').grid(row=3, column=0)

        self.tempDownButton = Button(self.controls, text="Naar beneden", state=buttonstate, command=lambda: self.changeTemp('down'), width=10)
        self.tempDownButton.grid(row=4, column=0, pady=(0, 16))

        self.lightUpButton = Button(self.controls, text="Omhoog", state=buttonstate, command=lambda: self.changeLight('up'),width=10)
        self.lightUpButton.grid(row=2, column=1)

        Label(self.controls, text="Lichtintensiteit", background='white').grid(row=3, column=1)

        self.lightDownButton = Button(self.controls, state=buttonstate, text="Naar beneden", command=lambda: self.changeLight('down'), width=10)
        self.lightDownButton.grid(row=4, column=1, pady=(0, 16))

    def setlayout(self):

        """
        Zet de layout op de goede plek. Er wordt hier nog (nauwelijks) gekeken naar de inhoud, maar de indeling wordt gemaakt in deze functie

        return {void}
        """
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
        """
        Zet het programma aan

        return {void}
        """

        if self.on:
            return

        self.on = True
        self.offButton['state'] = NORMAL
        self.onButton['state'] = DISABLED
        self.initEverything()
        self.roll('down')

    def turnOff(self):
        """
        Zet het programma uit

        return {void}
        """

        if self.on:
            self.on = False
            self.offButton['state'] = DISABLED
            self.onButton['state'] = NORMAL
            self.initEverything()
            self.roll('up')
        return

    def roll(self, direction):
        """
        Zend naar de module of het zonnescherm in- of uitgerold moet worden

        todo: zend het naar de module via Serial
        """
        pass

    def changeTemp(self, direction):
        """
        Pas de temperatuur aan zodat het zonnescherm in- of uitgerold wordt bij een andere temperatuurinstelling

        todo: zend het naar de module via Serial
        return {void}
        """
        if direction == "up":
            self.temperatuurDrempel += 1
        elif direction == "down":
            self.temperatuurDrempel -= 1

        #self.connection.write(1)

        self.tempVeld['state'] = NORMAL
        self.tempVeld.delete(0, END)
        self.tempVeld.insert(END, '{0} graden'.format(self.temperatuurDrempel))
        self.tempVeld['state'] = DISABLED

    def changeLight(self, direction):
        """
        Pas de lichtfelheid aan zodat het zonnescherm in- of uitgerold wordt bij een andere instelling

        todo: zend het naar de module via Serial
        return {void}
        """
        if direction == "up":
            self.lichtDrempel += 1
        elif direction == "down":
            self.lichtDrempel -= 1

        #self.connection.write(2)

        self.lichtVeld['state'] = NORMAL
        self.lichtVeld.delete(0, END)
        self.lichtVeld.insert(END, '{0} zonnescheid (lux)'.format(self.lichtDrempel))
        self.lichtVeld['state'] = DISABLED

    #krijg alle output van de arduino binnen
    # return void
    # TODO: kijken wanneer rolluik open is; hoe ver hij open is;
    def readArduino(self):
        """
        Leest in een loop of er iets vanaf de module via Serial komt. Dit gebeurt net zo lang dat self.connection niet None is. Dit gebeurd als de connectie gestopt is.
        """
        while True and self.connection is not None:

            # bereken de gemiddelde temperatuur
            self.calculateAverage()
            # lees de inkomende packet
            message = self.connection.read()

            #Laat de inkomende packets zien in hex-formaat, maar verwijder eerst de input
            try:
                # converteer datgene wat er binnenkomt naar een integer. Dit gebeurt altijd omdat de input eerst naar een hex-formaat geconverteerd wordt.
                input = int(message.hex(), 16)

                if self.checkinput(input) == 'temp':
                    self.averageTemp.append(self.convertinput(input))
                    # print(self.averageTemp)
                    self.tempOut['state'] = NORMAL
                    self.tempOut.delete(0, END)
                    self.tempOut.insert(END, '{0}\n graden'.format(self.convertinput(input)))
                    self.tempOut['state'] = DISABLED
                elif self.checkinput(input) == 'distance':
                    self.rolledOut['state'] = NORMAL
                    self.rolledOut.delete(0, END)
                    self.rolledOut.insert(END, '{0}\n cm'.format(self.convertinput(input)))
                    self.rolledOut['state'] = DISABLED
                elif self.checkinput(input) == 'status':
                    self.rolledOut['state'] = NORMAL
                    self.rolledOut.delete(0, END)
                    if self.convertinput(input) == 1:
                        status = "uitgerold"
                    elif self.convertinput(input) == 2:
                        status = "ingerold"
                    self.rolledOut.insert(END, '{0}'.format(status))
                    self.rolledOut['state'] = DISABLED
            except:
                pass

            #update de root, zodat het scherm interactief blijft
            self.root.update()

    def checkinput(self, input):
        """
        Check de input op wat voor waarde deze weergeeft. Er zijn drie mogelijke waarden: 1: afstand van de ultrasonoor | 2: temperatuur | 3: status van het zonnescherm (in- of uitgerold)
        Deze input komt binnen via Serial

        param {int} input De input vanuit Serial
        return {String} distance | temp | status
        """
        input = [int(i) for i in str(input)]

        if input[0] == 1:
            return 'distance'
        elif input[0] == 2:
            return 'temp'
        elif input[0] == 3:
            return 'status'

    def convertinput(self, input):
        """
        Haal het cijfer weg die laat zien wat voor input het is. (zie checkinput())

        param {int} input De input vanuit Serial
        return {int} De input vanuit Serial zonder het eerste cijfer
        """
        input = [i for i in str(input)]
        del input[0]
        return int(''.join(input))


    def calculateAverage(self):
        """
        Berekent de gemiddelde temperatuur om de 40 seconden. Er wordt gekeken naar de array averageTemp waar elke seconde een nieuwe waarde ingevoegd wordt.
        Als de lengte van deze array 40 is, zijn er dus 40 seconden verstreken.

        return {void}
        """
        if(len(self.averageTemp) == 40):
            self.connection.write(15)
            all = 0
            for i in self.averageTemp:
                all = all + i

            self.averageTempOut['state'] = NORMAL
            self.averageTempOut.delete(0, END)
            self.averageTempOut.insert(END, '{0}\n graden'.format((all // len(self.averageTemp))))
            self.averageTemp = []
            self.averageTempOut['state'] = DISABLED

# Maak de app
if __name__ == "__main__":
    app = App('COM3')
