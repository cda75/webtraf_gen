# -*- coding: utf-8 -*-
import subprocess
from datetime import datetime

#URL list
workDir = '/home/cda/webtraf_gen/logs/'
logFile = f'{workDir}access.log'
cpGw = '10.10.100.251'
ugGw = '10.10.100.252'
gwList = [cpGw, ugGw]


def logging(log_text, title=False):
    time = datetime.today().strftime('%d.%m.%Y %H:%M')
    log_text = f'\n{log_text}\n' if title else f'\n{time}\t{log_text}\n'
    with open(logFile, 'a') as f:
        f.write(log_text)


def get_default_gw():
    p = subprocess.Popen(['ip', 'route'], stdout = subprocess.PIPE) 
    output = str(p.communicate()) 
    default_gw = output.split()[2]
    return default_gw 


def get_new_gw():
    current_gw = get_default_gw()
    new_gw = [gw for gw in gwList if gw != current_gw][0]
    return new_gw


def change_default_gw():
    current_gw = get_default_gw()
    new_gw = get_new_gw()
    try:
        subprocess.call('ip route del default', shell=True)
        subprocess.call(f'ip route add default via {new_gw}', shell=True)
        logging(f'Changing default gateway to {new_gw}', True)
    except Exception:
        logging(f'Error changing default gateway from {current_gw}')


    
def main():
    change_default_gw()
    
        
  
if __name__== "__main__":
  main()
