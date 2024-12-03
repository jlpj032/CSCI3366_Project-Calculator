# Module: pretty 
# # This is where all the functions for handling the UI goes
import curses
import MathScanParse

helpoutput = "how to format?\n   each expression should be seperated by an operator, to avoid ambiguity this program doesn't support multiplication by juxtaposition 3(2+1) is not valid but 3*(2+1) is.\n\nWhat symbols should I use?\n   addition uses a + sign, subtraction uses a - sign\n   multiplication uses a *, division uses a / \n   exponenets uses ^\n\nWhere are my roots?\n   to do square root or similar roots you would need to do 4^(1/2). any root you just do the inverse as an expononet.\n\n What is the order of opperations? \n This program USES GEMA which would be Groupings aka paranthesis, Exponents, Multiplication, and Addition. \n\nfor trig functions such as sin, cos, etc you can change between DEG and RAD by simply typing that as the input\n program starts with RAD as default.\n\n pi and e are variables that are built in, they can be used by typing pi or e. \n  example: pi*3^2 \n 3 * e"

# might end up using this
def init_colors():
    curses.start_color()

    # Initialize color pairs
    #                        Text            Background
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)

def round_if_float(num):
    if isinstance(num, float):  # Check if num is a float
        return round(num, 4)  # Round to 4 decimal points
    return num  # Return the number unchanged if it's not a float

def calc_screen(stdscr):
    inputSym = ">> "
    printSym = True
    input_history = []
    curr_his_pos = 0
    user_input = ""
    currX = 3
    currY = 0
    
    stdscr.clear()
    
    stdscr.scrollok(True)  # Enable automatic scrolling
    stdscr.idlok(True)     # Enable line insertion and deletion
    
    while True:
        height, width = stdscr.getmaxyx()  # Get screen size

        if printSym:
            if currY == 0 and currX == 3:
                stdscr.addstr(0, 0, inputSym)
                curses.curs_set(1)  # Show cursor
                stdscr.move(currY, currX)
                printSym = False
            else:
                currY += 1
                currX = 3
                stdscr.addstr(currY, 0, inputSym)
                stdscr.move(currY, currX)
                printSym = False

        key_input = stdscr.getch()  # Get user input
        
        # Handle screen resize
        if key_input == curses.KEY_RESIZE:
            pass
        # Handle UP key to navigate input history
        elif key_input == curses.KEY_UP:
            if len(input_history) != 0:
                if curr_his_pos != 0:
                    curr_his_pos -= 1
                stdscr.move(currY, 3)
                stdscr.addstr(" " * len(user_input))  # Clear previous input
                stdscr.move(currY, 3)
                stdscr.addstr(input_history[curr_his_pos])
                currX = 3 + len(input_history[curr_his_pos].strip())
                user_input = input_history[curr_his_pos]
        # Handle DOWN key to navigate input history
        elif key_input == curses.KEY_DOWN:
            if len(input_history) != 0:
                if curr_his_pos != len(input_history):
                    curr_his_pos += 1
                if curr_his_pos == len(input_history):
                    stdscr.move(currY, 3)
                    stdscr.addstr(" " * len(user_input))  # Clear previous input
                    stdscr.move(currY, 3)
                    currX = 3
                    user_input = ""
                elif curr_his_pos < len(input_history):
                    stdscr.move(currY, 3)
                    stdscr.addstr(" " * len(user_input))  # Clear previous input
                    stdscr.move(currY, 3)
                    stdscr.addstr(input_history[curr_his_pos])
                    currX = 3 + len(input_history[curr_his_pos])
                    user_input = input_history[curr_his_pos]
        # Handle special keys like RIGHT, LEFT, BACKSPACE
        elif key_input == curses.KEY_RIGHT:
            if currX < len(user_input) + 3:
                currX += 1
            stdscr.move(currY, currX)
        elif key_input == curses.KEY_LEFT:
            if currX > 3:
                currX -= 1
            stdscr.move(currY, currX)
        elif key_input == curses.KEY_BACKSPACE:
            if currX != 3:
                stdscr.addstr(currY, 3, " "* len(user_input))
                user_input = user_input[:currX-4] + user_input[currX-3:]
                stdscr.addstr(currY, 3, user_input)
                currX -= 1
                stdscr.move(currY, currX)
        elif key_input == 10 and user_input.strip() != "":  # Enter key pressed
            if user_input.lower().strip() == "exit":
                break
            elif user_input.lower().strip() == "help":
                currY += 1
                currX = 0
                stdscr.move(currY, currX)
                stdscr.addstr(helpoutput)
                input_history.append(user_input)
                curr_his_pos = len(input_history) 
                user_input = ""
                y, x = stdscr.getyx()
                currY = y
                printSym = True
            elif user_input.lower().strip() == "deg":
                currY += 1
                currX = 0
                if MathScanParse.RAD == False: 
                    stdscr.addstr(currY, currX, "is Already in DEG mode")
                else:
                    stdscr.addstr(currY, currX, "updated to DEG mode")
                    MathScanParse.RAD = False
                input_history.append(user_input)
                curr_his_pos = len(input_history) 
                user_input = ""
                printSym = True
            elif user_input.lower().strip() == "rad":
                currY += 1
                currX = 0
                if MathScanParse.RAD == True: 
                    stdscr.addstr(currY, currX, "is Already in RAD mode")
                else:
                    stdscr.addstr(currY, currX, "updated to RAD mode")
                    MathScanParse.RAD = True
                input_history.append(user_input)
                curr_his_pos = len(input_history) 
                user_input = ""
                printSym = True 
            else:
                currY += 1
                currX = 0
                try:
                    foundTokens = MathScanParse.scan(user_input)
                    parser = MathScanParse.Parser(foundTokens)
                    parse_tree = parser.parse()
                    evaluation = round_if_float(parser.evaluate(parse_tree))
                    stdscr.move(currY, currX)
                    input_history.append(user_input)
                    input_history.append(str(evaluation))
                    stdscr.addstr(str(evaluation))
                    y, x = stdscr.getyx()
                    currY = y
                except ZeroDivisionError:
                    stdscr.addstr(currY, currX, "Error: Tried dividing by zero")
                except ValueError as e:
                    stdscr.addstr(currY, currX, f"Error: {e}")
                except Exception:
                    stdscr.addstr(currY, currX, "Something went wrong make sure you have propper syntax. type \"help\" if you need more information")
            
                printSym = True
                user_input = ""
                curr_his_pos = len(input_history)
                    
        else:  # Handle regular key input (e.g., typing)
            if currX != len(user_input)+3:
                stdscr.addstr(currY, 3, " "*len(user_input))
                user_input = user_input[:currX-3] + chr(key_input) + user_input[currX-3:]
                stdscr.addstr(currY, 3, user_input)
            else:
                stdscr.addstr(currY, currX, chr(key_input))
                user_input += chr(key_input)

            currX += 1
            stdscr.move(currY, currX)

        # If the content exceeds the window height, scroll automatically
        if currY >= height - 1:  # If the screen is full
            stdscr.scroll()  # This scrolls the window content up
            currY = height - 2  # Adjust cursor position after scroll

        stdscr.refresh()  # Refresh the screen to update the UI

def start_screen(stdscr):
    # Write a welcome message at the center of the screen
    message = "Welcome to the Calculator App!"
    names = "By Jose Pliego & Travis Shows"
    secondMessage = "Press any key to continue..."
    while True:
        stdscr.clear()
        curses.curs_set(0)
        init_colors()
        # Get the screen height and width
        height, width = stdscr.getmaxyx()

        x_pos = width // 2 - len(message) // 2
        y_pos = height // 2
        stdscr.addstr(y_pos, x_pos, message)
        stdscr.addstr(y_pos + 1, x_pos + (len(message)//2 - len(names) // 2), names) 
        stdscr.addstr(y_pos + 3, x_pos + (len(message)//2 - len(secondMessage)//2), secondMessage)

        # Refresh the screen to show the message
        stdscr.refresh()

        # Wait for user input before exiting
        sinput = stdscr.getch() 

        if sinput != curses.KEY_RESIZE:
            calc_screen(stdscr) 
            break
