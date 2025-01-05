import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Globals
player_x, player_y = 250, 50  # Initial position of the player's car
enemy_cars = []  # List of enemy cars [x, y]
collectibles = []  # List of collectibles [x, y]
score = 0  # Player's score
car_speed = 5  # Speed of enemy cars
speed_increment = 5  # Speed increment per 200 points
paused = False  # Pause state
window_width, window_height = 500, 500
background_color = [0.0, 0.0, 0.0]

# Function to draw a point
def draw_points(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

# Function to draw a filled circle using GL_POINTS
def draw_circle(xc, yc, r):
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x * x + y * y <= r * r:
                draw_points(xc + x, yc + y)

# Draw a car using GL_POINTS and circles
def draw_car(x, y):
    # Car body (a filled rectangle using points)
    for i in range(-15, 16):
        for j in range(-20, 21):
            draw_points(x + j, y + i)

    # Wheels
    draw_circle(x - 15, y - 20, 5)
    draw_circle(x + 15, y - 20, 5)

# Draw a button using circles and filled points
def draw_button(x, y, width, height, label):
    for i in range(width):
        for j in range(height):
            draw_points(x + i, y + j)
    
# Map characters to a simple representation (e.g., rectangles for simplicity)
char_map = {
    'A': [(0, 0), (1, 3), (2, 0)],  # Example representation for 'A'
    'B': [(0, 0), (0, 3), (1, 1.5), (0, 3)],  # Example representation for 'B'
    # Add mappings for other characters
}

def draw_character(char, x, y, size=10):
    """Manually draw a character using rectangles."""
    if char in char_map:
        for (dx, dy) in char_map[char]:
            draw_filled_rectangle(x + dx * size, y + dy * size, size, size)

def draw_text_manual(text, x, y, size=10, spacing=5):
    """
    Manually render text at a given position.

    Parameters:
        text (str): The text to render.
        x (float): X-coordinate.
        y (float): Y-coordinate.
        size (int): Size of each character.
        spacing (int): Spacing between characters.
    """
    for i, char in enumerate(text):
        draw_character(char, x + i * (size + spacing), y, size)


# Draw a pause/play button icon using circles

def draw_pause_play_icon(x, y, paused):
    draw_circle(x, y, 10)  # Outer circle
    if not paused:
        # Draw play symbol (triangle using points)
        for i in range(6):
            for j in range(i + 1):
                draw_points(x + j - 3, y - 3 + i)
    else:
        # Draw pause symbol (two vertical bars using points)
        for i in range(-5, 6):
            for j in range(-2, 1):
                draw_points(x + j, y + i)
            for j in range(2, 5):
                draw_points(x + j, y + i)

# Draw the player's car
def draw_player_car():
    glColor3f(0.0, 1.0, 0.0)  # Green color
    draw_car(player_x, player_y)

# Draw the enemy cars
def draw_enemy_cars():
    glColor3f(1.0, 0.0, 0.0)  # Red color
    for car in enemy_cars:
        draw_car(car[0], car[1])

# Draw the collectibles
def draw_collectibles():
    glColor3f(1.0, 1.0, 0.0)  # Yellow color
    for col in collectibles:
        draw_circle(col[0], col[1], 5)

# Move the enemy cars downward
def move_enemy_cars():
    global score, car_speed
    for car in enemy_cars[:]:
        car[1] -= car_speed
        if car[1] < 0:  # If car moves off-screen
            enemy_cars.remove(car)
            score += 10
            if score % 200 == 0:  # Increase speed every 200 points
                car_speed += speed_increment

# Move the collectibles downward
def move_collectibles():
    for col in collectibles[:]:
        col[1] -= car_speed
        if col[1] < 0:  # Remove if off-screen
            collectibles.remove(col)

# Check for collision with enemy cars
def check_collision():
    global player_x, player_y

    # Player car dimensions
    player_width = 40  # Total width (20 to the left, 20 to the right)
    player_height = 30  # Total height (15 up, 15 down)

    for car in enemy_cars:
        # Enemy car dimensions (assuming similar size)
        enemy_x, enemy_y = car[0], car[1]
        enemy_width = 40  # Width of the enemy car
        enemy_height = 30  # Height of the enemy car

        # Check for overlap between the player's car and the enemy car
        if (player_x - player_width / 2 < enemy_x + enemy_width / 2 and
            player_x + player_width / 2 > enemy_x - enemy_width / 2 and
            player_y - player_height / 2 < enemy_y + enemy_height / 2 and
            player_y + player_height / 2 > enemy_y - enemy_height / 2):
            print("Game Over!")
            print(f"Final Score: {score}")
            glutLeaveMainLoop()


# Check for collision with collectibles
def check_collectibles():
    global score
    for col in collectibles[:]:
        if abs(player_x - col[0]) < 20 and abs(player_y - col[1]) < 20:
            collectibles.remove(col)
            score += 50

# Generate enemy cars at random positions
def generate_enemy_car():
    if random.randint(1, 50) == 1:  # Random chance of generating a car
        enemy_cars.append([random.randint(50, window_width - 50), window_height])

# Generate collectibles at random positions
def generate_collectible():
    if random.randint(1, 100) == 1:  # Random chance of generating a collectible
        collectibles.append([random.randint(50, window_width - 50), window_height])

# Handle mouse clicks
def mouse_click(button, state, x, y):
    global paused, player_x, player_y, score, car_speed, enemy_cars, collectibles
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 10 <= x <= 110 and window_height - 30 <= window_height - y <= window_height:  # Restart button
            player_x, player_y = 250, 50
            enemy_cars.clear()
            collectibles.clear()
            score = 0
            car_speed = 5
            paused = False  # Ensure game is unpaused when restarted
        elif 195 <= x <= 295 and window_height - 30 <= window_height - y <= window_height:  # Pause button
            paused = not paused  # Toggle pause state
            showScreen()  # Force redraw for immediate visual feedback
        elif 390 <= x <= 490 and window_height - 30 <= window_height - y <= window_height:  # Exit button
            glutLeaveMainLoop()

# Keyboard controls for player movement
def keyboard(key, x, y):
    global player_x, player_y
    step = 10  # Step size for movement
    if key == b'w' and player_y + step < window_height:  # Move up
        player_y += step
    elif key == b's' and player_y - step > 0:  # Move down
        player_y -= step
    elif key == b'a' and player_x - step > 0:  # Move left
        player_x -= step
    elif key == b'd' and player_x + step < window_width:  # Move right
        player_x += step


# Special key listener
def specialKeyListener(key, x, y):
    global background_color  # Declare global to modify it
    if key == GLUT_KEY_UP:  # Arrow up key
        background_color = [1.0, 1.0, 1.0]  # Set to white
    elif key == GLUT_KEY_DOWN:  # Arrow down key
        background_color = [0.0, 0.0, 0.0]  # Set to black
    glutPostRedisplay()  # Request a redraw


# Main display function
def showScreen():
    global score, paused, background_color
    glClearColor(*background_color, 1.0)  # Use updated background color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    # Draw buttons
    glColor3f(0.0, 0.0, 1.0)  # Button color
    draw_button(10, window_height - 30, 100, 20, "Restart")
    draw_button(195, window_height - 30, 100, 20, "Pause")
    draw_button(390, window_height - 30, 100, 20, "Exit")
    draw_pause_play_icon(245, window_height - 15, paused)

    if not paused:
        draw_player_car()
        draw_enemy_cars()
        draw_collectibles()
        move_enemy_cars()
        move_collectibles()
        check_collision()
        check_collectibles()
        generate_enemy_car()
        generate_collectible()

    glColor3f(1.0, 1.0, 1.0)
    draw_text(f"Score: {score}", 10, window_height - 50)
    glutSwapBuffers()


def draw_text(text, x, y, font=GLUT_BITMAP_HELVETICA_18, color=(1.0, 1.0, 1.0)):
    """
    Draw text on the screen at specified coordinates.
    
    Parameters:
        text (str): The text to be displayed.
        x (float): X-coordinate for the text position.
        y (float): Y-coordinate for the text position.
        font: GLUT font (default: GLUT_BITMAP_HELVETICA_18).
        color (tuple): RGB color values as floats between 0 and 1 (default: white).
    """
    glColor3f(*color)  # Set the color of the text
    glRasterPos2f(x, y)  # Set the position for the text
    for char in text:
        glutBitmapCharacter(font, ord(char))


# Window setup and main loop
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Car Dose")
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)  # For regular keys
    glutSpecialFunc(specialKeyListener)  # For special keys like arrows
    glutMainLoop()


main()
