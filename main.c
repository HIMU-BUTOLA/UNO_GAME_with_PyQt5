#include <stdio.h>
#include "game.h"

int main() {
    printf("=== UNO: Human vs AI ===\n");
    initDeck();
    shuffle();
    dealCards();
    playGame();
    return 0;
}