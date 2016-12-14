# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT/2]
ball_vel = [0, 0]
score1 = 0
score2 = 0
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
game_over = False

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT/2]
    if direction == LEFT:
        ball_vel = [-random.randrange(1, 3), -random.randrange(2, 4)]
    else:
        ball_vel = [random.randrange(1, 3), -random.randrange(2, 4)]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, game_over  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [PAD_WIDTH/2, HEIGHT/2 - PAD_HEIGHT/2]
    paddle2_pos = [WIDTH - PAD_WIDTH/2, HEIGHT/2 - PAD_HEIGHT/2]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    game_over = False
    spawn_ball(LEFT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, game_over
    acc = 4
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    if not(game_over):
        
        # update ball
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # draw ball
        canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

        # update paddle's vertical position, keep paddle on the screen
        paddle1_pos[1] += paddle1_vel      
        if paddle1_pos[1] < 0:
            paddle1_pos[1] = 0
        elif paddle1_pos[1] > HEIGHT - PAD_HEIGHT:
            paddle1_pos[1] = HEIGHT - PAD_HEIGHT

        paddle2_pos[1] += paddle2_vel      
        if paddle2_pos[1] < 0:
            paddle2_pos[1] = 0
        elif paddle2_pos[1] > HEIGHT - PAD_HEIGHT:
            paddle2_pos[1] = HEIGHT - PAD_HEIGHT

        # draw paddles
        canvas.draw_line(paddle1_pos, [paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH, "White")
        canvas.draw_line(paddle2_pos, [paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH, "White")
    
        # check for collisions
        gutter_left = False
        gutter_right = False
        collision_left = False
        collision_right = False
        collision_top = False
        collision_bottom = False

        if (ball_pos[0] - BALL_RADIUS <= paddle1_pos[0]):
            if ball_pos[1] < paddle1_pos[1] or ball_pos[1] > paddle1_pos[1] + PAD_HEIGHT:
                gutter_left = True
            else:
                collision_left = True

        elif (ball_pos[0] + BALL_RADIUS >= paddle2_pos[0]):
            if ball_pos[1] < paddle2_pos[1] or ball_pos[1] > paddle2_pos[1] + PAD_HEIGHT:
                gutter_right = True
            else:
                collision_right = True

        if (ball_pos[1] - BALL_RADIUS <= 0):
            collision_top = True
        elif (ball_pos[1] + BALL_RADIUS >= HEIGHT):
            collision_bottom = True

        # update score and respawn if ball in gutter
        if gutter_left:
            score2 += 1
            if score2 < 5:
                spawn_ball(RIGHT)
            else:
                game_over = True
        elif gutter_right:
            score1 += 1
            if score1 < 5:
                spawn_ball(LEFT)
            else:
                game_over = True

        if not game_over:
            # change position to handle ball reflection
            if collision_left or collision_right:
                ball_vel[0] = -(ball_vel[0] + 0.1 * ball_vel[0])
                ball_vel[1] = ball_vel[1] + 0.1 * ball_vel[1]
            elif collision_top or collision_bottom:
                ball_vel[1] = -ball_vel[1]

    # game over
    else:
        if score2 == 5:
            canvas.draw_text("Player 2 wins!", [(WIDTH/2 - 50), HEIGHT/2], 20, "Red")
        elif score1 == 5: 	       
            canvas.draw_text("Player 1 wins!", [(WIDTH/2 - 50), HEIGHT/2], 20, "Red")

    # draw scores
    canvas.draw_text("Player 1: "+str(score1), [(WIDTH/2 - 200), 50], 20, "White")
    canvas.draw_text("Player 2: "+str(score2), [(WIDTH/2 + 100), 50], 20, "White")

def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 4
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel -= acc
    elif key == simplegui.KEY_MAP['down']:     
        paddle1_vel += acc
    elif key == simplegui.KEY_MAP['w']:     
        paddle2_vel -= acc
    elif key == simplegui.KEY_MAP['s']:     
        paddle2_vel += acc
  
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
