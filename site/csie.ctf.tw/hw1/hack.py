#!/usr/bin/env python

from struct import *

with open('flag-ee94f5c9452a6db022db1e4f3a036b375b3ac472') as fd:
    data = fd.read()

data = unpack('<{}i'.format(len(data) / 4), data)

def encrypt(data):
    for idx, item in enumerate(data):
        tmp = (2 + idx) * 0xcccccccd
        D = tmp >> 32
        A = tmp & 0xffffffff
        D >>= 3
        A = D * 10
        C = (2 + idx - A) & 0xff
        D = idx + 1
        D <<= C
        print hex(ord(item) * D + 0x2333)
    return

def decrypt(data):
    ans = ''
    for idx, item in enumerate(data):
        tmp = (2 + idx) * 0xcccccccd
        D = tmp >> 32
        A = tmp & 0xffffffff
        D >>= 3
        A = D * 10
        C = (2 + idx - A) & 0xff
        D = idx + 1
        D <<= C
        ans += chr((item - 0x2333) / D)
    print ans
    return

decrypt(data)
