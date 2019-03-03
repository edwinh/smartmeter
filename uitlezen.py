# DSMR v4.2 p1 uitlezen
# (c) 10-2012 - 2016 GJ - gratis te kopieren en te plakken
versie = "1.1"
import sys
import serial
from datetime import datetime
import extract_telegram

def read_mock_data():
  p1_teller = 0
  while (p1_teller < len(extract_telegram.mock_data)):
    p1_line=''
    p1_line = extract_telegram.mock_data[p1_teller]
    result = extract_telegram.decode_line(p1_line)
    if result != None:
      print (result)
    
    p1_teller += 1
  return

def read_live_data():
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
  telegram_length = 26

  #Open COM port
  try:
      ser.open()
  except:
      sys.exit ("Fout bij het openen van %s. Aaaaarch."  % ser.name)

  #Initialize
  p1_teller = 0
  done = False
  first_line_read = False

  while not done:
      p1_line=''

      #Read 1 line van de seriele poort
      try:
          p1_raw= ser.readline()
          p1_str=str(p1_raw)
          p1_line=p1_str.strip()
      except:
          sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )

      first_line_read = first_line_read or (len(p1_line) > 0 and p1_line[0] == '/')
      print(first_line_read)
      result = extract_telegram.decode_line(p1_line)
      if result != None:
        print (result)

      done = (first_line_read and len(p1_line) > 0 and p1_line[0] == '!')
  return

def main():
  ##############################################################################
  #Main program
  ##############################################################################
  print ("DSMR P1 uitlezen",  versie)
  print ("Control-C om te stoppen")

  # argument: 'mock=true' -> show mock data + neat formatting
  # argument: 'mock=false' -> show real data + formatting
  if (len(sys.argv) > 1):
    mock = (sys.argv[1] == "mock=true")
  else:
    mock = True

  if mock:
    read_mock_data()
  else:
    read_live_data()

  return
  
  if (not mock):
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
  p1_teller = 0

  while (p1_teller < len(extract_telegram.mock_data)):
      p1_line=''

      if (not mock):
        #Read 1 line van de seriele poort
        try:
            p1_raw= ser.readline()
            p1_str=str(p1_raw)
            p1_line=p1_str.strip()
        except:
            sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )
      else:
        p1_line = extract_telegram.mock_data[p1_teller]

      result = extract_telegram.decode_line(p1_line)
      if result != None:
        print (result)
      
      if mock:
        p1_teller += 1

  #Close port and show status
  if (not mock):
    try:
        ser.close()
    except:
        sys.exit ("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % ser.name )

#line = "0-0:1.0.0(190224214937W)"
#print (decodeTelegram(line))
main()

