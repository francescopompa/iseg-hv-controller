import pandas as pd
import numpy as np
import toml
def getNumberChannel(n):

    return n
ip = '192.168.1.16'
df = pd.read_csv('HV_settings.csv')
# do stuff
gains = [0.5 * i * 10**6 for i in range(1, 21)]
addresses=[f'0.{c//100}.{(c-(c//100))%16}' for c in df.HV]
header_dict = {'Server': {'ip': ip, 'port': '8080', 'username': 'admin', 'password': 'password'},
               'Defaults': {'voltage': 0, 'ramp_speed': 40, 'trip_current': 350e-6, 'power_status': True}}
header_dict_off = {'Server': {'ip': ip, 'port': '8080', 'username': 'admin', 'password': 'password'},
               'Defaults': {'voltage': 0, 'ramp_speed': 40, 'trip_current': 350e-6, 'power_status': False}}

for g in gains:
    with open(f'config_{g:.1e}.toml', mode='w') as f:
        toml.dump(header_dict, f)
        for i in range(48):
            address =f'0.{i//16}.{i%16}'
            int_address = int(i//16*100+i%16)

            voltage =np.array(df[f'V(G={g:.1e})'][df.HV == int_address])
            if len(voltage) == 0:
                voltage=0
            else:
                voltage=int(voltage[0])
            dict = {'addr':address,'voltage':voltage,'trip_current':350e-6,'power_status':True}
            f.write('\n')
            f.write(f'[Channels.{i+1}]\n')
            toml.dump(dict,f)

with open(f'config_matched.toml', mode='w') as f:
        toml.dump(header_dict, f)
        for i in range(48):
            address =f'0.{i//16}.{i%16}'
            int_address = int(i//16*100+i%16)

            voltage =np.array(df[f'V_f'][df.HV == int_address])
            if len(voltage) == 0:
                voltage=0
            else:
                voltage=int(voltage[0])
            
            dict = {'addr':address,'voltage':voltage,'trip_current':350e-6,'power_status':True}
            f.write('\n')
            f.write(f'[Channels.{i+1}]\n')
            toml.dump(dict,f)


with open(f'config_off.toml', mode='w') as f:
        toml.dump(header_dict_off, f)
        for i in range(48):
            address =f'0.{i//16}.{i%16}'
            int_address = int(i//16*100+i%16)

            voltage =0
            
            dict = {'addr':address,'voltage':voltage,'trip_current':350e-6,'power_status':False}
            f.write('\n')
            f.write(f'[Channels.{i+1}]\n')
            toml.dump(dict,f)


