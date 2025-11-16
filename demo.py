"""
Demo script showing the UNO game engine working with Python bindings.
This runs a full game turn-by-turn to show the system in action.
"""
import engine_py


def print_hand(player, label):
    hand = engine_py.get_hand(player)
    print(f"\n{label}:")
    if not hand:
        print("  (empty)")
    else:
        for i, (color, value) in enumerate(hand, start=1):
            print(f"  {i}. {color} {value}")


def main():
    print("=" * 60)
    print("UNO Card Game - Demo")
    print("=" * 60)

    # Initialize game
    engine_py.init()
    print("\n✓ Game initialized")

    turn = 0
    while True:
        turn += 1
        print(f"\n{'=' * 60}")
        print(f"TURN {turn}")
        print(f"{'=' * 60}")

        current = engine_py.get_current_player()
        top_color, top_val = engine_py.get_top_discard()
        print(f"Top discard: {top_color} {top_val}")

        if current == 0:
            print("\n>>> HUMAN PLAYER's TURN")
            print_hand(0, "Your Hand")

            hand = engine_py.get_hand(0)
            # Find first playable card
            played = False
            for idx, (color, value) in enumerate(hand, start=1):
                if engine_py.play_card(0, idx):
                    top_color, top_val = engine_py.get_top_discard()
                    print(f"\n✓ You played: {color} {value}")
                    print(f"  Top discard is now: {top_color} {top_val}")
                    played = True
                    break
            if not played:
                # Draw instead
                res = engine_py.draw_card(0)
                if res == 1:
                    print(f"\n✓ You drew a card (kept it)")
                elif res == 2:
                    top_color, top_val = engine_py.get_top_discard()
                    print(f"\n✓ You drew and played it!")
                    print(f"  Top discard is now: {top_color} {top_val}")
                else:
                    print(f"\n✗ Deck is empty!")

        else:
            print("\n>>> AI PLAYER's TURN")
            print_hand(1, "AI Hand")

            if engine_py.ai_move():
                top_color, top_val = engine_py.get_top_discard()
                print(f"\n✓ AI played!")
                print(f"  Top discard is now: {top_color} {top_val}")
            else:
                print(f"\n✓ AI drew a card")

        # Advance turn
        engine_py.next_turn()

        # Check winner
        winner = engine_py.check_winner()
        if winner != -1:
            print(f"\n{'=' * 60}")
            print(f"🎉 GAME OVER! Player {winner} wins!")
            print(f"{'=' * 60}\n")
            break

        if turn > 50:
            print("\n⚠ Demo stopped after 50 turns (max).\n")
            break


if __name__ == '__main__':
    main()
