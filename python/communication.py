# Om data van C naar Python over te brengen via uart kunnen we net zoals realterm een poort en baudrates opgeven voor python.
# Hiervoor gebruiken we PySerial. Dit is een externe library.

### Quick install ###
# pip install pyserial

### Meer informatie ###
# Github: https://github.com/pyserial/pyserial
# PyPI: https://pypi.python.org/pypi/pyserial

# Importeer de serial library
import serial

# Uit de serial library, gebruik de Serial class. Vervang COM3 voor de poort in jouw pc. 19200 zijn de baudrates.
# Voor meer informatie over de Serial class en de constructor zie: http://pyserial.readthedocs.io/en/latest/pyserial_api.html?highlight=serial
ser = serial.Serial('COM3', 19200)

# Infinite loop om de data voor altijd op te blijven halen
while True:
	s = ser.read()	# read() method uit de Serial class. Returns byte object
	print(s.hex())	# Convert de byte object naar een hex
