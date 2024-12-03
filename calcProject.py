import curses
import MathScanParse
import pretty

Tokens = MathScanParse.Tokens 


if __name__ == '__main__':
    curses.wrapper(pretty.start_screen)
