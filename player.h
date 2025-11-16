#ifndef PLAYER_H
#define PLAYER_H

#include "card.h"
#include "deck.h"

// Number of players
#define MAX_PLAYERS 2  

extern Node* hands[MAX_PLAYERS];

// Player actions
void dealCards();
void showPlayerHand(int playerIndex);
int playerTurn(int playerIndex);
int aiTurn(int playerIndex);
int checkWinCondition(int playerIndex);

#endif