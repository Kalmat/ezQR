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
from pathlib import Path, PurePath
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
import clparser
from cloptions import *


def check_file(file, extension="", find_alt=False):

    file = file.rstrip("\\").rstrip("/")
    dir_name, file_name = os.path.split(file)
    short_name, file_ext = os.path.splitext(file_name)

    valid_path = True
    if dir_name:
        if Path(dir_name).is_dir():
            dir_name += os.sep
        else:
            dir_name = ""
            valid_path = False

    if (extension and file_ext.lower() != extension.lower()) or not file_ext:
        file_ext += extension

    file_name = "{}{}{}".format(dir_name, short_name, file_ext)

    is_file = Path(file_name).is_file()
    is_dir = Path(file_name).is_dir()

    if find_alt:
        i = 1
        while Path(file_name).is_file() or Path(file_name).is_file():
            file_name = PurePath(file_name).with_name("{}{}_{}{}".format(dir_name, file_name, i, file_ext))
            i += 1

    return file_name, is_dir, is_file, valid_path


def get_params():

    option = file = message = ""

    args, args_names, args_values, opts, opt_values = clparser.read_command_line(sys.argv, arguments, options, arg_opt)
    argument = args_names[0]

    if len(opts) >= 1:
        option = opts[0]

    if argument == "encode":
        file, _, _, valid_path = check_file(args_values[0], extension="png", find_alt=True)

        if not valid_path:
            print("WARNING: wrong path. Writing output file %s to current directory" % file)

        if option == "-m":
            message = " ".join(opt_values[0])
        else:
            print("Enter (or paste) your message:")
            message = input("")

    elif argument == "decode":
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

    if option == "encode":
        qr_encode(message, file)

    elif option == "decode":
        print(qr_decode(file))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        exit()
