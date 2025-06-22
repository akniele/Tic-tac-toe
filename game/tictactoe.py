import numpy as np
import pandas as pd

"""
In this file, the Player class and the TicTacToe class are defined. 

A quick note on the game board as defined in the TicTacToe class: the datastructure used for this board is a NumPy array.
This makes it easy to check if a player has won the game (by summing over the rows, columns, and diagonals).

Player 1's tiles are represented as 1's on the game board, player 2's tiles as -1's, and empty tiles as 0's. 
This means that if the sum of any row, column or diagonal is 3, player 1 has won, while if the sum is -3, player 2 has won.

One could have also used a nested list instead of a NumPy array for this. 
However, using the vectorized methods of NumPy arrays tends to be more time-efficient.
"""

class Player:
    def __init__(self, id, symbol, tile_value):
        self.score = 0  # keeps track of the number of times the player has won
        self.id = id  # id that uniquely identifies the player
        self.symbol = symbol  # symbol that is shown on the game board
        self.tile_value = tile_value # tile value is 1 for the first player and -1 for the second player

    def get_player_score(self):
        return self.score
    
    def increase_player_score(self):
        self.score += 1


class TicTacToe:
    def __init__(self, size): # size is a tuple (x,y) where x = y
        # check if size fulfills requirements:
        assert isinstance(size, tuple)  # is a tuple
        assert len(size) == 2  # has length 2 (because two-dimensional board)
        assert size[0] == size[1]  # both sides have same length

        self.size = size
        self.to_win = float(size[0]) # the number of tiles you need to have in a row to win
        self.board = np.zeros(self.size) # initialize board with all zeros
        self.players = []
        self.current_player = None

    def add_player(self, new_player): # add new players to the game
        if len(self.players) == 0:
            self.current_player = new_player # set first added player as the current player to start with

        if len(self.players) == 2:
            print("You already have two players, so you can't add any more!")
    
        else:
            self.players.append(new_player)

            # check if all player ids are unique
            player_ids = [player.id for player in self.players]
            assert len(player_ids) == len(set(player_ids)) 

            # check if all player symbols are unique
            player_symbols = [player.symbol for player in self.players]
            assert len(player_symbols) == len(set(player_symbols))


    def update_game_board(self, row, column, player):  # update game board after a move has been made
        if self.players.index(player) == 0:
            self.board[row, column] = 1  # player 1's tiles are represented with 1's
        elif self.players.index(player) == 1:
            self.board[row, column] = -1  # player 2's tiles are represented with -1's
        else:
            print("This is not meant to happen, check code.")
        return self.board
    
    
    def reset_game_board(self):
        self.board = np.zeros(self.size) # remove all tiles from the board for new game
    

    def prettify_board(self):
        df_board = pd.DataFrame(self.board)  # get a pandas dataframe of the game board for printing to the terminal
        
        def noughts_and_crosses(x):
            x = x.replace(0.0, " ").replace(self.players[0].tile_value, self.players[0].symbol).replace(self.players[1].tile_value, self.players[1].symbol)  # replace 1's and -1's with the players' symbols
            return x

        df_board = df_board.apply(noughts_and_crosses)
        return df_board
    

    def get_current_score(self):
        vertical_sums = self.board.sum(axis=0)  # sum up the numbers of the tiles vertically
        horizontal_sums = self.board.sum(axis=1) # sum up the numbers of the tiles horiontically
        diagonal_sum_1 = self.board.diagonal().sum()  # sum up the numbers of the tiles of the principal diagonal (upper left to lower right)
        diagonal_sum_2 = np.fliplr(self.board).diagonal().sum() # sum up the numbers of the tiles of the secondary diagonal (upper right to lower left)

        if (self.to_win in vertical_sums) or (self.to_win in horizontal_sums) or (diagonal_sum_1 == self.to_win) or (diagonal_sum_2 == self.to_win):
            return "player 1 wins" # player 1 wins if they have filled a full row/column/diagonal with their tiles
        elif (-self.to_win in vertical_sums) or (-self.to_win in horizontal_sums) or (diagonal_sum_1 == -self.to_win) or (diagonal_sum_2 == -self.to_win):
            return "player 2 wins" # player 2 wins if they have filled a full row/column/diagonal with their tiles
        elif 0.0 in self.board:
            return "continue" # if no one has won yet and there is still an empty spot left on the board, we continue the game
        else:
            return "done"  # no more empty spots -> game is done
        

    def parse_user_input(self, user_input_row, user_input_column): # make sure user typed in valid input (a number in the right range)
    
        user_input_options = [str(i) for i in range(self.size[0])]

        if (user_input_row in user_input_options) and (user_input_column in user_input_options):
            row = int(user_input_row)
            column = int(user_input_column)
            if self.board[row, column] == 0.0:
                return row, column
            else:
                print("This slot is already filled! Choose a different one.")
                return -1, -1 
        else:
            print(f"Please type one of {list(range(self.size[0]))} (and nothing else!) when asked for a row or column number.")   
            return -1, -1 


    def play_game(self):
        # the game will continue until the final state has been reached (namely that the players don't want to play anymore)
        final_state = False

        # the game loop
        while not final_state:
            print(f"This is the current state of the game board:\n{self.prettify_board()}")
            print(f"It is player {self.current_player.id}'s turn!")

            # get user input: first the row number, then the column number that they want to put a tile into
            user_input = False
            while not user_input:
                user_input_row = input("Type the row you want as a number: ")
                user_input_column = input("Type the column you want as a number: ")
                row, column = self.parse_user_input(user_input_row, user_input_column) 
                if row in list(range(self.size[0])): # if the formatting the user used was correct, leave the loop
                    user_input = True

            # update the numpy array that keeps track of the players' scores
            self.update_game_board(row, column, self.current_player)

            # check if someone has won, if there are moves left to make, or if the board is full
            result = self.get_current_score()  

            # choose the player for the next turn (always the player who hasn't just had their turn)
            new_player_index = (self.players.index(self.current_player) + 1) % 2 
            self.current_player = self.players[new_player_index]  

            # check if one of the players has one, if there is a draw, or if the game can continue
            if result == "player 1 wins":
                self.players[0].increase_player_score()
                print(f"player {self.players[0].id} wins this round!")
            elif result == "player 2 wins":
                self.players[1].increase_player_score()
                print(f"player {self.players[1].id} wins this round!")
            elif result == "done":
                print("There is a draw!")
            else:
                print("Let's continue the game!")
                continue

            print(f"This is the final state of the game board:\n{self.prettify_board()}")

            #  check if the players want to play again. If yes, reset game board, else present final score of each player
            new_game = input("Do you want to play again? (y/n)")

            while new_game not in ["y", "n"]:
                new_game = input("Do you want to play again? Answer with 'y' or 'n'.")

            if new_game == "n":
                final_state = True
                print("Well played!")
                print(f"Final score Player {self.players[0].id}: {self.players[0].score}")
                print(f"Final score Player {self.players[1].id}: {self.players[1].score}")

            elif new_game == "y":
                self.reset_game_board()
                print("New game!")    