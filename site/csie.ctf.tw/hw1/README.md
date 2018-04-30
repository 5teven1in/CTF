hw1
===

## hw1

### concept

- normal work
    - 讀懂組語中加密函式的行為後便可以反向解出被加密的 flag

![](https://i.imgur.com/q3Egxm4.png)

- dirty work
    - 觀察到該程式是每次加密一個 byte，且每個 byte 互相獨立不影響加密計算。如此即可暴力窮舉出所有可視字元，依序破解每一個 byte

### exploit

- normal work

```python
#!/usr/bin/env python

from struct import *

with open('flag') as fd: 
    data = fd.read()

data = unpack('<{}i'.format(len(data) / 4), data)

def encrypt(data):
    for idx, item in enumerate(data):
        tmp = (2 + idx) * 0xcccccccd
        D = tmp >> 32
        A = tmp & 0xffffffff
        D >>= 3
        A = D * 10
        C = (2 + idx - A) & 0xff
        D = idx + 1 
        D <<= C
        print hex(ord(item) * D + 0x2333)
    return

def decrypt(data):
    ans = ''
    for idx, item in enumerate(data):
        tmp = (2 + idx) * 0xcccccccd
        D = tmp >> 32
        A = tmp & 0xffffffff
        D >>= 3
        A = D * 10
        C = (2 + idx - A) & 0xff
        D = idx + 1 
        D <<= C
        ans += chr((item - 0x2333) / D)
    print ans 
    return

decrypt(data)
```

- dirty work

```python
#!/usr/bin/env python

from pwn import *
import string
import os

with open('ans') as fd: 
    ans = fd.read()

def gen_ans(data):
    os.system('echo \'{}\' | ./hw1 '.format(data))
    with open('flag') as fd: 
        res = fd.read()
    return res 

test_ans = 'FLAG{'

for k in xrange(33):
    for i in string.printable:
        if ans.startswith(gen_ans(test_ans + i)):
            test_ans += i
            break

print test_ans
```

### flag

```FLAG{Iost4SXskSmu53CbCAI5e52FBJkj1JKl}```
