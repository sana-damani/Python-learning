# implementation of card game - Memory

import simplegui
import random
cardlist = range(0, 8) + range(0, 8)
exposed = []
found = []
num_exposed = 0
turns = 0

# helper function to initialize globals
def new_game(): 
    global exposed, num_exposed, found, turns
    random.shuffle(cardlist)
    exposed = [False for card in cardlist]
    found = [0 for x in range(0,8)]
    num_exposed = 0
    turns = 0
     
# define event handlers
def mouseclick(pos):
    global exposed, num_exposed, found, turns
    index = pos[0] // 50
    card = cardlist[index]
    if exposed[index] == False and found[card] < 2:
        turns += 1
        if num_exposed == 2:
            for i in cardlist:
                if found[i] == 1 and card != i:
                    found[i] = 0
            exposed = [False for i in cardlist]
            num_exposed = 0
        found[card] += 1
        exposed[index] = True
        num_exposed += 1
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global found
    x = 0
    y = 0
    index = 0
    label.set_text("Turns = " + str(turns))
    for card in cardlist:
        if exposed[index] == True or found[card] == 2:
            canvas.draw_polygon([(x, y), (x + 50, y), (x + 50, y + 100), (x , y + 100)], 1, "White", "Green")
            canvas.draw_text(str(card), (x + 25, y + 50), 20, "Black")
        else:
            canvas.draw_polygon([(x, y), (x + 50, y), (x + 50, y + 100), (x , y + 100)], 1, "White", "Black")
        x += 50
        index += 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
