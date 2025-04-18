# Choislet

Choislet is a desktop application designed to help users make random decisions through various fun and interactive tools.

## Features

*   **Roulette:** Enter a list of candidates (options, names, tasks, etc.), and spin the roulette to randomly select one.
*   **Coin Flip:** Define options for heads and tails, and flip a virtual coin to get a random outcome.
*   **Dice Game:** Enter a list of players, and roll two dice per player in rounds until a single winner with the highest score emerges.

## How it Works

The application is built using the Flet framework for Python, providing a graphical user interface.

1.  **Navigation:** Use the icons on the left sidebar to switch between the different decision-making tools (Roulette, Coin Flip, Dice Game).
2.  **Roulette:**
    *   Type the candidates into the text box, one per line.
    *   Click the "Spin" button.
    *   The roulette wheel will spin and land on a random candidate, announcing the winner.
3.  **Coin Flip:**
    *   (Optional) Enter custom names for the "Heads" and "Tails" options.
    *   Click the "Flip Coin" button.
    *   The coin will animate, and the result (Heads or Tails) will be displayed.
4.  **Dice Game:**
    *   Enter the names of the players, one per line.
    *   Click the "Roll Dice" button.
    *   Each player rolls two dice. If there's a tie for the highest score, the tied players roll again until a single winner is determined. The final winner and their score are announced.

## Technology

*   **Language:** Python
*   **Framework:** Flet (for the GUI)

## Running the Application

To run the application locally:

1.  Ensure you have Python installed.
2.  Install the required dependencies.
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the main script:
    ```bash
    flet run main.py
    ```
