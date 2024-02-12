import curses
import time

## Parses a designated file and returns its content
## as a list of lists
def parseFile(file):
    txtFile = []
    dirFile = "./" + file
    name = dirFile

    f = open(dirFile, "r")

    rawTxt = f.readlines()
    f.close()

    i = 0
    for line in rawTxt:
        txtFile.append([])
        for char in rawTxt[i]:
            txtFile[i].append(char)
        i += 1

    return txtFile

######################################


name = ''

## Prompt user for file to create / edit
def promptUser():

    ## Function for validating yes/no inputs
    def valInput():
        while True:
            try:
                f = input("--> ")
                if f != "y" and f != "n":
                    raise ValueError("Please input 'y' for Yes OR 'n' for No")
                elif f == "y":
                    return True
                else:
                    return False
            except ValueError as ve:
                print(ve)

    print("Welcome to pyTxt!")
    print("You can edit existing files, or create new one!")
    print("Are you editing an existing file? (y/n): ")
    a1 = valInput()
    if a1 == True:
        print("WARNING: Your file must be in the current directory.")
        name = input("Please enter the name of your file, including extension: ")
    else:
        print("Your file will be saved to the current directory.")
        name = input("Please enter the name of your file: ")
        with open(name, "w") as n:
            pass

    return name


## Instantiates curses window
def main(stdscr):

     # Get terminal size
    height, width = stdscr.getmaxyx()


    ## Get the current x-coordinate of the cursori
    def cursorX():
        return stdscr.getyx()[1]

    ## Get the current y-coordinate of the cursor
    def cursorY():
        return stdscr.getyx()[0]

    ## Initialize a list for storing our data that will be written to a file.
    ## This list will be a list of lists. Each individual list will contain the chars that make up a string.


    ## Enable cursor
    curses.curs_set(1)

    ## Tracking variables for the current position of cursor
    ## IMPORTANT: curses uses (y, x) for coordinates. NOT the standard (x, y).
    curY = 0
    curX = 0

    ## Display the file contents on the screen
    myText = parseFile(name)
    numLines = len(myText)
    if numLines < 1:
        myText.append([])
    else:
        for i in range(0, numLines):
            stdscr.move(i, 0)
            curY = i
            stdscr.addstr("".join(myText[i]))
        curX = len(myText[curY])
        stdscr.move(curY, curX)

    ## on/off switch for the while loop
    isRunning = True
    key = 0

    while(isRunning == True):
        curY = cursorY()
        ## set curX equal to the length of this line's text
        curX = cursorX()

        ## Window informing the user of how to exit
        warning_win = curses.newwin(1, width, height-1, 0)
        warning_win.addstr("Press 'q' to exit. Sorry about that.")
        warning_win.refresh()

        ## wait for user input
        key = stdscr.getch()

        ## if backspacing...
        if key == curses.KEY_BACKSPACE or key == 127:

            ## if no text is on current line, move cursor to previous line
            if curX == 0:

                ## if greater than 0, move line up, and del the trailing newline char
                if curY > 0:
                    ## pop the line's string off the list
                    myText.pop()
                    curY -= 1

                    ## set X-coord equal to length of this line's string
                    curX = len(myText[curY])

                    ## delete new line char, if it exists
                    if myText[curY][curX - 1] == "\n":
                        myText[curY].pop()
                        curX -= 1

                    ## update cursor
                    stdscr.move(curY, curX)

                ## else do nothing, maintain cursor position
                else:
                    stdscr.move(curY, curX)
                    continue


            ## else, pop the last element from the current line's string and move cursor
            else:
                if len(myText[curY]) > 0:
                    ## delete char from screen and move cursor
                    myText[curY].pop()
                    curX -= 1
                    stdscr.move(curY, curX)
                    stdscr.delch(curY, curX)

        ## compare ASCII key value to that of our quit-key
        elif key == ord("q"):
            ## if quit-key is pressed, exit program
            isRunning = False

        elif key == curses.KEY_UP or key == curses.KEY_RIGHT or key == curses.KEY_LEFT or key == curses.KEY_DOWN:
            continue

        ## if we press ENTER, move cursor down a line
        elif key == curses.KEY_ENTER or key == 10:
            myText[curY].append(chr(key))
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


    curses.endwin()
    return myText

## returns a list of lists. this represents a text file with multiple lines each containing a string of text

name = promptUser()
text = curses.wrapper(main)

## Write new changes to the file
f = open(name, "w")
for i in range(0, len(text)):
    f.write("".join(text[i]))

f.close()
print("Success! Saved to {}".format(name))

# for line in text:
#     print(''.join(line))
