import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
import random
import seaborn as sns

folder = "fig"
if not os.path.exists(folder):
    os.makedirs(folder)

sns.set_theme(style="white", palette="pastel")
matplotlib.rcParams["axes.labelsize"] = 10
matplotlib.rcParams["axes.labelweight"] = "ultralight"
matplotlib.rcParams["figure.dpi"] = 300
matplotlib.rcParams["figure.figsize"] = (12, 6)
matplotlib.rcParams["font.family"] = "Helvetica Neue"
matplotlib.rcParams["font.size"] = 10
matplotlib.rcParams["font.weight"] = "ultralight"


def format_dollars(x, pos):
    return "${:,.0f}".format(x)


formatter = ticker.FuncFormatter(format_dollars)


def betting_strategy(strategy, current_bet, previous_result):
    if strategy == "Martingala":
        if previous_result == 0:
            return 2 * current_bet
        return current_bet
    elif strategy == "Martingala invertida":
        if previous_result == 1:
            return 2 * current_bet
        return current_bet / 2
    elif strategy == "Constante":
        return current_bet
    elif strategy == "d'Alembert":
        if previous_result == 0:
            return current_bet + (current_bet * 0.1)
        return current_bet - (current_bet * 0.1)
    elif strategy == "Paroli":
        if previous_result == 1:
            return 2 * current_bet
        return current_bet
    else:
        return None


def roulette_payout(bet_type, bet_number, winning_number):
    if bet_type == "Straight up":
        if bet_number == winning_number:
            return 35
    elif bet_type == "Split":
        if bet_number in [
            winning_number - 1,
            winning_number + 1,
        ]:
            return 17
    elif bet_type == "Street":
        if bet_number in [
            winning_number - 1,
            winning_number,
            winning_number + 1,
        ]:
            return 11
    elif bet_type == "Square":
        if bet_number in [
            winning_number - 3,
            winning_number - 1,
            winning_number + 1,
            winning_number + 3,
        ]:
            return 8
    elif bet_type == "Six line":
        if bet_number in [
            winning_number - 4,
            winning_number - 3,
            winning_number - 1,
            winning_number,
            winning_number + 1,
            winning_number + 3,
            winning_number + 4,
        ]:
            return 5
    elif bet_type == "Column":
        if bet_number % 3 == winning_number % 3:
            return 2
    elif bet_type == "Dozen":
        if bet_number in range(
            (winning_number - 1) // 12 * 12 + 1,
            (winning_number - 1) // 12 * 12 + 13,
        ):
            return 2
    elif bet_type == "Even money":
        if bet_number % 2 == winning_number % 2:
            return 1
    return -1


def simulate(strategy, bet_types, starting_funds, max_num_bets):
    count = 0
    current_bet = starting_funds * 0.01
    funds = [starting_funds]
    previous_result = 1
    while count < max_num_bets and funds[-1] > 0:
        count += 1
        current_bet = betting_strategy(strategy, current_bet, previous_result)
        bet_type = random.choice(bet_types)
        bet_number = random.randint(0, 37)
        winning_number = random.randint(0, 37)
        payout = roulette_payout(bet_type, bet_number, winning_number)
        funds.append(funds[-1] + current_bet * payout)
        if payout > 0:
            previous_result = 1
        else:
            previous_result = 0
    return np.cumsum(funds) / np.arange(1, len(funds) + 1)


starting_funds = 10000

bet_types = [
    "Straight up",
    "Split",
    "Street",
    "Square",
    "Six line",
    "Column",
    "Dozen",
    "Even money",
]

iterations = [
    1,
    10,
    100,
    1000,
    10000,
]

strategies = [
    "Martingala",
    "Martingala invertida",
    "Constante",
    "d'Alembert",
    "Paroli",
]

for iteration in iterations:
    fig, ax = plt.subplots(figsize=(9, 6), nrows=1, ncols=1)
    for strategy in strategies:
        funds = simulate(strategy, bet_types, starting_funds, iteration)
        (line,) = plt.plot(funds, label=strategy)
        last_fund = funds[-1]
        last_index = len(funds) - 1
        ax.scatter(
            last_index,
            last_fund,
            marker="o",
            color=line.get_color(),
            s=10,
        )
    plt.legend()
    ax.yaxis.set_major_formatter(formatter)
    plt.savefig(f"fig/{iteration}_its.png")
