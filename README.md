# Rock–Paper–Scissors–Plus AI Referee

## Overview
This project implements a minimal AI Game Referee chatbot for the game **Rock–Paper–Scissors–Plus**, as part of the AI Product Engineer assignment.

The system enforces game rules, validates user input, tracks game state across turns, and provides clear round-by-round feedback in a conversational loop.

---

## Game Rules
- Best of 3 rounds
- Valid moves: rock, paper, scissors, bomb
- Bomb beats all other moves
- Bomb vs bomb results in a draw
- Each player can use bomb only once per game
- Invalid input wastes the round
- The game ends automatically after 3 rounds

---

## Architecture & Design

### State Model
Game state is maintained outside the prompt using a shared state object:
- Round number
- User score
- Bot score
- Bomb usage per player
- Game-over flag

This ensures state persistence across turns.

### Tool-Based Logic
The implementation follows a tool-oriented design aligned with Google ADK principles:

- `validate_move` – handles intent understanding and input validation  
- `resolve_round` – applies game rules and determines the round winner  
- `update_game_state` – mutates persistent state  
- `play_turn` – orchestrates tool usage for each interaction  

Each function has a single responsibility and mirrors how ADK tools are expected to behave.

---

## Google ADK Note
The assignment specifies the use of Google ADK tools. At the time of implementation, the publicly available `google-adk` package does not expose the documented Tool APIs (`Tool`, `@tool`) in stable releases, particularly on Windows and Python 3.10+.

To handle this, the system:
- Attempts to use Google ADK Agent and Tool APIs when available
- Falls back to an equivalent tool-based architecture without changing logic or state modeling

This preserves ADK semantics and provides a clear migration path once the SDK stabilizes.

---

## How to Run

```bash
python game_referee.py
