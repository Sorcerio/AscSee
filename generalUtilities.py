# General Utilities v1.0 for Python by Brody Childs
# Allows ease of use though providing generalized methods for commonly used Python code blocks.

# Imports
from time import time

# Configuration
TITLE_MARKER_LEFT = "["
TITLE_MARKER_RIGHT = "]"
CHECKBOX_INDICATOR = "X"

# Variables
CLOCKER_TIMES = {}

# Configuration Functions
# Allows the left Title Marker to be set to a custom character
def setTitleMarkerLeft(marker):
    # Scope the global
    global TITLE_MARKER_LEFT

    # Change the marker
    TITLE_MARKER_LEFT = marker

# Allows the right Title Marker to be set to a custom character
def setTitleMarkerRight(marker):
    # Scope the global
    global TITLE_MARKER_RIGHT

    # Change the marker
    TITLE_MARKER_RIGHT = marker

# Allows the Checkbox 'checked' Indicator to be set to a custom character
def setCheckboxIndicator(indicator):
    # Scope the global
    global CHECKBOX_INDICATOR

    # Change the checkbox indicator
    CHECKBOX_INDICATOR = indicator

# Functions
# Ask the user to input a valid answer and returns the choice once answered.
# query -> String to ask the user. Has ": " appened to its end
# validAnswers -> List of answer strings that are valid
# showChoices -> If the choices provided should be shown to the user by this function
def askUser(query, validAnswers, showChoices = True):
    # Build options string
    answers = str(validAnswers[0])
    for i in range(1, len(validAnswers)):
        answers += (", "+str(validAnswers[i]))
    
    # Show Options if applicable
    if showChoices:
        print("Choose one: "+answers)
    
    # Set to lowercase valid answers
    validAnswers = [str(answer).lower() for answer in validAnswers]

    # Enter query loop
    answer = None
    while answer == None or answer.lower() not in validAnswers:
        # Ask user for input
        answer = input(query+": ")

    # Return answer
    return answer

# Asks the user a yes or no question.
# query -> String to ask the user. Has ": " appened to its end
# boolean -> If the return value should be a boolean as opposed to a string
def askUserYesNo(query, boolean = False):
    # Check what mode
    if boolean:
        # Ask user
        answer = askUser(query, ["Yes","No"])

        # Check answer
        if answer.lower() == "yes":
            return True
        else:
            return False
    else:
        # Run standard questioning
        return askUser(query, ["Yes","No"])

# Prints and retains a menu system based on provided information leaving the calling program to decide function.
# title -> The title of the menu. Can also be supplied 'None' to have no title printed
# choices -> List of choice titles for the menu
def presentTextMenu(title, choices):
    # Check if title should be printed
    if title != None and title.strip() != '':
        # Print title
        print(TITLE_MARKER_LEFT+" "+title+" "+TITLE_MARKER_RIGHT)

    # Print Menu
    index = 0
    numberList = []
    for choice in choices:
        # Print choice
        print("["+str(index)+"] "+choice)

        # Add choice to number list
        numberList.append(index)

        # Iterate
        index += 1

    # Print instructions
    print("Enter a number to choose the option.")
    
    # Ask user for choice and return
    return askUser("Choice", numberList, False)

# Asks for user input while watching for an exit phrase that if entered returns a 'None' object.
# query -> Question to ask the user for input on. Has ": " appended to it
# exitPhrase -> String to listen for to indicate no response
def managedInput(query, exitPhrase):
    # Display query
    print("Enter '"+str(exitPhrase)+"' to "+(str(exitPhrase).lower())+".")

    # Ask user for input
    answer = input(query+": ")

    # Check if exit phrase
    if answer.lower() == exitPhrase.lower():
        # Send exit tag
        return None
    else:
        # Send inputted answer
        return answer

# Asks for user input while waiting for some form of none empty input to be entered
# query -> Question to ask the user for input on. Has ": " appended to it
# blacklist -> Inputs that would qualify as a bad input. Has a default value
def managedInputForced(query, blacklist = [None, ""]):
    # Enter the input loop
    answer = blacklist[0]
    while(answer in blacklist):
        # Ask user for input
        answer = input(query+": ").strip()

    # Return the answer
    return answer

# Asks for user input of a number while watching for an exit phrase that if entered.
# Returns a 'None' object if canceled.
# query -> Question to ask the user for input on. Has ": " appended to it
# exitPhrase -> String to listen for to indicate no response
def managedInputNumber(query, exitPhrase):
    # Enter validation loop
    answer = None
    goodNumber = False
    while not goodNumber:
        # Get managed input
        answer = managedInput(query, exitPhrase)

        # Check if valid
        if answer != None:
            # Attempt to convert to int
            try:
                # Convert to number
                answer = int(answer)

                # Exit loop
                goodNumber = True
                break
            except ValueError:
                # Tell user to fix it
                print("'"+str(answer)+"' is not a number.")
        else:
            # Canceled, break loop
            break

    # Check final verdict
    if goodNumber:
        return answer
    else:
        return None

# Asks for user input while waiting for some form of none empty input that can be converted to an int to be entered
# query -> Question to ask the user for input on. Has ": " appended to it
# blacklist -> Inputs that would qualify as a bad input. Has a default value
def managedInputNumberForced(query, blacklist = [None, '']):
    # Enter the input loop
    answer = blacklist[0]
    while answer in blacklist:
        # Ask user for input
        answer = input(query+": ").strip()

        # Attempt to convert to int
        try:
            # Convert to number
            answer = int(answer)

            # If success, break out
            break
        except ValueError:
            # Tell user to fix it
            print("'"+str(answer)+"' is not a number.")

            # Reset the answer
            answer = blacklist[0]

    # Return the valid number
    return answer

# Asks for user input of a number while watching for an exit phrase that if entered.
# Returns a 'None' object if canceled.
# query -> Question to ask the user for input on. Has ": " appended to it
# maxNumber -> The maximum number that would be considered valid (inclusive)
# minNumber -> The minimum number that would be considered valid (inclusive)
# exitPhrase -> String to listen for to indicate no response
def managedInputNumberRange(query, maxNumber, minNumber, exitPhrase):
    # Enter validation loop
    answer = None
    withinRange = False
    while not withinRange:
        # Get input
        answer = managedInputNumber(query, exitPhrase)

        # Check if valid
        if answer != None:
            # Check if within range
            if answer <= maxNumber and answer >= minNumber:
                # Within range
                withinRange = True
        else:
            # Canceled, break loop
            break
    
    # Final check
    if withinRange:
        return answer
    else:
        return None

# Prints a text menu and handles input between an accompanied execution function all within a handled loop.
# title -> The title of the menu
# choices -> List of choice titles for the menu
# lastOption -> Option to add to the last of the choices. Often 'Back' or 'Quit'
# func -> The function to call within the script that calls this function that uses the data gathered from this function
def textMenu(title, choices, lastOption, func):
    # Prep answer choice
    answer = None

    # Add last option to choices
    choices.append(lastOption)

    # Enter main loop
    while answer == None or answer != str(len(choices)-1):
        # Present main menu and wait for input
        print("")
        answer = presentTextMenu(title, choices)

        # Apply answer to main menu functions
        func(answer)

# Example of the method the 'textMenu()' function is looking for in the 'func' parameter.
# This can be used as a template and for learning to understand the process of the 'textMenu()' function.
def exampleTextMenuFunction(answer):
    # Print the returned answer
    print("textMenu: "+str(answer))

# Prints a text menu and handles input between an accompanied execution function all within a handled loop.
# title -> The title of the menu
# choices -> List of choice titles for the menu
# lastOption -> Option to add to the last of the choices. Often 'Back' or 'Quit'
# func -> The function to call within the script that calls this function that uses the data gathered from this function
# package -> Data that is sent along with whatever choice is made to be used later
def textMenuWithPackage(title, choices, lastOption, func, package):
    # Prep answer choice
    answer = None

    # Add last option to choices
    choices.append(lastOption)

    # Enter main loop
    while answer == None or answer != str(len(choices)-1):
        # Present main menu and wait for input
        print("")
        answer = presentTextMenu(title, choices)

        # Apply answer to main menu functions
        func(answer,package)

# Example of the method the 'textMenuWithPackage()' function is looking for in the 'func' parameter.
# This can be used as a template and for learning to understand the process of the 'textMenuWithPackage()' function.
def exampleTextMenuWithPackageFunction(answer, package):
    # Print the returned answer
    print("textMenu w/ package: "+str(answer)+" w/ "+str(package))

# Reads the entire contents of a file to memory and returns the content as a lumpsum string (good for JSON files, etc).
# fileName -> Name (or full address path if not in the working directory) of the file to read
def readFullFile(fileName):
    # Open the file
    with open(fileName, "r") as rFile:
        # Read and return the data
        return rFile.read()

# Writes the entire contents of the supplied text to the specified tile (good for JSON files, etc).
# fileName -> Name (or full address path if not in the working directory) of the file to write to. Be sure to include the file extension
# text -> The text to write to the file in one pass (can include new line, tab, etc characters)
def writeFullFile(fileName, text):
    # Open the file
    with open(fileName, "w") as wFile:
        # Write the text out
        wFile.write(text)

# DEPRECIATED: Prints and retains a checkbox based menu system based on provided information leaving the calling program to decide function.
# NOTE: It is recommend to use the pagedMultiSelect functions instead of this.
# title -> The title of the menu
# choices -> Dictionary of Choice Titles as keys and if the option is selected as Boolen for the value to be displayed by the menu
def presentCheckboxMenu(title, choices, silenceDepreciation = False):
    # Check if depreciation silenced
    if not silenceDepreciation:
        # Print the depreciation message
        print('presentCheckboxMenu(...) is depreciated. Check it\'s documentation for alternatives.')

    # Print title
    print(TITLE_MARKER_LEFT+" "+title+" "+TITLE_MARKER_RIGHT)

    # Print Menu
    index = 0
    numberList = []
    for choice in choices:
        # Check if the last item
        if index == (len(choices)-1):
            # Print choice as a regular option
            print("["+str(index)+"] "+choice)
        else:
            # Decide if the choice is checked or not
            checkIndicator = " "
            if choices[choice]:
                checkIndicator = CHECKBOX_INDICATOR

            # Print choice as a checkbox option
            print("["+str(index)+"] ("+checkIndicator+") "+choice)

        # Add choice to number list
        numberList.append(index)

        # Iterate
        index += 1

    # Print instructions
    print("Enter a number to choose the option.")

    # Ask user for choice
    answer = askUser("Choice", numberList, False)

    # Get the choices' keys
    choiceKeys = list(choices.keys())

    # Get the key associated with the current answer
    answersKey = choiceKeys[int(answer)]

    # Mark the selected answer as checked
    if choices[answersKey]:
        choices[answersKey] = False
    else:
        choices[answersKey] = True

    # Ask user for choice and return
    return answer, choices

# DEPRECITATED: Prints a check box menu and handles input between an accompanied execution function all within a handled loop.
# NOTE: It is recommend to use the pagedMultiSelect functions instead of this.
# title -> The title of the menu
# choices -> Dictionary of Choice Titles as keys and if the option is selected as Boolen for the value to be displayed by the menu
# lastOption -> Option to add to the last of the choices. Often 'Back' or 'Quit'
# func -> The function to call within the script that calls this function that uses the data gathered from this function
def checkboxMenu(title, choices, lastOption, func, silenceDepreciation = False):
    # Check if depreciation silenced
    if not silenceDepreciation:
        # Print the depreciation message
        print('checkboxMenu(...) is depreciated. Check it\'s documentation for alternatives.')

    # Prep answer choice
    answer = None

    # Add last option to choices
    choices[lastOption] = False

    # Enter main loop
    while answer == None or answer != str(len(choices)-1):
        # Present main menu and wait for input
        print("")
        answer, choices = presentCheckboxMenu(title, choices)

        # Apply answer to main menu functions
        func(answer)

# Starts a clocker (a time tracker) for the provided key that will remain in memory until it is requested
#   with the endClocker(...) function.
# key -> A unique string key that this specific clocker will be referenced by
# message -> A string message to display once the clocker starts. Can also supply None or an empty string
#               to display nothing.
def startClocker(key, message = 'Started clocking.'):
    # Scope the global
    global CLOCKER_TIMES

    # Add the current time to the log
    CLOCKER_TIMES[str(key)] = time()

    # Check if message was supplied
    if message != None and message != '':
        # Print the message
        print(message)

# Finishes a clocker (a time tracker) started by the startClocker(...) function and, by default, removes
#   the now used clocker from memory. Then returns and, optionally, prints the time ellapsed in the format
#   (by default) of '# Days, # Hours, # Minutes, # Seconds'. If a value of time is 0, it will not be show.
#   If a value of time is 1, it's textual representation with lack the trailing 's'.
# key -> A unique string key that this specific clocker will be referenced by
# message -> A string message to display once the clocker starts. Can also supply None or an empty string
#               to display nothing. Remember to end you message with a space if you want to seperate it
#               visually from the clocker string
# seperator -> A string to seperate the time string if printed.
# retain -> Boolean that if true keeps the clocker for the provided key in memory for future reference.
def endClocker(key, message = 'Completed in ', seperator = ', ', retain = False):
    # Scope the global
    global CLOCKER_TIMES

    # Check to see if the key is in the clocker times
    if key in CLOCKER_TIMES:
        # Check if the key should be removed from clocker times
        timeStart = None
        if not retain:
            # Get the time for the key and remove it
            timeStart = CLOCKER_TIMES.pop(str(key), None)
        else:
            # Get the time for the key
            timeStart = CLOCKER_TIMES[str(key)]

        # Caculate the number of seconds between the start and now
        timeEllapsed = time()-timeStart

        # Calculate the number of days
        days = timeEllapsed//86400

        # Calculate the number of hours
        hours = (timeEllapsed-days*86400)//3600

        # Calculate the number of minutes
        minutes = (timeEllapsed-days*86400-hours*3600)//60

        # Calculate the number of seconds
        seconds = timeEllapsed-days*86400-hours*3600-minutes*60

        # Prepare the time string
        outTime = ''

        # Add the days if needed
        if days > 0:
            # Add the days text
            outTime += ('%.0f day' %  days)

            # Check if an S is needed
            if days != 1:
                outTime += 's'

            # Add the seperator
            outTime += seperator

        # Add the hours if needed
        if hours > 0:
            # Add the hours text
            outTime += ('%.0f hour' %  hours)

            # Check if an S is needed
            if hours != 1:
                outTime += 's'

            # Add the seperator
            outTime += seperator

        # Add the minutes if needed
        if minutes > 0:
            # Add the minutes text
            outTime += ('%.0f minute' %  minutes)

            # Check if an S is needed
            if minutes != 1:
                outTime += 's'

            # Add the seperator
            outTime += seperator

        # Add the seconds if needed
        if seconds > 0:
            # Add the seconds text
            outTime += ('%.2f second' %  seconds)

            # Check if an S is needed
            if seconds != 1:
                outTime += 's'

            # Add the seperator
            outTime += seperator

        # Check if a message was supplied
        if message != None and message != '':
            # Print the message with the out time
            print(message+outTime)

        # Return the values
        return (days, hours, minutes, seconds)
    else:
        # Report the problem
        print('GeneralUtlities: No clocker exists for the key, \''+str(key)+'\'')

# Allows the user to select multiple options from a provided list of choices that are displayed in a pageinated
#   fashion for easy reading. Returns a list of the selected answers, or None if a cancelOption was provided and
#   the user chooses it.
# title -> The title of the menu. Can also be supplied 'None' to have no title printed
# choices -> A list of the possible choices. Ensure your choices do not have the same String as any of your
#   values for the various options!
# confirmOption -> The text shown for the option that confirms the current selection
# perPage -> Indicates how many items shown per page
# minSelect -> The minimum number of items that need to be selected for a valid return
# maxSelect -> The maximum number of items that can be selected for a valid return. Supply -1 if there should be no limit
# cancelOption -> The text shown for the option that cancels input. If None is provided, no cancel option is shown
# nextOption -> The text shown for the option that allows movement to the next page
# prevOption -> The text shown for the option that allows movement to the previous page
# allowSearch -> If the user is allowed to used the search action. Search is generally not needed for very short choice lists,
#   but is extremely helpful for long ones
def presentPagedMultiSelect(title, choices, confirmOption, perPage = 8, minSelect = 1, maxSelect = -1, cancelOption = None, nextOption = 'Next Page', prevOption = 'Prev Page', allowSearch = True):
    # Bound the select boundries
    if minSelect <= 0:
        minSelect = 1

    if maxSelect != -1 and maxSelect < minSelect:
        maxSelect = minSelect

    # Establish the search option
    searchOption = ':Search'

    # Prepare the selected answers list
    answers = []

    # Split the choices into paged clumps
    choices = [choices[i*perPage:(i+1)*perPage] for i in range((len(choices)+perPage-1)//perPage)]

    # Enter the input loop
    finished = False
    curPage = 0
    while not finished:
        # Check if what type of status needs to be printed
        selectStatus = ''
        if len(answers) >= minSelect:
            # Check if a max is set
            if maxSelect != -1:
                # Show the current out of max
                selectStatus = ('Selected '+str(len(answers))+'/'+str(maxSelect))
            else:
                # Show the current selected
                selectStatus = ('Selected '+str(len(answers)))
        elif minSelect != 0:
            # Show the at least select amount text
            selectStatus = ('Select at least '+str(minSelect))

        # Check if title should be printed
        if title != None and title.strip() != '':
            # Print the title
            print(TITLE_MARKER_LEFT+" "+title+" "+TITLE_MARKER_RIGHT)

        # Print the page and selection information
        print('Page '+str(curPage+1)+' of '+str(len(choices)))
        print(selectStatus+': '+(', '.join(answers) if len(answers) > 0 else 'None'))

        # Copy the current page choices
        curChoices = choices[curPage].copy()

        # Check if not on the last page
        if curPage < (len(choices)-1):
            # Add the next page option
            curChoices.append(':'+str(nextOption))

        # Check if not on the first page
        if curPage > 0:
            # Add the previous page option
            curChoices.append(':'+str(prevOption))

        # Check if search is enabled
        if allowSearch:
            # Add the search option
            curChoices.append(searchOption)

        # Add the confirm option
        curChoices.append(':'+str(confirmOption))

        # Check if a cancel option was provided
        if cancelOption != None and cancelOption.strip() != '':
            # Add the cancel option
            curChoices.append(':'+str(cancelOption))

        # Present a text menu with the current options
        choice = int(presentTextMenu(None, curChoices))

        # Get the actual choice text from the option
        choice = curChoices[choice]

        # Decide what to do with the choice
        if choice == (':'+str(confirmOption)):
            # Check if the minimum amount of items has been selected
            if len(answers) >= minSelect:
                # Mark as finished
                finished = True
                break
            else:
                # Tell the user they need to select more
                print('\n'+str(minSelect)+' item'+('s' if minSelect != 1 else '')+' must be selected.\n')
        elif choice == (':'+str(cancelOption)):
            # Set the answers to None
            answers = None

            # Mark as finished
            finished = True
            break
        elif choice == (':'+str(nextOption)):
            # Iterate to the next page
            curPage += 1
        elif choice == (':'+str(prevOption)):
            # Iterate to the previous page
            curPage -= 1
        elif allowSearch and choice == searchOption:
            # TODO: Allow the user to search
            pass
        else:
            # Check if choice is in answers
            if choice in answers:
                # Remove the choice from answers
                answers.remove(choice)
            else:
                print(maxSelect)
                # Check if above the max items
                if maxSelect != -1 and len(answers) >= maxSelect:
                    # Report the issue
                    print('\nOnly '+str(maxSelect)+' items can be selected!\n')
                else:
                    # Add the selected to the answers list
                    answers.append(choice)

    # Return the selected answers
    return answers

# Presents the user with a search bar
# options -> The options to search within
def presentSearchInput(options):
    # Enter the action loop
    answer = None
    while True:
        # Ask the user for a query
        query = managedInputForced('Search '+str(len(options))+' items')

        # Get the items that are similar in string form
        results = [option for option in options if query.lower() in str(option).lower()]

        # Add the search again option
        results.append(':Search Again')

        # Ask the user if any of the results are what they want
        answerIndex = int(presentTextMenu(None, results))

        # Check if a selected answer
        if answerIndex != (len(results)-1):
            # Set the answer and exit
            answer = results[answerIndex]
            break

    # Return the selected answer
    return answer
