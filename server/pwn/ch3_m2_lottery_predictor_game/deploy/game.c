#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<stdint.h>

#define MAX 9
#define MIN 1

// gcc game.c -o game -no-pie -z execstack
void print_banner(){
    printf("========== Bankde Lottery Guesser ==========\n");
}

int lottery(int q){
    uint64_t lottery[MAX] = {
        613106,
        484669,
        943703,
        929332,
        331583,
        436594,
        474482,
        652362,
        983252
    };

    // bounds checking
    if (q > MAX || q < MIN) {
        printf("Get out hacker\n");
        exit(1);
    }
    printf("%lu\n", lottery[q]);
}

void print_secret(){
    // Redacted
    printf("Flag is here -> https://bit.ly/3Sd1kh4\n");
}

void main(){
    int q;
    char ans[8];

    setvbuf(stdout, NULL, _IONBF, 0);

    print_banner();

    while (1) {
        printf("Your Lucky Number [%d-%d]: ", MIN, MAX);
        fflush(stdout);

        scanf("%d", &q);
        lottery(q);

        printf("Again ?: ");
        fflush(stdout);
        scanf(" %s", ans);
        if (strcmp(ans, "no") == 0) break;
    }
}