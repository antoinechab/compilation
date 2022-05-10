#!/bin/bash

read -p "numéro du fichier .lex ?" lexfile
reponse() {
    lex lex$lexfile.lex
}
reponse
gcc -o lex$lexfile lex.yy.c
gcc -c lex.yy.c

exit