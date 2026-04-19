import random
import tkinter as tk

# ==================================================
# CARD
# ==================================================

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def name(self):
        names = {11:"J",12:"Q",13:"K",14:"A"}
        v = names.get(self.value, str(self.value))
        return f"{v} of {self.suit}"


# ==================================================
# DECK
# ==================================================

class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

        for s in suits:
            for v in range(2, 15):
                self.cards.append(Card(v, s))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()


# ==================================================
# HAND EVALUATION
# ==================================================

def evaluate_hand(hand):
    values = [c.value for c in hand]
    counts = {}

    for v in values:
        counts[v] = counts.get(v, 0) + 1

    pairs = 0
    three = False

    for c in counts.values():
        if c == 3:
            three = True
        elif c == 2:
            pairs += 1

    if three:
        return 3, "Three of a Kind"
    elif pairs == 2:
        return 2, "Two Pair"
    elif pairs == 1:
        return 1, "One Pair"
    else:
        return 0, "High Card"


# ==================================================
# GUI GAME
# ==================================================

class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Game")

        # 🎨 BACKGROUND COLOR
        self.root.configure(bg="#1e1e2f")

        self.deck = None
        self.player_hand = []
        self.computer_hand = []

        self.player_score = 0
        self.computer_score = 0
        self.ties = 0

        # ==================================================
        # TITLE
        # ==================================================

        self.title = tk.Label(
            root,
            text="POKER GAME",
            font=("Arial", 22, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        self.title.pack(pady=10)

        # ==================================================
        # LABELS
        # ==================================================

        self.player_label = tk.Label(root, text="", fg="lightgreen", bg="#1e1e2f")
        self.player_label.pack(pady=5)

        self.computer_label = tk.Label(root, text="Computer: ???", fg="orange", bg="#1e1e2f")
        self.computer_label.pack(pady=5)

        self.result_label = tk.Label(root, text="", fg="white", bg="#1e1e2f")
        self.result_label.pack(pady=5)

        self.score_label = tk.Label(root, text="", fg="cyan", bg="#1e1e2f")
        self.score_label.pack(pady=5)

        # ==================================================
        # BUTTON STYLE (BIG + COLOR)
        # ==================================================

        button_style = {
            "font": ("Arial", 14, "bold"),
            "width": 20,
            "height": 2,
            "bd": 3
        }

        # ==================================================
        # BUTTONS
        # ==================================================

        tk.Button(
            root,
            text="PLAY ROUND",
            bg="#4CAF50",
            fg="white",
            command=self.play_round,
            **button_style
        ).pack(pady=5)

        tk.Button(
            root,
            text="REVEAL COMPUTER",
            bg="#2196F3",
            fg="white",
            command=self.reveal,
            **button_style
        ).pack(pady=5)

        tk.Button(
            root,
            text="SHOW RULES",
            bg="#FF9800",
            fg="black",
            command=self.show_rules,
            **button_style
        ).pack(pady=5)

        tk.Button(
            root,
            text="RESET SCORE",
            bg="#f44336",
            fg="white",
            command=self.reset,
            **button_style
        ).pack(pady=5)

        self.update_score()

    # ==================================================
    # PLAY ROUND
    # ==================================================

    def play_round(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand = [self.deck.draw() for _ in range(5)]
        self.computer_hand = [self.deck.draw() for _ in range(5)]

        self.player_label.config(
            text="Player: " + ", ".join([c.name() for c in self.player_hand])
        )

        self.computer_label.config(text="Computer: ???")
        self.result_label.config(text="Computer is hidden...")

    # ==================================================
    # REVEAL + TIEBREAKER
    # ==================================================

    def reveal(self):
        self.computer_label.config(
            text="Computer: " + ", ".join([c.name() for c in self.computer_hand])
        )

        p_rank, _ = evaluate_hand(self.player_hand)
        c_rank, _ = evaluate_hand(self.computer_hand)

        if p_rank > c_rank:
            self.result_label.config(text="You Win!")
            self.player_score += 1

        elif c_rank > p_rank:
            self.result_label.config(text="Computer Wins!")
            self.computer_score += 1

        else:
            p_vals = sorted([c.value for c in self.player_hand], reverse=True)
            c_vals = sorted([c.value for c in self.computer_hand], reverse=True)

            winner = "tie"

            for p, c in zip(p_vals, c_vals):
                if p > c:
                    self.result_label.config(text="Tie → You Win!")
                    self.player_score += 1
                    winner = "player"
                    break
                elif c > p:
                    self.result_label.config(text="Tie → Computer Wins!")
                    self.computer_score += 1
                    winner = "computer"
                    break

            if winner == "tie":
                self.result_label.config(text="Exact Tie!")
                self.ties += 1

        self.update_score()

    # ==================================================
    # RULES
    # ==================================================

    def show_rules(self):
        rules = tk.Toplevel(self.root)
        rules.title("Rules")
        rules.configure(bg="white")

        text = """
CARD ORDER:
2 < 3 < 4 < 5 < 6 < 7 < 8 < 9 < 10 < J < Q < K < A

HAND RANKS:
- Three of a Kind
- Two Pair
- One Pair
- High Card

TIEBREAKER:
Cards are sorted from highest to lowest.
Highest card is compared first.
If equal, next card is compared.
First difference decides winner.
If all equal → Tie.
"""
        tk.Label(rules, text=text, justify="left", bg="white", font=("Arial", 11)).pack(padx=10, pady=10)

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.update_score()
        self.result_label.config(text="Scores reset!")

    # ==================================================
    # SCORE
    # ==================================================

    def update_score(self):
        self.score_label.config(
            text=f"Player: {self.player_score} | Computer: {self.computer_score} | Ties: {self.ties}"
        )


# ==================================================
# RUN
# ==================================================

root = tk.Tk()
app = PokerGUI(root)
root.mainloop() 
