%{
    #include<stdio.h>
    int bra=0,op=0,curop=0,num=0,grp=0;
%}
%option noyywrap
%%
[a-zA-Z]+ {
    printf(" ==> Error: Invalid character\n");
    exit(1);
}
[0-9]+ {
    if (bra == 0 || op == 0) {
        printf(" ==> Error: Missing operator or braket\n");
        exit(1);
    }
    num++;
    if (num > 2) {
        printf(" ==> Error: Too many numbers\n");
        exit(1);
    }
    printf("%s",yytext);
}
"(" {
    bra++;
    curop=0;
    printf("%s",yytext);
}
")" {
    if (bra == 2) {
        grp++;
    }
    if (grp > 2) {
        printf(" ==> Error: Too many groups\n");
        exit(1);
    }
    bra--;
    if (bra < 0) {
        printf(" ==> Error: Missing braket\n");
        exit(1);
    }
    if (op == 0 && grp < 2) {
        printf(" ==> Error: Missing operator\n");
        exit(1);
    }
    if (num < 2 && grp < 2 && grp+num != 2) {
        printf(" ==> Error: Missing number\n");
        exit(1);
    }
    if (bra == 0) {
        printf("%s ==> Success: end of expression\n",yytext);
        exit(1);
    }
    op--;
    num = num - 2;
    curop = 0;
    printf("%s",yytext);
}
[*+] {
    op++;
    curop++;
    if (curop > 1) {
        printf(" ==> Error: Too many operators\n");
        exit(1);
    }
    printf("%s",yytext);
}
\n {printf("\n");}
. {printf("%s",yytext);}

%%
int main()
{
    printf("Enter an expression: ");
    yylex();
    return 0;
} 