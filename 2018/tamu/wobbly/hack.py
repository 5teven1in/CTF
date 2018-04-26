#!/usr/bin/python3

m = [103, -48, -48, -52, -46, -24, -33, -45, -35, -30, -45, -95, -82, -43, -41, -39, -24, 123]
pre = 0

for i in m:
    pre = i - pre
    print(chr(pre % 256), end = '')
