import simplegui

# define global variables
time = 0
success = 0
tries = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(time):
    ms = time % 10
    time = time / 10
    sec = time % 60
    min = time / 60
    if (min == 10):
        reset_handler()   	
    if (min < 10):
        min = "0" + str(min)
    else:
        min = str(min)        
    if (sec < 10):
        sec = "0" + str(sec)
    else:
        sec = str(sec)        
    ms = str(ms)        
    string = min + ":" + sec + "." + ms
    return string
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()

def stop_handler():
    global tries, success
    if (timer.is_running()):
        timer.stop()
        ms = time % 10
        tries += 1
        if (ms == 0):
            success += 1

def reset_handler():
    global time, tries, success
    time = 0
    success = 0
    tries = 0

# define event handler for timer with 0.1 sec interval
def timer_helper():
    global time
    time = time + 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(time), [225, 150], 25, "Red")
    canvas.draw_text(str(success) + "/" + str(tries), [450, 30], 24, "White")
    
# create frame
frame = simplegui.create_frame("Timer_Game", 500, 300)
timer = simplegui.create_timer(100, timer_helper)

# register event handlers
frame.set_draw_handler(draw_handler)
frame.add_button('Start', start_handler)
frame.add_button('Stop', stop_handler)
frame.add_button('Reset', reset_handler)

# start frame
frame.start()
