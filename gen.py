#!/usr/bin/env python3

import htb  # Just pip install this bad boy
import dotenv
import os
import sys
from pathlib import Path
import shutil

API_KEY = dotenv.get_key('.env','API_KEY')
HTB_DIR = dotenv.get_key('.env','HTB_DIR')
TEMP_LOC = dotenv.get_key('.env','TEMP_LOC')

def get_vars(mid):
    hapi = htb.HTB(API_KEY)
    info= hapi.get_machine(mid)
    print('Box Information Received')
    return info


def gen_dirs(host):
    dirs = {'Files': ['Scans', 'Screenshots'], 'Writeup': ['en', 'es', 'jp']}
    mk = []
    base = HTB_DIR+'/'+host
    Path(base).mkdir(exist_ok=True)
    os.chdir(base)
    for key in dirs:
        for val in dirs[key]:
            mk.append(key+'/'+val)
    for _ in mk:
        Path(_).mkdir(parents=True, exist_ok=True)
        if _.startswith('Writeup'):
            shutil.copyfile(TEMP_LOC, _+'/'+host+'-'+_[-2:]+'.tex')
    print('Directories Created')
    return(''.join([_ for _ in mk if _.endswith('Scans')]))


def gen_rep(scans, info):
    os.chdir(HTB_DIR+'/'+info['name']+'/'+scans)
    os.system('sudo echo {} {} >> /etc/hosts'.format(info['ip'], info['name'].lower()+'.htb'))
    with open('Information', 'w+') as file:
        for key in info:
            file.write(key+' - '+str(info[key])+'\n')
        file.close()
    print('Scanning the host')
    os.system('sudo nmap -sS -sC -sV --script vuln {} > {}'.format(info['ip'], info['name'].lower()+'-scan'))
    print('All done!')


def main():
    info = get_vars(sys.argv[-1])
    scans = gen_dirs(info['name'])
    gen_rep(scans, info)


main()
