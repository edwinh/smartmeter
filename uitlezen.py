# DSMR v4.2 p1 uitlezen
# (c) 10-2012 - 2016 GJ - gratis te kopieren en te plakken
versie = "1.1"
import sys
import serial


##############################################################################
#Main program
##############################################################################
print ("DSMR P1 uitlezen",  versie)
print ("Control-C om te stoppen")

#Set COM port config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

#Open COM port
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s. Aaaaarch."  % ser.name)      


#Initialize
#p1_teller is mijn tellertje voor van 0 tot 36 te tellen
p1_teller  = 0

while True: #not last_line: #p1_teller < 26:
    p1_line=''
    #Read 1 line van de seriele poort
    try:
        p1_raw = ser.readline()
    except:
        sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )
    
    
    p1_str=str(p1_raw)
    p1_line=p1_str.strip()
    
    # date/time
    if (p1_line.startswith("0-0:1.0.0")):
      print("Datum/tijd: " + p1_line)
    
    # Meter 1
    if (p1_line.startswith("1-0:1.8.1")):
      start_actual = p1_line.find("(")
      end_actual = p1_line.find("*")
      meter1_value = float(p1_line[start_actual+1:end_actual])
      print("Meter 1: " + str(meter1_value) + " kWh")

    # Meter 2
    if (p1_line.startswith("1-0:1.8.2")):
      start_actual = p1_line.find("(")
      end_actual = p1_line.find("*")
      meter2_value = float(p1_line[start_actual+1:end_actual])
      print("Meter 2: " + str(meter2_value) + " kWh")

    # Actual
    if (p1_line.startswith("1-0:1.7.0")):
      start_actual = p1_line.find("(")
      end_actual = p1_line.find("*")
      actual_value = int(p1_line[start_actual+1:end_actual].replace('.', ''))
      print("Actual: " + str(actual_value) + " Watt")
    
    #print ("Line " + str(p1_teller) + ": " + p1_line)
    p1_teller += 1

#Close port and show status
try:
    ser.close()
except:
    sys.exit ("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % ser.name )      