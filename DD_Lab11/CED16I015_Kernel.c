#include <stdio.h>

int main(int argc, char *argv[]){
    char *ptr = (char *)0xc0000000; 
    printf("%c\n", *ptr); 

    return 0;
}