from game.tictactoe import TicTacToe, Player


if __name__ == "__main__":

    # you can change these if you like:
    player_1_name = "1"  # any string (preferably len >= 1) you like
    player_2_name = "2"  # any string (preferably len >= 1) you like

    player_1_symbol = "x"  # any string (preferably len == 1) you like
    player_2_symbol = "o"  # any string (preferably len == 1) you like

    game_board_size = (3,3)  # any tuple of length two with two identical integers

    # instantiate two players
    player_1 = Player(player_1_name, player_1_symbol, 1) # DON'T change the third parameter, it will break the game
    player_2 = Player(player_2_name, player_2_symbol, -1) # DON'T change the third parameter, it will break the game

    # create a game
    game = TicTacToe(game_board_size)

    # add the players to the game
    game.add_player(player_1)
    game.add_player(player_2)

    # start game loop
    game.play_game()