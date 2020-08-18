#!/usr/bin/env python3

import argparse
from nacl import signing, encoding
import os

parser = argparse.ArgumentParser()
parser.add_argument('--key', help='location of verifying key file, default ./keys/verify')
parser.add_argument('file', nargs='+', help='files to verify')
args = parser.parse_args()

if args.key is None:
    args.key = os.path.dirname(os.path.realpath(__file__)) + "/keys/verify"

verify_key_f = os.open(args.key, os.O_RDONLY)
verify_key_hex = os.read(verify_key_f, 64)
os.close(verify_key_f)

verify_key = signing.VerifyKey(verify_key_hex, encoder=encoding.HexEncoder)

for arg in args.file:
    with open(arg, "rb") as f:
        verified = verify_key.verify(f.read())

    with open(arg + ".verified", "wb") as f:
        f.write(verified)
