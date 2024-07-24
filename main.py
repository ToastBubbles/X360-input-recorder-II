import pygame
import time

# Initialize Pygame
pygame.init()

# Initialize the joystick module
pygame.joystick.init()

# Check if there are any joysticks connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    pygame.quit()
    exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick Name: {joystick.get_name()}")
print(f"Number of Axes: {joystick.get_numaxes()}")
print(f"Number of Buttons: {joystick.get_numbuttons()}")
print(f"Number of Hats: {joystick.get_numhats()}")

buttons = {
    'A': 0,
    'B': 1,
    'X': 2,
    'Y': 3,
    'LB': 4,
    'RB': 5,
    'back': 6, 
    'start': 7,
    'LS': 8,
    'RS': 9,
    'up': (0, 1), 
    'down': (0, -1), 
    'left': (-1, 0), 
    'right': (1, 0) 
}

# Deadzone threshold
DEADZONE_THRESHOLD = 0.1

# Reverse mapping for button names
button_names = {v: k for k, v in buttons.items()}

# Define axis and hat mappings (adjust according to your needs)
axes = {
    0: 'LS X',
    1: 'LS Y',
    2: 'RS X',
    3: 'RS Y',
    4: 'LT',
    5: 'RT'
}

hats = {
    0: 'D-pad'
}

# Reverse mapping for axis and hat names
axis_names = {v: k for k, v in axes.items()}
hat_names = {v: k for k, v in hats.items()}

# Convert axis values to percentages with deadzone
def convert_to_percentage(value):
    if abs(value) < DEADZONE_THRESHOLD:
        return 0
    return round(value * 100)

# Logging function
def log_input(input_type, identifier, value):
    with open('controller_log.txt', 'a') as f:
        if input_type == 'axis':
            name = axis_names.get(identifier, f"Axis {identifier}")
            f.write(f"Axis ({name}): {value}\n")
        elif input_type == 'button':
            f.write(f"Button {button_names.get(identifier, identifier)} {'pressed' if value else 'released'}\n")
        elif input_type == 'hat':
            name = hat_names.get(identifier, f"Hat {identifier}")
            f.write(f"Hat ({name}): {value}\n")

# Main loop
try:
    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = event.value
                value = convert_to_percentage(value)
                if value != 0:
                    log_input('axis', axis, value)
                    print(f"{axes.get(axis, axis)}: {value}")
            elif event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                log_input('button', button, True)
                print(f"Button {button_names.get(button, button)} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                button = event.button
                log_input('button', button, False)
                print(f"Button {button_names.get(button, button)} released")
            elif event.type == pygame.JOYHATMOTION:
                hat = event.hat
                value = event.value
                direction = "Center"
                if value[0] == 0 and value[1] == 1:
                    direction = "Up"
                elif value[0] == 0 and value[1] == -1:
                    direction = "Down"
                elif value[0] == -1 and value[1] == 0:
                    direction = "Left"
                elif value[0] == 1 and value[1] == 0:
                    direction = "Right"
                log_input('hat', hat, direction)
                print(f"{hat_names.get(hat, hat)}: {direction}")

        time.sleep(0.1)


except KeyboardInterrupt:
    print("Exiting...")
    pygame.quit()