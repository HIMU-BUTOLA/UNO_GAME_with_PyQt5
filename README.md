# UNO Card Game - Production GUI Edition

A modern, interactive UNO card game with a graphical user interface (GUI) built in Python using PyQt5. Play against an AI opponent with a polished, responsive interface featuring animated card displays, win overlays, and game statistics.

## Features

- 🎮 **Interactive GUI** - Clickable card images instead of CLI commands
- 🤖 **AI Opponent** - Smart AI player with strategic moves
- 💫 **Smooth Animations** - Card zooms, blurred win overlays, animated transitions
- 📊 **Game Stats** - Move history, turn counter, and visual feedback
- 🎨 **Dark Theme** - Eye-friendly dark UI with vibrant accent colors
- 🃏 **High-Quality Assets** - Card images from `U_CARDS` folder with facedown visuals for AI

---

## System Requirements

- **Windows** (7 or later), Linux, or macOS
- **Python 3.8+** (tested on Python 3.14)
- Internet connection (to download packages, one-time only)

---

## Installation & Setup (For Beginners)

### Step 1: Open Terminal in VS Code

1. Open the project folder in VS Code
2. Press **Ctrl + `` (Ctrl + backtick) to open the integrated terminal
3. You should see a PowerShell prompt (Windows) or bash (Mac/Linux)

### Step 2: Install Python Packages

Copy and paste this command into the terminal and press Enter:

```powershell
pip install PyQt5 Pillow
```

**Wait for the installation to complete.** You'll see output like:
```
Successfully installed PyQt5-5.15.x Pillow-10.x.x
```

**If you see an error:**
- **"pip: command not found"** → Python isn't installed. Download from [python.org](https://www.python.org/downloads/) and install
- **"Permission denied"** → Try: `pip install --user PyQt5 Pillow`
- **Other errors** → Copy the error message and search it online, or check Troubleshooting below

### Step 3: Verify Game Engine

The C game engine (`game.dll`) should already be compiled in your project folder. 

**Check it exists:**
- Look in the project root folder for a file named `game.dll` (Windows) or `libgame.so` (Linux)
- If missing, the game won't start

---

## How to Run the Game

### ✅ Option 1: Run the Main Game (Recommended)

In the VS Code terminal, type:

```powershell
python gui_qt.py
```

A window opens with the UNO game board. You can now:
- **Click cards** in your hand (bottom) to play them
- **Click the DRAW button** if you can't play any card
- **Click End Turn** to pass your turn to the AI
- **Win** by emptying your hand first
- See **move history** and the AI's card count on screen

---

### 🎮 Option 2: Preview the Win Screen (Demo)

To see what the end-of-game overlay looks like:

```powershell
python demo_overlay.py
```

A window appears with a blurred overlay showing a winner message and two buttons:
- **🔄 New Game** - Restart
- **⛔ Exit Game** - Close the app

Click the buttons to test them. The window auto-closes after 12 seconds.

---

### 🤖 Option 3: Automated Game (Engine Test)

To verify the AI and game logic work (no GUI):

```powershell
python demo.py
```

The terminal prints a turn-by-turn log of a full automated game, showing:
- Cards played by human and AI
- Whose turn it is
- Final winner

This is useful for testing if something is broken.

---

## Playing the Game - Quick Guide

### Your Turn
1. Look at the cards at the **bottom** of the screen (your hand)
2. **Green-bordered cards** can be played — click one to play it
3. **Grey cards** cannot be played right now
4. If no card is playable:
   - Click the **DRAW** button (light grey card to the left)
   - You must play or end your turn after drawing

### AI's Turn
- The AI's cards appear at the **top** as blue card-backs (count shown)
- You'll see "🤖 AI is thinking..." status
- The game continues automatically

### Win Screen
- When someone wins, a **blurred dark overlay** appears with the winner message
- Choose:
  - **🔄 New Game** to play again
  - **⛔ Exit Game** to close the app

---

## Troubleshooting

### Problem: "Module not found: PyQt5"

**Solution:**
```powershell
pip install PyQt5
```

Wait for it to finish, then try running the game again.

---

### Problem: "game.dll not found" or similar error

**Solution:**
1. Make sure you're in the **project root folder** in the terminal
2. Type `dir` or `ls` to see files — you should see `game.dll` listed
3. If it's missing, ask your instructor or check that the file was extracted/downloaded

---

### Problem: GUI window opens but nothing displays (blank/black)

**Solution:**
1. Check the terminal for error messages
2. Make sure `U_CARDS/` folder exists with PNG files inside
3. Try: `python demo.py` to test the engine separately
4. Restart VS Code and try again

---

### Problem: Click on a card but nothing happens

**Possible causes:**
- **Card is not playable** - Only cards matching the top discard's color OR number can be played. Green-highlighted cards are playable
- **Game logic issue** - Try drawing a card or ending your turn
- **Frozen UI** - Wait a moment (AI is thinking), or restart the game

---

### Problem: "pip" command not found

**Solution:**
1. Make sure Python is installed: Type `python --version` in terminal
   - If command not found, download Python from [python.org](https://www.python.org/downloads/)
2. Reinstall Python and check **"Add Python to PATH"** during installation
3. Restart VS Code terminal after installing Python

---

## File Guide

| File | Purpose |
|------|---------|
| `gui_qt.py` | Main game GUI (run this!) |
| `engine_py.py` | Python code that talks to the C engine |
| `game.dll` | Compiled C engine with game logic |
| `demo.py` | Text-only automated game test |
| `demo_overlay.py` | Win screen preview |
| `U_CARDS/` | Folder with card images (PNG files) |
| `README.md` | This guide |

---

## Advanced Tips (Optional)

### Make the UI Bigger
Edit `gui_qt.py`, find `self.resize(1200, 800)`, and change the numbers to larger values like `(1400, 900)`

### Change Animation Speed
Find `self.geom_anim.setDuration(650)` and change `650` (milliseconds) to higher for slower animation

### Adjust Blur Effect
Find `blur.setBlurRadius(12)` and try values like `8` (less blur) or `20` (more blur)

---

## Frequently Asked Questions

**Q: Can multiple people play?**  
A: Not yet. The game is 1 player vs AI. Multiplayer would require network features.

**Q: Where do I get more card designs?**  
A: Card images are in the `U_CARDS/` folder. You can replace PNG files with your own designs (keep the same filenames).

**Q: How do I change the game rules?**  
A: The C code (`game.c`, `player.c`) contains the game logic. Modify those files and rebuild with `make dll` (requires GCC compiler).

**Q: Does this work on Mac/Linux?**  
A: Yes, PyQt5 is cross-platform. You may need to rebuild the C engine for your OS.

**Q: Can I close the game mid-game?**  
A: Yes, close the window. There's no save feature, so progress is lost.

---

## Need More Help?

1. **Check the terminal output** — Error messages often explain what went wrong
2. **Run `python demo.py`** — Tests if the core engine works
3. **Reinstall packages** — `pip install --upgrade PyQt5 Pillow`
4. **Restart VS Code** — Sometimes the terminal needs a fresh start

---

**Happy playing! 🎴✨**
