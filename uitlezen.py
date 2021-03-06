# DSMR v4.2 p1 uitlezen
# (c) 10-2012 - 2016 GJ - gratis te kopieren en te plakken
versie = "1.1"
import sys
import serial
from datetime import datetime
import extract_telegram
import json
import requests
import time

def read_mock_data():
  p1_teller = 0
  telegram = []
  while (p1_teller < len(extract_telegram.mock_data)):
    p1_line=''
    p1_line = extract_telegram.mock_data[p1_teller]
    result = extract_telegram.decode_line(p1_line)
    if result != None:
      telegram.append(result)
    
    p1_teller += 1
  return telegram

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

  #Open COM port
  try:
    ser.open()
  except:
    sys.exit ("Fout bij het openen van %s. Aaaaarch."  % ser.name)

  #Initialize
  done = False
  first_line_read = False
  telegram = []
  
  while not done:
      p1_line=''

      #Read 1 line van de seriele poort
      try:
          p1_line = str(ser.readline()).strip()
          # Remove b' from beginning and \r\n from the end of the line
          p1_line = p1_line[2:-5]
      except:
          sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )
      first_line_read = first_line_read or (len(p1_line) > 0 and p1_line[0] == '/')
      if first_line_read:
        result = extract_telegram.decode_line(p1_line)
        if result != None:
          telegram.append(result)

      done = (first_line_read and len(p1_line) > 0 and p1_line[0] == '!')

  try:
        ser.close()
  except:
      sys.exit ("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % ser.name )
  return telegram

def main():
  ##############################################################################
  #Main program
  # argument: 'mock=true' -> show mock data + neat formatting
  # argument: 'mock=false' -> show real data + formatting
  ##############################################################################
  if (len(sys.argv) > 1):
    mock = (sys.argv[1] == "mock=true")
  else:
    mock = True

  if mock:
    result = read_mock_data()
  else:
    result = read_live_data()

  json_dict = {}
  for i in range(0,len(result)):
    linetype = result[i][0]
    if linetype == "dt":
      json_dt = result[i][2].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
      json_dict[result[i][0]] = json_dt
    if linetype == "kwh_c1" or linetype == "kwh_c2":
      json_dict[result[i][0]] = float(result[i][2])
  
  print (json_dict)
  ##headers = {
  #      'Content-Type': 'application/json'}
  #response = requests.post("http://127.0.0.1:5000/electricity", headers = headers, data = json.dumps(json_dict))
  #print (response.status_code, response)


  
  return

while True:
  main()
  time.sleep(5)