import unittest
from game.tictactoe import TicTacToe, Player


# function for setting up game and players, to avoid repeating these lines in each test case
def set_up_game_and_players():
    game = TicTacToe((3,3))
    player_1 = Player("paul", "o", 1) 
    player_2 = Player("mary", "x", -1)

    game.add_player(player_1)
    game.add_player(player_2)

    return game


class TestTicTacToe(unittest.TestCase):
    def test_update_game_board(self):

        game = set_up_game_and_players()

        game.update_game_board(2, 2, game.players[0])  
        game.update_game_board(1, 1, game.players[1]) 

        self.assertEqual(game.board[2, 2], 1.0)
        self.assertEqual(game.board[1, 1], -1.0)
        self.assertEqual(game.board[0, 0], 0.0)


    def test_get_current_score_continue(self):

        game = set_up_game_and_players()

        """
        this configuration should result in continuation of play:
        x o
        

        """

        game.update_game_board(0, 0, game.players[0])  
        game.update_game_board(0, 1, game.players[1]) 

        result = game.get_current_score()

        self.assertEqual(result, "continue")



    def test_get_current_score_win(self):

        game = set_up_game_and_players()

        """
        this configuration should result in player 1 winning:
        x x x
        

        """

        game.update_game_board(0, 0, game.players[0])  
        game.update_game_board(0, 1, game.players[0]) 
        game.update_game_board(0, 2, game.players[0])
        
        result = game.get_current_score()

        self.assertEqual(result, "player 1 wins")


    def test_get_current_score_done(self):
        game = set_up_game_and_players()

        """
        this configuration should result in a draw:
        x o x
        x o x
        o x o
        """

        game.update_game_board(0, 0, game.players[0])  
        game.update_game_board(0, 1, game.players[1]) 
        game.update_game_board(0, 2, game.players[0])
        game.update_game_board(1, 0, game.players[0]) 
        game.update_game_board(1, 1, game.players[1])
        game.update_game_board(1, 2, game.players[0])
        game.update_game_board(2, 0, game.players[1])
        game.update_game_board(2, 1, game.players[0])
        game.update_game_board(2, 2, game.players[1])


        result = game.get_current_score()

        self.assertEqual(result, "done")



    def test_reset_game_board(self):

        game = set_up_game_and_players()

        # First simulate some moves
        game.update_game_board(2, 2, game.players[0])  # tile in third row, third column will get value 1
        game.update_game_board(1, 1, game.players[0])  # tile in second row, second column will get value 1

        self.assertEqual(game.board.sum(), 2.0)

        # Then reset game board
        game.reset_game_board()

        self.assertEqual(game.board.sum(), 0.0)



if __name__ == "__main__":
    unittest.main()