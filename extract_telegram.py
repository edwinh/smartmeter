import re
from datetime import datetime

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

telegram_translation = {
    "0-0:1.0.0": {'id': 'dt', 'title': 'Date/time', 'show': True, 'function': 'extract_dt'},
    "0-0:96.1.1": {'id': 'kwh_equip', 'title':"Equip ID", 'show':False},
    "1-0:1.8.1": {'id': 'kwh_c1', 'title':"kWh meter 1", 'show':True},
    "1-0:1.8.2": {'id': 'kwh_c2', 'title':"kWh meter 2", 'show':True},
    "1-0:2.8.1": {'id': 'kwh_r1', 'title':"kWh meter 1 received", 'show':False},
    "1-0:2.8.2": {'id': 'kwh_r2', 'title':"kWh meter 2 received",'show':False},
    "0-0:96.14.0": {'id': 'tariff_ind', 'title':"Tariff indicator", 'show':True},
    "1-0:1.7.0": {'id': 'curr_power_c', 'title':"Current power consumed", 'show':True},
    "1-0:2.7.0": {'id': 'curr_power_r', 'title':"Current power received", 'show':False},
    "0-0:96.7.21": {'id': 'short_power_fail', 'title':"Short Power failures", 'show':False},
    "0-0:96.7.9": {'id': 'long_power_fail', 'title':"Long Power failures", 'show':False},
    "1-0:99.97.0": {'id': 'power_fail_log', 'title':"Power failures log", 'show':False},
    "1-0:32.7.0": {'id': 'volt', 'title':"Voltage",'show':False},
    "0-1:96.1.0": {'id': 'gas_equip', 'title':"Gas equip ID", 'show':False},
    "0-1:24.2.1": {'id': 'm3_dt', 'title':"Gas m3 reading", 'show':True, 'function': 'extract_dt'}
  }

def extract_dt(dt_string):
  dt_string = dt_string[:-1]
  return datetime.strptime(dt_string, '%y%m%d%H%M%S')

def decode_line(line):
  if len(line) == 0:
    return
  values = re.split('[()*]', line)
  values = list(filter(None, values))
  if values[0] in telegram_translation and telegram_translation[values[0]]['show']:
    values.insert(0, telegram_translation[values[0]]['title'])
    if 'function' in telegram_translation[values[1]]:
      # Execute function, add it to dict and delete input value from dict
      values.append(globals()[telegram_translation[values[1]]['function']](values[2]))
      del(values[2])
    values.insert(0, telegram_translation[values[1]]['id'])
    del(values[2])
    return values

#for i in range(0,len(mock_data)):
#  decode_line(mock_data[i])
#print(telegram_translation['0-0:1.0.0']['title'])
  