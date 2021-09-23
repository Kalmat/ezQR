arguments = {
    "Usage": "qr ARGUMENT FILE [-m MESSAGE]",
    "Values": {
        "-e": {"Name": "encode", "Help": "Encode message into QR"},
        "-d": {"Name": "decode", "Help": "Decode data from QR"}
    },
    "MinArg": 1,
    "MaxArg": 1,
    "MutExc": [["-e", "-d"]],
    "FreeArgs": True,
    "FreeArgsDesc": "file name",
    "MinFreeArgs": 1,
    "MaxFreeArgs": 1
}

options = {
    "Values": {
        "-m": {"Name": "message", "isFlag": False, "FreeValues": True, "NoContent": "Ignore", "Help": "Message to Encode/Decode"},
    },
    "MutExc": [],
    "RequiredIf": []
}

arg_opt = {
    "-d": {"Required": [], "RequiredIf": [], "MutExc": [], "Ignored": ["-m"]}
}
