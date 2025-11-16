#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "card.h"

void addCard(Node** hand, Card c) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->card = c;
    newNode->next = *hand;
    *hand = newNode;
}

void removeCard(Node** hand, int pos) {
    Node* temp = *hand, *prev = NULL;
    for (int i = 1; temp && i < pos; i++) {
        prev = temp;
        temp = temp->next;
    }
    if (temp) {
        if (prev) prev->next = temp->next;
        else *hand = temp->next;
        free(temp);
    }
}

int handSize(Node* hand) {
    int count = 0;
    while (hand) {
        count++;
        hand = hand->next;
    }
    return count;
}

void showHand(Node* hand) {
    int i = 1;
    while (hand) {
        printf("%d. %s %d\n", i, hand->card.color, hand->card.value);
        hand = hand->next;
        i++;
    }
}

int canPlay(Card c, Card top) {
    return (strcmp(c.color, top.color) == 0 || c.value == top.value);
}