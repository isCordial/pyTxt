import curses
import time

# Merely wipes the board, waits a few seconds, then returns it to its previous state
def main(stdscr):

    #### FUNCTIONS ####

    ## Get the current x-coordinate of the cursori
    def cursorX():
        return stdscr.getyx()[1]

    ## Get the current y-coordinate of the cursor
    def cursorY():
        return stdscr.getyx()[0]

    ## Initialize a list for storing our data that will be written to a file.
    ## This list will be a list of lists. Each individual list will contain the chars that make up a string.
    myText = [[]]

    ## Enable cursor
    curses.curs_set(1)

    ## Tracking variables for the current position of cursor
    ## IMPORTANT: curses uses (y, x) for coordinates. NOT the standard (x, y).
    curY = 0
    curX = 0

    ## Display all output on the screen
    # curses.echo()

    ## on/off switch for the while loop
    isRunning = True
    key = 0

    while(isRunning == True):
        curY = cursorY()
        ## set curX equal to the length of this line's text
        curX = cursorX()


        ## wait for user input
        key = stdscr.getch()

        ## if backspacing...
        if key == curses.KEY_BACKSPACE or key == 127:

            ## if no text is on current line, move cursor to previous line
            if curX == 0:

                ## if greater than 0, move line up
                if curY > 0:
                    ## pop the line's string off the list
                    myText.pop()
                    curY -= 1
                    ## set X-coord equal to length of this line's string
                    curX = len(myText[curY])
                    stdscr.move(curY, curX)

                ## else do nothing
                else:
                    continue


            ## else, pop the last element from the current line's string and move cursor
            else:
                myText[curY].pop()
                curX -= 1
                ## delete char from screen and move cursor
                stdscr.move(curY, curX)
                stdscr.delch(curY, curX)

        ## compare ASCII key value to that of our quit-key
        elif key == ord("q"):
            ## if quit-key is pressed, exit program
            isRunning = False


        ## if we press ENTER or Down Arrow, move cursor down a line
        elif key == curses.KEY_ENTER or key == curses.KEY_DOWN or key == 10:
            curY += 1
            ## if there is nothing on this line, add an empty string list
            if len(myText) - 1 < curY:
                myText.append([])

            curX = len(myText[curY])

            ## update cursor
            stdscr.move(curY, curX)

        ## else, just append the key to the current line's string
        else:
            curX += 1
            myText[curY].append(chr(key))

            ## display the characters on-screen
            stdscr.addch(cursorY(),cursorX(),key)


    curses.beep()
    curses.endwin()
    return myText

## returns a list of lists. this represents a text file with multiple lines each containing a string of text
text = curses.wrapper(main)
for line in text:
    print(''.join(line))
