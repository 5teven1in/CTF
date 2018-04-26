#!/usr/bin/env python

import requests

url = 'http://sha1.pwn.seccon.jp/upload'

with open('shattered-1.pdf', 'rb') as fd:
    f1 = fd.read()

with open('shattered-2.pdf', 'rb') as fd:
    f2 = fd.read()

f1 += 'a' * 1642980
f2 += 'a' * 1642980

res = requests.post(url, files = {'file1' : f1, 'file2' : f2})
print res.text
