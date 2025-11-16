#ifndef ENGINE_H
#define ENGINE_H

#include "card.h"
#include "player.h"
#include "deck.h"

#ifdef _WIN32
#  ifdef BUILDING_ENGINE
#    define ENGINE_API __declspec(dllexport)
#  else
#    define ENGINE_API __declspec(dllimport)
#  endif
#else
#  define ENGINE_API
#endif

// Initialize engine (deck, shuffle, deal, initial discard)
ENGINE_API void engine_init();

// Reset / restart
ENGINE_API void engine_reset();

// Query current player (0 = human, 1 = AI)
ENGINE_API int engine_get_current_player();

// Get top discard
ENGINE_API Card engine_get_top_discard();

// Get hand size for player
ENGINE_API int engine_get_hand_size(int player);

// Fill an array of Cards with the player's hand; returns number of cards written (max elements given)
ENGINE_API int engine_get_hand(int player, Card* out_array, int max);

// Player actions
// Play a card at 1-based position; returns 1 on success, 0 on invalid move
ENGINE_API int engine_play_card(int player, int position);

// Draw a card (position 0 equivalent); returns 1 if drawn-and-kept, 2 if drawn-and-played, 0 if deck empty
ENGINE_API int engine_draw_card(int player);

// Advance AI turn (AI will play/draw as needed). Returns 1 if AI played, 0 otherwise
ENGINE_API int engine_ai_move();

// Advance to next player (used if GUI drives turns)
ENGINE_API void engine_next_turn();

// Check for winner, returns player index or -1 if none
ENGINE_API int engine_check_winner();

#endif
