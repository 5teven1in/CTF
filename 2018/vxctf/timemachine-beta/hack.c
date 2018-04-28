#include <stdio.h>

int main(int argc, const char **argv, const char **envp) {
    int v3; // eax@42
    signed int i2; // [sp+8h] [bp-58h]@40
    int i1; // [sp+Ch] [bp-54h]@37
    int nn; // [sp+10h] [bp-50h]@34
    int mm; // [sp+14h] [bp-4Ch]@31
    int v9; // [sp+18h] [bp-48h]@31
    int v10; // [sp+1Ch] [bp-44h]@31
    int v11; // [sp+20h] [bp-40h]@31
    int ll; // [sp+24h] [bp-3Ch]@10
    signed int kk; // [sp+28h] [bp-38h]@9
    signed int jj; // [sp+2Ch] [bp-34h]@8
    signed int ii; // [sp+30h] [bp-30h]@7
    signed int n; // [sp+34h] [bp-2Ch]@6
    signed int m; // [sp+38h] [bp-28h]@5
    signed int l; // [sp+3Ch] [bp-24h]@4
    signed int k; // [sp+40h] [bp-20h]@3
    signed int j; // [sp+44h] [bp-1Ch]@2
    signed int i; // [sp+48h] [bp-18h]@1
    signed int v22; // [sp+4Ch] [bp-14h]@1

    puts("Beta: Cracking the key::Started. You need to wait for a 20 minutes :-)");
    fflush(stdout);
    v22 = 1;
    for ( i = 0; i <= 9; ++i )
    {
        for ( j = 0; j <= 8; ++j )
        {
            for ( k = 0; k <= 7; ++k )
            {
                for ( l = 0; l <= 6; ++l )
                {
                    for ( m = 0; m <= 5; ++m )
                    {
                        for ( n = 0; n <= 4; ++n )
                        {
                            for ( ii = 0; ii <= 3; ++ii )
                            {
                                for ( jj = 0; jj <= 2; ++jj )
                                {
                                    for ( kk = 0; kk <= 1; ++kk )
                                    {
                                        for ( ll = 0; ll <= 0; ++ll )
                                        {
                                            v22 *= 3;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    v11 = 0;
    v10 = 0;
    v9 = 0;
    for ( mm = 0; mm <= 999; mm = 2 * mm + 2 )
        v11 = 2 * mm + 1;
    for ( nn = 0; nn <= 999; nn = 4 * nn * nn + 2 )
        v10 = 4 * nn * nn + 1;
    for ( i1 = 0; i1 <= 999; i1 = i1 * 6 * i1 * i1 + 2 )
        v9 = i1 * 6 * i1 * i1 + 1;
    for ( i2 = 0; i2 <= 999999998; ++i2 ) {
        if ( i2 == 999999998 ) {
            v3 = 99998;
            printf("The flag is: %d", (unsigned int)((v10 + v11 + v22 + v9) / 4 + v3));
        }
    }
    return 0;
}
