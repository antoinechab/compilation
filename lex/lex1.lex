%{
#include<stdio.h>
int op=0,num=0,bra=0;
%}
%option noyywrap
%%
[a-zA-Z]* {
    printf("\n %s n'est pas un symbole valide\n", yytext);
    exit(1);
}
[0-9]+ {
    if(op==0)
    {
        printf("\n il manque l'opérateur \n");
        exit(1);
    }
    num++;
    printf("%s",yytext);
}
[\+\-\*\/] {
    op++;
    printf("%s",yytext);
}
"(" {
    bra++;
    printf("%s",yytext);
}
")" {
    bra--;
    printf("%s",yytext);
}
\n {op=0;num=0;bra=0;}
. {printf("\n correct");exit(1);}
%%

int main()
{
    printf("expression:");
    yylex();
    return 0;
}