# Justin G. Fr. Michael Goetz CSS
# 4/9/2021
# A program for the class MazeGame which every level will be based off of

class MazeGame():
  def __init__(self, board, player_x, player_y, end_x, end_y, item_num):
    """The initialization of the class
    
    Keyword Arguments
    board -- the 2D list containing the layout of the current level
    player_x, player_y -- the x and y coordinates in the 2D list of where the player starts the level
    end_x, end_y -- the x and y coordinates in the 2D list of where the end of the level is
    item_num -- the amount of items the player can collect in the current level
    """

    self.board = board
    self.player_x = player_x
    self.player_y = player_y
    self.end_x = end_x
    self.end_y = end_y
    self.items_collected = 0
    self.item_num = item_num

  def print_board(self):
    """A function that will print the board/maze when it is called"""

    for row in self.board:

      # this is to prevent all the squares in the board being printed to one line
      print()
      for square in row:

        # printed this way to show each individual square of a row on the same line
        print(square, end=' ')

  def is_done(self):
    """Returns True if the level is done and False if the level is not done

    checks to see if the player's coordinates are the same as the end coordinates
    """

    if self.player_x == self.end_x and self.player_y == self.end_y:
      return True
    
    return False
  
  def item_collected(self):
    """Returns True if the player has picked up an item and False if the player has not picked up an item"""

    if self.board[self.player_x][self.player_y] == "📱" or self.board[self.player_x][self.player_y] == "🖥️" or self.board[self.player_x][self.player_y] == "💻":
        return True
    
    return False

  def can_move(self, direction):
    """Returns True if the player's move is not going into a wall or go outside the board's borders and False if the move will
    
    Keyword Arguments
    direction -- the direction that the player is trying to move in
    """

    # player coordinates are assigned to temporary variables so that if the move cannot be done it does not affect the real coordinates
    x = self.player_x
    y = self.player_y
    if direction == "right":
      y = self.player_y + 1
    elif direction == "left":
      y = self.player_y - 1
    elif direction == "up":
      x = self.player_x - 1
    elif direction == "down":
      x = self.player_x + 1

    # if the move is within the bounds of the board and is into an empty square or into an item then the move can be performed
    if x >= 0 and x < len(self.board) and y >= 0 and y < len(self.board[0]):
      if self.board[x][y] == "⬛" or self.board[x][y] == "♻️" or self.board[x][y] == "📱" or self.board[x][y] == "🖥️" or self.board[x][y] == "💻":
        return True
    
    return False

  def move(self, direction):
    """Moves the player in the desired direction
    
    Keyword Arguments
    direction -- the direction the player wants to move in
    """

    # checking if the move can be performed
    if self.can_move(direction):

      # change the previous square to an empty space so that there the player model isn't in every place that the player was
      self.board[self.player_x][self.player_y] = "⬛"

      # changes the cooridinates based on the direction that the player is moving in
      if direction == "right":
        self.player_y = self.player_y + 1
      elif direction == "left":
        self.player_y = self.player_y - 1
      elif direction == "up":
        self.player_x = self.player_x - 1
      elif direction == "down":
        self.player_x = self.player_x + 1
      
      # checks if there is an item in the square that is about to be moved to before changing the space in that square to the player model so the items_collected is accurate at the end
      if self.item_collected():
        self.items_collected += 1
      self.board[self.player_x][self.player_y] = "🏃"
      self.print_board()

    # for when the can_move(direction) function returns False which means the player is trying to move somewhere they can't
    else:
      self.print_board()
      print("\nyou cannot move there, choose another direction and try again")
    
    # final check to see if the player has completed the level
    if self.is_done():
      print("\nyou beat the level, good job!")
      print(f"you collected {self.items_collected} / {self.item_num} items")
