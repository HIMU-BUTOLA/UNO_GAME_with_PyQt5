#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "deck.h"

Card deck[DECK_SIZE];
int deckTop = -1;
Card discardPile[1000];
int discardTop = -1;

char* colors[4] = {"Red", "Green", "Blue", "Yellow"};

void pushDeck(Card c) { deck[++deckTop] = c; }
Card popDeck() { return deck[deckTop--]; }

void pushDiscard(Card c) { discardPile[++discardTop] = c; }
Card topDiscard() { return discardPile[discardTop]; }

void initDeck() {
    int k = 0;
    for (int i = 0; i < COLORS; i++) {
        for (int j = 0; j < VALUES; j++) {
            strcpy(deck[k].color, colors[i]);
            deck[k].value = j;
            k++;
        }
    }
    deckTop = DECK_SIZE - 1;
}

void shuffle() {
    srand(time(0));
    for (int i = 0; i < DECK_SIZE; i++) {
        int r = rand() % DECK_SIZE;
        Card temp = deck[i];
        deck[i] = deck[r];
        deck[r] = temp;
    }
}