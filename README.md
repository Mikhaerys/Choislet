# Choislet

Choislet is a modern desktop application built with Python and Flet 1.0 designed to help users make random decisions through interactive and fun tools.

## Features

* **Roulette:** Enter a list of candidates (options, names, tasks, etc.), and spin an animated roulette wheel with dynamic sector sizing to randomly select a winner.
* **Coin Flip:** Customize Heads and Tails options, and trigger an animated coin flip with real-time result history.
* **Dice Game:** Enter a list of players to compete in a dice tournament. Each player rolls 2 dice per round, with automatic tie-breaking until a final champion emerges.
* **Dashboard / Home:** Quick access hub to jump directly into any decision tool.

## Requirements

* Python 3.11+ (Python 3.13 recommended)
* Flet 1.0.5+

## Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate   # On Windows
   # source .venv/bin/activate  # On Linux/macOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To launch the desktop application with Hot Reload enabled:

```bash
flet run src/main.py
```

Or run directly with Python:

```bash
python -m src.main
```

On Windows, you can also double-click or run `Open_Choislet.ps1` with PowerShell.

## Running Tests

To run the automated test suite:

```bash
pytest
```
