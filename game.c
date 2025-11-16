#include <stdio.h>
#include <stdlib.h>
#include "game.h"

void initQueue(Queue* q) {
    q->front = 0; q->rear = -1; q->size = 0;
}

void enqueue(Queue* q, int x) {
    if (q->size < MAX_PLAYERS) {
        q->rear = (q->rear + 1) % MAX_PLAYERS;
        q->items[q->rear] = x;
        q->size++;
    }
}

int dequeue(Queue* q) {
    int val = q->items[q->front];
    q->front = (q->front + 1) % MAX_PLAYERS;
    q->size--;
    return val;
}

int peek(Queue* q) {
    return q->items[q->front];
}

void playGame() {
    Queue q;
    initQueue(&q);
    enqueue(&q, 0); // Human
    enqueue(&q, 1); // AI

    pushDiscard(popDeck()); // Initial discard
    int winner = -1;

    while (winner == -1) {
        int curr = peek(&q);

        if (curr == 0)
            playerTurn(curr);
        else
            aiTurn(curr);

        if (checkWinCondition(curr)) {
            winner = curr;
            break;
        }

        dequeue(&q);
        enqueue(&q, curr);
    }

    printf("\n=== GAME OVER ===\n");
    if (winner == 0)
        printf("🏆 You Win!\n");
    else
        printf("💻 AI Wins!\n");
}