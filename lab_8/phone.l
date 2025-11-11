%{
#include <stdio.h>
%}

%option noyywrap

%%

\(?[0-9][0-9]?[0-9]?[ -./]?[0-9][0-9]?[0-9]?[ -./]?[0-9][0-9]?[0-9]?\)?   { printf("$PHONE$"); }
.|\n                                                                      { ECHO; }

%%

int main(void) {
    yylex();
    return 0;
}

