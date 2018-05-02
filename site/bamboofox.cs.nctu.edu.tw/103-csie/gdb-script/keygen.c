#include <stdio.h>

int main()
{
    timer();

    int i;
    for (i = 0; i < 32; i++) {
        keygen(i); 
        int you_can_set_breakpoint_at_here = i;
    }
}
