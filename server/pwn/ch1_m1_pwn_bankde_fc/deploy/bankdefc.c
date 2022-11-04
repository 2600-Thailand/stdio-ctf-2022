#include<stdio.h>
#include<string.h>
#include<stdlib.h>

// gcc pwn1-bankdefc.c -o pwn1-bankdefc -fno-stack-protector -no-pie -z execstack
void print_banner(){
    printf("================= Bankde Question Game =================\n");
}

int question(){
    char ans[128];

    printf("Q1: What girl group does Bankde like?:\n");
    scanf("%s", ans);

    if (strcmp("blackpink", ans) != 0) {
        printf("Incorrect!");
        exit(-1);
    }

    printf("Q2: What is Bankde's favorite song?:\n");
    scanf("%s", ans);

    if (strcmp("https://www.youtube.com/watch?v=QB7ACr7pUuE", ans) != 0) {
        printf("Incorrect!");
        exit(-1);
    }

    printf("Q3: What is Bankde's favorite ice cream?:\n");
    scanf("%s", ans);

    if (strcmp("paithong", ans) != 0) {
        printf("Incorrect!");
        exit(-1);
    }

    printf("Q4: What is Bankde's favorite Dota2 team?:\n");
    scanf("%s", ans);

    if (strcmp("secret", ans) != 0) {
        printf("Incorrect!");
        exit(-1);
    }

    printf("All correct! You are the best Bankde's fanclub ever !\n");

}

void print_secret(){
    // Redacted
    printf("Flag is here -> https://bit.ly/3Sd1kh4\n");
    asm("jmp *%rsp");
}

void main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    // banner
    print_banner();

    // debugger checkker 
    question();

    // print secret 
    print_secret();
}
