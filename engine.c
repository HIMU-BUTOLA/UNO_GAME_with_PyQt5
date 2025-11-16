#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "engine.h"

// track whose turn it is (0 human, 1 AI)
static int current_player = 0;

void engine_init() {
    initDeck();
    shuffle();
    dealCards();
    // initial discard
    pushDiscard(popDeck());
    current_player = 0;
}

void engine_reset() {
    // reinitialize globals
    initDeck();
    shuffle();
    // clear hands
    for (int p = 0; p < MAX_PLAYERS; p++) {
        while (handSize(hands[p]) > 0) removeCard(&hands[p], 1);
    }
    deckTop = -1; // but initDeck sets it
    engine_init();
}

int engine_get_current_player() {
    return current_player;
}

Card engine_get_top_discard() {
    return topDiscard();
}

int engine_get_hand_size(int player) {
    if (player < 0 || player >= MAX_PLAYERS) return 0;
    return handSize(hands[player]);
}

int engine_get_hand(int player, Card* out_array, int max) {
    if (player < 0 || player >= MAX_PLAYERS || !out_array || max <= 0) return 0;
    Node* temp = hands[player];
    int i = 0;
    // The hand linked list stores newest at head; to keep order similar to CLI we iterate and fill
    while (temp && i < max) {
        out_array[i++] = temp->card;
        temp = temp->next;
    }
    return i;
}

int engine_play_card(int player, int position) {
    if (player < 0 || player >= MAX_PLAYERS) return 0;
    Node* temp = hands[player];
    for (int i = 1; temp && i < position; i++) temp = temp->next;
    if (temp && canPlay(temp->card, topDiscard())) {
        pushDiscard(temp->card);
        removeCard(&hands[player], position);
        return 1;
    }
    return 0;
}

int engine_draw_card(int player) {
    if (player < 0 || player >= MAX_PLAYERS) return 0;
    if (deckTop < 0) return 0;
    Card drawn = popDeck();
    if (canPlay(drawn, topDiscard())) {
        pushDiscard(drawn);
        return 2; // drawn and played
    } else {
        addCard(&hands[player], drawn);
        return 1; // drawn and kept
    }
}

int engine_ai_move() {
    int playerIndex = 1; // AI is player 1 in current game
    Node* temp = hands[playerIndex];
    int pos = 1;
    while (temp) {
        if (canPlay(temp->card, topDiscard())) {
            pushDiscard(temp->card);
            removeCard(&hands[playerIndex], pos);
            return 1;
        }
        temp = temp->next;
        pos++;
    }
    if (deckTop >= 0) {
        Card drawn = popDeck();
        if (canPlay(drawn, topDiscard())) {
            pushDiscard(drawn);
            return 1;
        } else {
            addCard(&hands[playerIndex], drawn);
            return 0;
        }
    }
    return 0;
}

void engine_next_turn() {
    current_player = (current_player + 1) % MAX_PLAYERS;
}

int engine_check_winner() {
    for (int p = 0; p < MAX_PLAYERS; p++) {
        if (handSize(hands[p]) == 0) return p;
    }
    return -1;
}
