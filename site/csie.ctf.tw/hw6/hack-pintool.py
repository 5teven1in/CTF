#!/usr/bin/env python

import os
import string

def try_one(ans, c):
    os.system('echo \'{}\' | ../../../pin -t obj-intel64/inscount0.so -- ./break > /dev/null 2>&1'.format(ans + c))
    with open('inscount.out') as fd:
        f = fd.read()
    return int(f.split()[1])

ans = ''

for i in xrange(75):
    cnt = 0
    ch = ''
    for c in string.printable:
        tmp = try_one(ans, c)
        if tmp > cnt:
            cnt = tmp
            ch = c
    ans += ch
    print ans
