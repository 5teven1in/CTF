#!/usr/bin/python -u
import os
import time
import random
import fractions

code1="""#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <signal.h>

uint64_t map = (1ULL<<36)-1;
uint64_t piece[9][9] = {
"""

code3="""
};
int p=0;
int num_piece = 9;
char in[4]={0,0,0,0},i=0;

void catflag(){
	system(" """

code4="echo GJ!"

code5="""");
}

void handler(){
    puts("Time's up!");
    exit(-1);
}

int main(){
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 1, 0LL);
    signal(SIGALRM, handler);
    alarm(60);
    for( p = 0 ; p < num_piece; p++ ){
	printf("%dth Piece\\n",p);
        read(0,in,3);
	if( in[0] < '0' || in[0] > '6' ) return -1;
	if( in[1] < '0' || in[1] > '6' ) return -1;
	if( in[2] != '\\n' ) return -1;
        in[0] -= '0';
        in[1] -= '0';
        for( i = 0 ; piece[p][i] != 0 ; i++ ){
            piece[p][i] = piece[p][i]*(1ULL<<in[0])*(1ULL<<(6*in[1]));
            map -= piece[p][i];
        }
    }
    if( map == 0 ){
        catflag();
	return 0;
	}
    else{
        puts("GG");
	return -1;
	}
}

"""

def genarr():
	matrix = [ x for x in range(36) ]
	msize = 36
	arr = ["{},{},{},{},{},{},{},{},{}" for x in range(9) ]

	for i in range(9):
		piece=[0,0,0,0,0,0,0,0,0]
		size = random.randint(4,5)
		n=6
		m=6
		if i == 8 :
			size = msize
		if size > msize :
			size = msize
		msize = msize - size
		for j in range(size):
			r = random.randint(0,len(matrix)-1)
			piece[j] = matrix[r]
			del matrix[r]
		#print piece
		for j in range(size):
			n = piece[j]%6 if piece[j]%6 < n else  n
			m = piece[j]/6 if piece[j]/6 < m else  m
		for j in range(size):
			piece[j] = 1<<(piece[j]-(6*m)-n)
		#print piece,m,n
		arr[i] =  "{"+arr[i].format(piece[0],piece[1],piece[2],piece[3],piece[4],piece[5],piece[6],piece[7],piece[8])+"},"
	return arr


os.chdir('/tmp/')
code2 = "".join(genarr())
f = open("puzzle.c","w+")
f.write(code1+code2+code3+code4+code5)
f.close()
os.popen('gcc puzzle.c -o puzzle.out');
print("Hey")
print("Try to solve magic puzzle")
print("I will send you program encoded by base64")
time.sleep(1)
output = os.popen('base64 puzzle.out');
print output.read()
rv = os.system('./puzzle.out');
if rv != 0 :
	print "Wrong answer"
	exit(1)

code2 = "".join(genarr())
code4 = "cat flag"
f = open("puzzle.c","w+")
f.write(code1+code2+code3+code4+code5)
f.close()
os.popen('gcc puzzle.c -o puzzle.out');
output = os.popen('base64 puzzle.out');
print output.read()
rv = os.system('./puzzle.out');
