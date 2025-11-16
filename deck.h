#ifndef DECK_H
#define DECK_H

#include "card.h"

#define DECK_SIZE (COLORS * VALUES)

extern Card deck[DECK_SIZE];
extern int deckTop;
extern Card discardPile[1000];
extern int discardTop;
extern char* colors[4];

// Deck and discard functions
void initDeck();
void shuffle();
void pushDeck(Card c);
Card popDeck();
void pushDiscard(Card c);
Card topDiscard();

#endif