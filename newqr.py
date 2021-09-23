#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

"""
********* QR TOOL by alef (Paython 3) ********* 
This is a very simple tool to encode/decode QR codes (.png only)

SUGGESTION: Could be fun to interchange messages with friends using QRs
            or passwords for ciphered messages created with CRYPTO TOOL!!!

*** USAGE: qr OPTION FILE
    OPTIONS:
          -e    Encode message to QR
          -d    Decode message from QR
"""

import sys
import os
from pathlib import Path,PurePath
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import clparser
from cloptions import *

ENCODE="encode"
DECODE="decode"
EXT_OK="png"
M="-m"

def decorator(function):    
    def wrapper(*args,**kwargs):
        import time
        init=time.time()
        outcome=function(*args,**kwargs)
        end=time.time()
        print("<time_execution> {:f}".format(end - init))
        return outcome
    return wrapper

def getNameFile(file_name):
    ''' genera un nuevo nombre de fichero en path si existe'''   
    _myPurePath=PurePath(file_name) 
    _nameFile=_myPurePath.stem
    _extension=_myPurePath.suffix
        
    i=1        
    while Path(file_name).is_file():
        file_name=PurePath(file_name).with_name("{}({}){}".format(_nameFile,i,_extension)).as_posix()        
        i+=1
    return file_name

@decorator
def check_file(file_name):
    
    _nameDir,_nameFile=os.path.split(file_name)    
    _shortName,_extension=os.path.splitext(_nameFile)

    if not _extension.lower() == EXT_OK:  #tratamiento extension        
        _extension=EXT_OK
        
    if not _nameDir: # sino informa directorio asignamos directorio de trabajo
        _nameDir=os.getcwd()

    _tempNameFile="{}\{}.{}".format(_nameDir,_shortName,_extension)    
    return getNameFile(_tempNameFile)     

def get_params():

    option = file = message =""
 
    args, args_names, args_values, opts, opt_values = clparser.read_command_line(sys.argv, arguments, options, arg_opt)
    
    argument = args_names[0]
    if len(opts) >= 1:
        option = opts[0]

    if argument == ENCODE:
        file = check_file(args_values[0])

        if option == M and len(opt_values[0]):   #tratamos mensaje cuando informa parm -m e informa mensaje       
            message=" ".join(opt_values[0])
        else:
            print("Enter (or paste) your message:")
            message = input("")

    elif argument == DECODE:
        file = args_values[0]
        if not os.path.isfile(file):
            print("ERROR: QR file not found or is a directory")
            exit()
        elif ".png" not in file:
            print("ERROR: QR file must be .png")
            exit()

    else:
        exit()

    return argument, file, message


def qr_encode(data, file):
    img = qrcode.make(data)
    img.save(file, "PNG")
    return

def qr_decode(file):
    qr = decode(Image.open(file))
    data = ""
    for bc in qr:
        data = bc.data.decode()
    return data


def main():
    option, file, message = get_params()

    if option == ENCODE:
        qr_encode(message, file)

    elif option == DECODE:
        print(qr_decode(file))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        exit()
