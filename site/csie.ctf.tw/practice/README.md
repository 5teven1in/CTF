practice
===

## strings

### concept

使用 ```strings``` 查看 binary 檔案中可視字元，搭配 ```grep``` 指令即可找到 flag

### exploit

```strings ./strings | grep FLAG```

### flag

```FLAG{__flag_in_the_file}```

## strace

### concept

使用 ```strace``` 指令搭配 ```-s``` 指定 string size

### exploit

```strace -s 36 ./strace```
其中就可以發現 flag

### flag

```FLAG{____yaaaa_flag_in_the_stack___}```

## patching

### concept

執行程式後發現只要將 Value 改成 0x00023333 就可以獲得 flag

```
Value = 0x376c8
Go patching the value to 0x00023333
```

使用 ```xxd``` 即可修改 binary 檔案，需要注意的是 Value 的值是 little endian 的方式儲存，修改時也要依格式更改值

### exploit

搜尋 c876 03 後修改其中的值

![](https://i.imgur.com/HAmxIv3.png)

直接修改為 3333 02 儲存後執行就可以獲得 flag

![](https://i.imgur.com/QUitdsV.png)

### flag

```FLAG{oa11TH80wfMEs6ZflBhGF4btUcS1Ds9y}```

## pwntools

### concept

使用 pwntool 連上遠端題目後二分搜猜到數字後即可獲得 flag

### exploit

```python
#!/usr/bin/env python

from pwn import *
import time

# r = remote("localhost", 10123)
r = remote("csie.ctf.tw", 10124)

x = 1 
y = 50000000

r.recvuntil('= ')

while True:
    mid = (x + y) / 2 
    r.sendline(str(mid))
    res = r.recvuntil('= ')
    if 'small' in res:
        x = mid + 1 
    elif 'big' in res:
        y = mid 
    else:
        print res 
        break

r.interactive()
```

### flag

```FLAG{h02Ooysbv4O5Lf1Fmdrt2QKts7buYz0J}```
