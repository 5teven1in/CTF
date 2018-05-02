set environment LD_LIBRARY_PATH ./
b *0x8048591
r
while(1)
  x/x $esp - 0x14
  c
end
