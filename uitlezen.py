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

# argument: 'mock=true' -> show mock data + neat formatting
# argument: 'mock=false' -> show real data + formatting

mock = (sys.argv[1] == "mock=true")

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
else:
  mock_data = [
    "/XMX5LGBBLA4415333325",
    "",
    "1-3:0.2.8(50)",
    "0-0:1.0.0(190224214937W)",
    "0-0:96.1.1(4530303435303034303237373133343137)",
    "1-0:1.8.1(000448.180*kWh)",
    "1-0:1.8.2(000491.421*kWh)",
    "1-0:2.8.1(000000.000*kWh)",
    "1-0:2.8.2(000000.000*kWh)",
    "0-0:96.14.0(0001)",
    "1-0:1.7.0(00.248*kW)",
    "1-0:2.7.0(00.000*kW)",
    "0-0:96.7.21(00009)",
    "0-0:96.7.9(00006)",
    "1-0:99.97.0(6)(0-0:96.7.19)(180514151900S)(0000009430*s)(180514183631S)(0000000602*s)(181006153411S)(0000005679*s)(181006154404S)(0000000225*s)(181006171105S)(0000001908*s)(181006173340S)(0000000822*s)",
    "1-0:32.32.0(00003)",
    "1-0:32.36.0(00000)",
    "0-0:96.13.0()",
    "1-0:32.7.0(224.0*V)",
    "1-0:31.7.0(001*A)",
    "1-0:21.7.0(00.248*kW)",
    "1-0:22.7.0(00.000*kW)",
    "0-1:24.1.0(003)",
    "0-1:96.1.0(4730303332353635353239353139303137)",
    "0-1:24.2.1(190224214510W)(00112.770*m3)",
    "!BA4E"
  ]

#Initialize
p1_teller = 0

while True and (p1_teller < len(mock_data)):
    p1_line=''

    if (not mock):
      #Read 1 line van de seriele poort
      try:
          p1_raw = ser.readline()
      except:
          sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )
    else:
      p1_raw = mock_data[p1_teller]
        
    p1_str=str(p1_raw)
    p1_line=p1_str.strip()
    print (p1_)
    
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
if (not mock):
  try:
      ser.close()
  except:
      sys.exit ("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % ser.name )      