#!/usr/bin/python2 -u
import time
import random
import string
import os
import subprocess
import signal

begin = """
#include <stdio.h>
#include <stdlib.h>
int oo[10];
int ooo[100];
int oooo[1000];
int ooo000()
{
    puts("Guess OOO");
    for(int i=0; i<1000; i++)
    {
        int o;
        scanf("%d",&o);
        if (o!=oooo[i])
            return 0;
    }
    return 1;
}

int oo00()
{
    puts("Guess OO");
    for(int i=0; i<100; i++)
    {
        int o;
        scanf("%d",&o);
        if (o!=ooo[i])
            return 0;
    }
    return 1;
}

int o0()
{
    puts("Guess O");
    for(int i=0; i<10; i++)
    {
        int o;
        scanf("%d",&o);
        if (o!=oo[i])
            return 0;
    }
    return 1;
}
int main(int argc, char * argv[])
{
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stdin, 0LL, 1, 0LL);
    puts("If you want to OO, you have to OO first");
"""
end = """
    if(o0() && oo00() && ooo000())
    {
        puts("You can OO now.");
        system("sh");
    } 
    return 0; 
}
"""


def timeout(signum,frame):
    print("TIMEOUT")
    exit(0)


if __name__ == "__main__":
    oo = range(0,10)
    ooo = range(0,100)
    oooo = range(0,1000)

    random.shuffle(oo)
    random.shuffle(ooo)
    random.shuffle(oooo)

    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(30)
    os.chdir("/tmp/")

    print("Hey")
    print("Try to bypass oo program")
    print("I will send you program encoded by base64")
    time.sleep(1)
    filename = time.strftime("%m%d_%H%M%S", time.localtime()) + os.urandom(16).encode('hex') + ".c"
    with open(filename, "wb") as f:
        initial= ''
        for i in range(10):
            initial +="oo["+str(i)+"]="+str(oo[i])+";\n"
        for i in range(100):
            initial +="ooo["+str(i)+"]="+str(ooo[i])+";\n"
        for i in range(1000):
            initial +="oooo["+str(i)+"]="+str(oooo[i])+";\n"
        f.write(begin)
        f.write(initial)
        f.write(end)
    os.system("gcc -o ./"+filename[:-2]+" ./"+filename+" 2>/dev/null")
    os.system("strip ./"+filename[:-2])
    result = subprocess.check_output("base64 ./"+filename[:-2] , shell=True)
    print(result)
    print("\nNOW GIVE ME YOUR INPUT\n")
    os.execv('./'+filename[:-2],[''])
