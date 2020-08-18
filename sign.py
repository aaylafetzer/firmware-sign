#!/usr/bin/env python3

import argparse
from nacl import encoding, signing
import os

parser = argparse.ArgumentParser()
parser.add_argument('--key', help='location of signing key file, default ./keys/sign')
parser.add_argument('file', nargs='+', help='files to sign')
args = parser.parse_args()

if args.key is None:
    args.key = os.path.dirname(os.path.realpath(__file__)) + "/keys/sign"

sign_key_f = os.open(args.key, os.O_RDONLY)
sign_key_hex = os.read(sign_key_f, 64)
os.close(sign_key_f)

sign_key = signing.SigningKey(sign_key_hex, encoder=encoding.HexEncoder)

for arg in args.file:
    with open(arg, "rb") as f:
        signed = sign_key.sign(f.read())

    with open(arg + ".signed", "wb") as f:
        f.write(signed)
