import simplegui
import random

guess_int = 0
secret_number = 0
allowed_guesses = 0
num_guesses = 0

# helper function to start and restart the game
def new_game(max):
    # initialize global variables used in your code here
    global secret_number, num_guesses
    secret_number = random.randrange(0, max)
    num_guesses = 0

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global allowed_guesses
    new_game(100)
    allowed_guesses = 7

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global allowed_guesses
    new_game(1000)    
    allowed_guesses = 10
    
def input_guess(guess):
    # main game logic goes here	
    global guess_int, num_guesses
    num_guesses += 1
    guess_int = int(guess)
    print "Guess was", guess_int
    if (guess_int == secret_number):
        print "Correct"
        return
    elif (guess_int < secret_number):
        print "Higher"
    else:
        print "Lower"         
    if (num_guesses == allowed_guesses):
        print "You lose!"
        new_game(100)
     
# create frame
frame = simplegui.create_frame("Guess", 200, 200)

# register event handlers for control elements and start frame
frame.add_input("input_guess", input_guess, 100)
frame.add_button("Range is [0,100)", range100, 100);
frame.add_button("Range is [0,1000)", range1000, 100);

# call new_game 
new_game(100)

# always remember to check your completed program against the grading rubric
frame.start()
