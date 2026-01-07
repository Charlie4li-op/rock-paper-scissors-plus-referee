import random

USE_ADK = False
try:
    from google.adk.agents import Agent
    from google.adk.tools import Tool
    USE_ADK = True
except Exception:
    USE_ADK = False

game_state = {
    "round": 1,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False,
    "game_over": False
}

VALID_MOVES = ["rock", "paper", "scissors", "bomb"]

def validate_move(move: str):
    move = move.lower().strip()
    if move not in VALID_MOVES:
        return False, "Invalid move"
    if move == "bomb" and game_state["user_bomb_used"]:
        return False, "Bomb already used"
    return True, move


def resolve_round(user_move: str):
    bot_moves = ["rock", "paper", "scissors"]
    if not game_state["bot_bomb_used"]:
        bot_moves.append("bomb")

    bot_move = random.choice(bot_moves)

    if user_move == "bomb":
        game_state["user_bomb_used"] = True
    if bot_move == "bomb":
        game_state["bot_bomb_used"] = True

    winner = "draw"
    if user_move == "bomb" and bot_move != "bomb":
        winner = "user"
    elif bot_move == "bomb" and user_move != "bomb":
        winner = "bot"
    elif user_move != bot_move:
        if (
            (user_move == "rock" and bot_move == "scissors") or
            (user_move == "paper" and bot_move == "rock") or
            (user_move == "scissors" and bot_move == "paper")
        ):
            winner = "user"
        else:
            winner = "bot"

    return bot_move, winner


def update_game_state(winner):
    if winner == "user":
        game_state["user_score"] += 1
    elif winner == "bot":
        game_state["bot_score"] += 1

    game_state["round"] += 1
    if game_state["round"] > 3:
        game_state["game_over"] = True


def play_turn(user_input: str) -> str:
    if game_state["game_over"]:
        return "GAME OVER."

    valid, result = validate_move(user_input)
    round_no = game_state["round"]

    if not valid:
        game_state["round"] += 1
        if game_state["round"] > 3:
            game_state["game_over"] = True
        return f"❌ {result}. Round {round_no} wasted."

    bot_move, winner = resolve_round(result)
    update_game_state(winner)

    response = (
        f"🎮 Round {round_no}\n"
        f"You played: {result}\n"
        f"Bot played: {bot_move}\n"
        f"Winner: {winner.upper()}\n"
        f"Score → You {game_state['user_score']} : {game_state['bot_score']} Bot"
    )

    if game_state["game_over"]:
        if game_state["user_score"] > game_state["bot_score"]:
            final = "🏆 YOU WIN"
        elif game_state["user_score"] < game_state["bot_score"]:
            final = "🤖 BOT WINS"
        else:
            final = "⚖️ DRAW"
        response += f"\n\nGAME OVER\n{final}"

    return response


if USE_ADK:
    play_tool = Tool(
        name="play_turn",
        description="Validates move, resolves round, updates game state",
        func=play_turn
    )

    agent = Agent(
        name="RPS Plus Referee",
        instructions=(
            "Explain the rules in 5 lines or fewer.\n"
            "Then ask the user for a move.\n"
            "ALWAYS use the play_turn tool."
        ),
        tools=[play_tool]
    )


if __name__ == "__main__":
    print("🎮 Rock–Paper–Scissors–Plus")
    print("Rules:")
    print("• Best of 3 rounds")
    print("• Moves: rock, paper, scissors, bomb")
    print("• Bomb beats all, usable once")
    print("• Invalid input wastes round\n")

    while not game_state["game_over"]:
        user_input = input("Your move > ")

        if USE_ADK:
            output = agent.run(user_input)
        else:
            output = play_turn(user_input)

        print("\n" + output)
