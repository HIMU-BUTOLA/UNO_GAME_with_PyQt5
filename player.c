#include <stdio.h>
#include <stdlib.h>
#include "player.h"

Node* hands[MAX_PLAYERS];

// Deal initial cards to both players
void dealCards() {
    for (int p = 0; p < MAX_PLAYERS; p++) {
        hands[p] = NULL;
        for (int i = 0; i < 7; i++) {
            addCard(&hands[p], popDeck());
        }
    }
}

// Display a player’s hand
void showPlayerHand(int playerIndex) {
    printf("\nPlayer %d's Hand:\n", playerIndex + 1);
    showHand(hands[playerIndex]);
}

// Handle a human player's turn
int playerTurn(int playerIndex) {
    printf("\n--- Your Turn ---\n");
    printf("Top of discard: %s %d\n", topDiscard().color, topDiscard().value);
    showPlayerHand(playerIndex);

    int choice;
    printf("Choose card to play (0 to draw): \n");
    fflush(stdout);
    scanf("%d", &choice);

    if (choice == 0) {
        if (deckTop >= 0) {
            Card drawn = popDeck();
            printf("You drew: %s %d\n", drawn.color, drawn.value);
            if (canPlay(drawn, topDiscard())) {
                printf("You played it!\n");
                pushDiscard(drawn);
            } else {
                addCard(&hands[playerIndex], drawn);
            }
        } else {
            printf("Deck empty!\n");
        }
        return 0;
    } else {
        Node* temp = hands[playerIndex];
        for (int i = 1; i < choice && temp; i++) temp = temp->next;
        if (temp && canPlay(temp->card, topDiscard())) {
            pushDiscard(temp->card);
            removeCard(&hands[playerIndex], choice);
            printf("You played: %s %d\n", topDiscard().color, topDiscard().value);
            return 1;
        } else {
            printf("Invalid move! Turn skipped.\n");
            return 0;
        }
    }
}

// AI logic: play first valid card or draw
int aiTurn(int playerIndex) {
    printf("\n--- AI's Turn ---\n");
    printf("Top of discard: %s %d\n", topDiscard().color, topDiscard().value);

    Node* temp = hands[playerIndex];
    int pos = 1;
    while (temp) {
        if (canPlay(temp->card, topDiscard())) {
            printf("AI played: %s %d\n", temp->card.color, temp->card.value);
            pushDiscard(temp->card);
            removeCard(&hands[playerIndex], pos);
            return 1;
        }
        temp = temp->next;
        pos++;
    }

    if (deckTop >= 0) {
        Card drawn = popDeck();
        printf("AI drew: %s %d\n", drawn.color, drawn.value);
        if (canPlay(drawn, topDiscard())) {
            printf("AI played drawn card!\n");
            pushDiscard(drawn);
        } else {
            addCard(&hands[playerIndex], drawn);
        }
    } else {
        printf("Deck empty!\n");
    }
    return 0;
}

// Check if player has won
int checkWinCondition(int playerIndex) {
    return (handSize(hands[playerIndex]) == 0);
}