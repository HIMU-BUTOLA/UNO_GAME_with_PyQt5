#ifndef GAME_H
#define GAME_H

#include "player.h"


typedef struct {
    int items[MAX_PLAYERS];
    int front, rear, size;
} Queue;

void initQueue(Queue* q);
void enqueue(Queue* q, int x);
int dequeue(Queue* q);
int peek(Queue* q);
void playGame();

#endif