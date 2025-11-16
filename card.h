#ifndef CARD_H
#define CARD_H

#define COLORS 4
#define VALUES 10

typedef struct {
    char color[10];  // Red, Green, Blue, Yellow
    int value;       // 0–9
} Card;

typedef struct Node {
    Card card;
    struct Node* next;
} Node;

// Linked list hand functions
void addCard(Node** hand, Card c);
void removeCard(Node** hand, int pos);
int handSize(Node* hand);
void showHand(Node* hand);
int canPlay(Card c, Card top);

#endif