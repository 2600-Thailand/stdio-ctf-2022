#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

struct history{
    int count;
    char datetime[100];
};

char name[128];
struct history history_list[100];
int history_index = 0;

// gcc -static SuperGuesser.c -o SuperGuesser -fno-stack-protector

void print_menu(){
    printf("========: Super Guesser :=======\n");
    printf("1. Play Guesser!\n");
    printf("2. View Score History\n");
    printf("3. Credit\n");
    printf("> ");
}

void guesser_game(){
    int magic_number = rand() % 69;
    int count = 0;
    int guess = 0;
    char choice[4];
    printf("Guess the magic number!\n");
    printf("The number range is 0-69.\n");
    while(1){
        count++;
        printf(">");
        scanf(" %d", &guess);
        if(guess == magic_number){
            printf("Correct! the magic number is %d\n", magic_number);
            break; // exit loop
        } else{
            if (guess > magic_number){
                printf("Invalid! the magic number is less than %d.\n", guess);
            } else if (guess < magic_number){
                printf("Invalid! the magic number is more than %d.\n", guess);
            }
        }
    }

    printf("Do you want to save the history?(Yes/No)\n");
    printf(">");
    scanf(" %s", choice);
    if (!strcmp("Yes", choice)){
        // don't know how it work just copy from somewhere
        time_t t = time(NULL);
        struct tm *tm = localtime(&t);

        history_list[history_index].count = count;
        strcpy(history_list[history_index].datetime,asctime(tm));
        history_index++;
        printf("Saved!\n");
    } else{
        printf("Back to main menu.\n");
    }
}


// view score function

void view_history(){
    printf("Work In Progress!\n");
}


// Credit
void print_credit(){
    printf("Bankde's Self Introduction Video: https://www.youtube.com/watch?v=EE-xtCF3T94\n");
}


void main(){
    setvbuf(stdout, NULL, _IONBF, 0);
    srand(time(NULL));
    int inp;
    // input name
    printf("Setup Name: ");
    scanf(" %s", name);

    // menu - guesser game, scoreboard
    while(1){
        print_menu();
        scanf(" %d", &inp);
        switch (inp){
            case 1:
                guesser_game();
                break;
            case 2:
                view_history();
                break;
            case 3:
                print_credit();
                break;
            default:
                printf("Invalid Choice!\n");
        }
    }
}