#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<klee/klee.h>
#define SIZE 40
int hash[36] = {405, 434, 457, 506, 467, 449, 465, 398, 381, 459, 465, 466, 538, 542, 546, 467, 449, 453, 463, 448, 523, 457, 448, 442, 455, 452, 521, 536, 463, 460, 467, 466, 453, 467, 483, 372};

int count(char* s, int start, int end)
{
    int sum = 0;
    for (int i = start; i < end; i++)
        sum += s[i];
    return sum;
}
int checksum(char* s)
{
    for (int i = 0; i + 5 <= SIZE; i++)
        if (count(s, i, i + 5) != hash[i])
            return 0;
    return 1;
}
int main()
{
    char s[40];
    printf("Hint: flag is \"FLAG{...}\" format.\n");
    // read(0, s, 40);
    klee_make_symbolic(s, 40, "s");
    klee_assume(s[0] == 'F');
    klee_assume(s[1] == 'L');
    klee_assume(s[2] == 'A');
    klee_assume(s[3] == 'G');
    klee_assume(s[4] == '{');
    if (checksum(s)) {
        printf("You passed.\n");
        klee_assert(0);
    }
    else
        printf("Maybe try again?\n");
}


