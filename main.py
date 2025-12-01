# Justin G. Fr. Michael Goetz CSS
# 4/9/2021
# A program that lets the user play a game related to E-Waste Recycling and then allows the user to locate an E-Waste Recycling Center in their city
import time
from maze import MazeGame
from blessed import Terminal
import googlemaps

def introduction():
    """The introduction to the game, with instructions and controls"""

    print("Welcome to The E-Waste Escapade!")
    print("Please go fullscreen!")
    time.sleep(3)
    print(
        "The goal of this game is to pick up recyclable E-Waste\non your way to the recycling center at the end of the maze"
    )
    time.sleep(6)

    print("The player you control looks like this: 🏃")
    time.sleep(1.5)
    print(
        "The recyclable items you need to pick up look like this: 📱 / 🖥️ / 💻")
    time.sleep(3)
    print("Your end goal, the recycling center, looks like this: ♻️")
    time.sleep(1.5)
    print("you control the player using the 'WASD' keys")
    time.sleep(4)

    print("\nThe first of three levels will begin shortly")
    time.sleep(2)
    print("\033c")


def load_level(board, level_num, level_size):
    """Loads the layout of a level into a 2D list

  reads from .txt files containing the layout of levels and appending each line to a 2D list
  Keyword Arguments
  board -- the 2D list which will contain each row of the level
  level_num -- the number indicating which level the function needs to load
  level_size -- the amount of rows in the level
  """

    with open('levels/level_' + level_num + '.txt', 'r') as level:

        # the amount of lines in the file determines how many rows/columns should be in the level
        for i in range(level_size):

            # gets the row and changes the black squares to spaces to match the expected input in the MazeGame object
            line = level.readline()  # .replace('⬛', ' ')

            # getting rid of new line escape keys to prevent printing the board wrong later
            line = line.replace('\n', '')

            # making each line a list by splitting where ever there is a '.', each line needs to be a list to match the expected input in the MazeGame object
            line = line.split('.')
            board.append(line)

        return board


def final_score(items_collected, total_items):
    """Returns an approximate percent of how many items the player collected the whole game
  
  Keyword Arguments
  items_collected -- the total amount of items the player collected
  total_items -- the total amount of items that the player was able to collect
  """

    return round(((items_collected / total_items) * 100), 1)


def intro_level(level_num, phone_num, monitor_num, laptop_num):
    """Gives introductory information about the current level
  
  Keyword Arguments
  level_num -- the number indicating what the current level is
  phone_num, monitor_num, laptop_num -- the amount of each item that is present in the current level
  """

    print(f"Welcome to Level {level_num}")
    time.sleep(1)
    print("lets get it started")
    time.sleep(1.25)
    print("\033c")

    print(
        f"find your way to the recycling center ( ♻️ ) and pick up these items on the way\n📱 (x{phone_num})\n🖥️ (x{monitor_num})\n💻 (x{laptop_num})"
    )
    time.sleep(3)
    print("\033c")


def play_level(board, start_x, start_y, end_x, end_y, item_num):
    """Allows a level to be played
  
  Keyword Arguments
  board -- the 2D list containing the layout of the current level
  start_x, start_y -- the x and y coordinates in the 2D list of where the player starts the level
  end_x, end_y -- the x and y coordinates in the 2D list of where the end of the level is
  item_num -- the amount of items the player can collect in the current level
  """
    # this object allows reading user input of a single key without needing to press enter
    term = Terminal()

    # made a global object to that the total items collected can be properly calculated later
    global maze
    maze = MazeGame(board, start_x, start_y, end_x, end_y, item_num)

    maze.print_board()
    while not maze.is_done():
        print()

        # reads user input of first key pressed without needing to press enter key
        with term.cbreak():
            move = term.inkey()

        # clears the screen from the previous board before printing the new board after key is pressed so that multiple boards arent on the screen at the same time
        print("\033c")

        # reads the user input and out puts accordingly
        if move == "w":
            maze.move("up")
        elif move == "a":
            maze.move("left")
        elif move == "s":
            maze.move("down")
        elif move == "d":
            maze.move("right")
        else:
            maze.print_board()
            print(
                "\ninvalid input!\nuse WASD keys to move up, left, down, and right\ntry again"
            )

    # to determine if the next level can be played
    if maze.is_done():
        return True


def get_api_key():
    api_key = ""
    try:
        with open("api_key.txt", "r") as api_file:
            api_key = api_file.readline().strip()
            return api_key
    except FileNotFoundError:
        print("api_key.txt does not exist, you must create your own API key through google maps platform")
        print("This program will exit")
        return api_key


def find_e_waste_center():
    """Finds an E-Waste Recycling Center based on a user inputted city"""

    # importing the google maps module in order to use the google maps api

    user_response = input(
        "Now that you have completed E-Waste Escapade, would you like to locate an E-Waste Recycling Center near you? "
    )

    # this variable is defaulted as False because if the user chooses not to locate a recycling center or their last search raised an error then an output without the results of their last search will be displayed at the end
    searched = False

    # input guard
    while user_response[0].lower() != "y" and user_response[0].lower() != "n":
        user_response = input("invalid input respond with 'y' or 'n': ")

    while user_response[0].lower() == "y":

        api_key = get_api_key()
        if not api_key:
            quit()

        # google maps client can only be used with an api key so this line is used to create the gmaps object using the api key
        gmaps = googlemaps.Client(
            key=api_key)
        user_city = input(
            "Enter the name of your city so we can find an E-Waste Recycling Center near you:\n"
        )

        # gmaps.find_place() expects arguments in this way (<the search in list form>, <the type of search being done>, <which information to return about the found place in list form>) and returns a dictionary
        try:
          
          search_result = gmaps.find_place(["e-waste recycling in " + user_city],
                                           "textquery",
                                           ["name", "formatted_address"])
        except (googlemaps.ApiError, googlemaps.TransportError, googlemaps.HTTPError, googlemaps.Timeout, TimeoutError):
          print("Looks like there is an API key error, try setting up your api key again")
          print("Anyways, thanks for playing!")
          quit()

        # the search result will have a status of 'OK' if the search was successful so if the status 'OK' is not in the returned results, then an error was raised and the user needs to submit a new input
        if not search_result["status"] == "OK":
            searched = False
            print("your search resulted in an error")
            user_response = input("would you like to retry? ")

            while user_response[0].lower() != "y" and user_response[0].lower(
            ) != "n":
                user_response = input(
                    "invalid input respond with 'y' or 'n': ")
            print("\033c")
        else:
            searched = True

            # formatting of the search result
            center_info = "\nName: " + search_result["candidates"][0][
                "name"] + "\nAddress: " + search_result["candidates"][0][
                    "formatted_address"]

            # even if the search was successful the result may be something the user wasn't looking for or, their original input had a typo or, they wish to search in a new city, this statment allows the user to submit a new input if they wish
            print(center_info)
            print(
                f"\nif '{user_city}' wasn't what you meant to search\nor if you want to search for another city you can try again.\nIf your search was inaccurate try the same search again but also with the name of your province/territory/state and/or country"
            )
            user_response = input("would you like to try again? ")
            while user_response[0].lower() != "y" and user_response[0].lower(
            ) != "n":
                user_response = input(
                    "invalid input respond with 'y' or 'n': ")
            print("\033c")

    # if the user wishes to exit and their last search brought up an error or they haven't searched at all then an empty line will be printed along with a final goodbye message
    if user_response[0].lower() == "n" and searched == False:
        return ""
    else:
        # if the user's last search didn't raise an error then they will see the results of their last search with the goodbye message
        print(
            f"Here is the result of your last search for E-Waste Recycling Centers in {user_city}"
        )
        return center_info


def main():
    """The main method"""

    # declaration of variables
    board_1 = []
    board_2 = []
    board_3 = []
    total_items = 0
    items_collected = 0
    load_level(board_1, "1", 20)
    load_level(board_2, "2", 25)
    load_level(board_3, "3", 30)

    introduction()
    intro_level(1, 1, 1, 1)
    if play_level(board_1, 1, 0, 18, 19, 3):
        print("Level two of three will begin shortly")

        # adding to the items collected/ total items variables so that a final score can be calculated later
        total_items += maze.item_num
        items_collected += maze.items_collected
        time.sleep(2)

        intro_level(2, 2, 1, 1)
        if play_level(board_2, 0, 12, 24, 12, 4):
            print("The final level will begin shortly")
            total_items += maze.item_num
            items_collected += maze.items_collected
            time.sleep(2)
            print("\033c")

            intro_level(3, 2, 1, 2)
            if play_level(board_3, 15, 0, 16, 29, 5):
                total_items += maze.item_num
                items_collected += maze.items_collected
                time.sleep(2)
                print("\033c")
                print("YOU WON!!!")
                print(
                    f"you collected {items_collected} out of {total_items}, so {final_score(items_collected, total_items)}% of the recyclable items were collected"
                )
                time.sleep(3)

    print(find_e_waste_center())
    print("")
    print(
        "\nThank You for using this program, hopefully you are now more aware of E-Waste Recycling Centers, Goodbye!"
    )


if __name__ == "__main__":
    main()

# resources used:
# ---MAZE---
# https://blessed.readthedocs.io/en/latest/api/terminal.html#blessed.terminal.Terminal.cbreak
# ---GOOGLE API---
# https://www.youtube.com/watch?v=qkSmuquMueA
# https://developers.google.com/maps/documentation/places/web-service/overview?hl=en_US
# https://googlemaps.github.io/google-maps-services-python/docs/
# https://cloud.google.com/maps-platform/user-guide/product-changes/#places
