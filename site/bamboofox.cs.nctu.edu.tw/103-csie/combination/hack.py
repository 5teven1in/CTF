#!/usr/bin/env python

from pwn import *
import time

r = remote('bamboofox.cs.nctu.edu.tw', 10110)

def mysend(s):
    time.sleep(0.1)
    r.sendline(s)

mysend('1')
mysend('Software Debugging')
mysend('2')
mysend('10')
mysend('Playing CTF is funnier than writing a paper.')
mysend('7')
mysend('4')
mysend('5')
mysend('The problem is modified by BCTF 2014 crypto 100, thanks for blue-lotus.')

r.interactive()
