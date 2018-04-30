#!/usr/bin/env python

from pwn import *
import string
import os

with open('ans') as fd:
    ans = fd.read()

def gen_ans(data):
    os.system('echo \'{}\' | ./hw1 '.format(data))
    with open('flag') as fd:
        res = fd.read()
    return res

test_ans = 'FLAG{'

for k in xrange(33):
    for i in string.printable:
        if ans.startswith(gen_ans(test_ans + i)):
            test_ans += i
            break

print test_ans
