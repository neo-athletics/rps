#!/usr/bin/env python3
import random
"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


class Player:
    def __init__(self):
        self.opponent_moves = []
        self.my_moves = []

    def move(self, *args):
        return 'rock'

    def learn(self, my_move, their_move):
        self.opponent_moves.append(their_move)
        self.my_moves.append(my_move)


class RockPlayer(Player):
    pass


class RandomPlayer(Player):
    def move(self,  *args):
        return random.choice(moves)


class ReflectPlayer(Player):
    # plays opponents last move on current round

    def move(self,  *args):
        # initial move should be random value
        round = args[0]

        if round == 1:
            return random.choice(moves)
        else:
            # continue with normal move
            return self.opponent_moves[len(self.opponent_moves) - 1]


class CyclePlayer(Player):
    # remembers what move it played last round

    def move(self,  *args):
        # initial move should be random value
        round = args[0]

        if round == 1:
            return random.choice(moves)
        else:
            # cycles through moves array starting from previous move

            index = moves.index(self.my_moves[-1]) + 1
            # check if last move is not out of range
            if len(moves) - 1 < index:
                # restart index to 0 and return first move else continue cycle
                index = 0
                return moves[index]
            else:
                return moves[index]


class HumanPlayer(Player):
    def move(self,  *args):
        movement = input("What will be your move rock, paper, scissors? \n")
        return self.valid_input(movement)

    def valid_input(self, movement):
        movement = movement.lower()

        if movement not in moves:
            return self.move()
        else:
            return movement


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        # score and rounds should be stored as instant variables
        self.score = {"p1": 0, "p2": 0}
        self.current_round = 1

    def get_rounds(self):
        rounds_per_game = input(("How many rounds will you like to play ?"
                                " Best of 1 or 3?\n"))

        if rounds_per_game == "1" or rounds_per_game == "3":
            rounds_per_game = int(rounds_per_game)
            return rounds_per_game
        else:
            return self.get_rounds()

    def keep_score_count(self, move1, move2):
        if beats(move1, move2):
            print(f"{move1} beats {move2} p1 wins")
            self.score["p1"] += 1
        elif beats(move2, move1):
            print(f"{move2} beats {move1} p2 wins")
            self.score["p2"] += 1
        else:
            print("It is a tie!")

    def play_round(self, round):
        move1 = self.p1.move()
        move2 = self.p2.move(round)

        print(f"Player 1: {move1}  Player 2: {move2}")

        self.keep_score_count(move1, move2)
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        print(f'Current score p1: {self.score["p1"]} and\
 p2: {self.score["p2"]}')

    def play_game(self):
        print("Game start!")
        game_rounds = self.get_rounds()
        rounds = game_rounds + 1
        points_to_win = None
        # reassign rounds to determine winner based on best out of 3 or 1
        if game_rounds == 3:
            points_to_win = game_rounds - 1
        else:
            points_to_win = 1

        while((points_to_win != self.score["p1"])
                and (points_to_win != self.score["p2"])):
            print(f"Round {self.current_round}:")
            self.play_round(self.current_round)
            # determine winner based on best out of number of rounds

            if points_to_win == self.score["p1"]:
                print("p1 wins")
            elif points_to_win == self.score["p2"]:
                print("p2 wins")

            self.current_round += 1

        print(f'Final score p1: {self.score["p1"]} and p2: {self.score["p2"]}')
        print("Game over!")


def setup_opponent():
    computer_player = input(("who will you like to play against a "
                            "rock, random, reflect or cycle player? \n"))

    # check if user chose valid input
    if computer_player in ["rock", "random", "reflect", "cycle"]:
        if computer_player == "rock":
            return RockPlayer()

        elif computer_player == "random":
            return RandomPlayer()

        elif computer_player == "reflect":
            return ReflectPlayer()

        elif computer_player == "cycle":
            return CyclePlayer()
    else:
        return setup_opponent()


if __name__ == '__main__':
    player_2 = setup_opponent()
    game = Game(HumanPlayer(), player_2)
    game.play_game()
