# import time
# import keyboard

# def move_character():
#     keyboard.press('s')
#     keyboard.release('s')
#     time.sleep(1)
#     keyboard.press('w')
#     keyboard.release('w')
#     time.sleep(1)
#     keyboard.press('s')
#     keyboard.release('s')
#     time.sleep(1)
#     keyboard.press('w')
#     keyboard.release('w')
#     time.sleep(1)

# move_character()

import tkinter as tk
import time
import keyboard

def reverse_keys(key_string):
    mapping = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}
    return ''.join(mapping.get(key, key) for key in key_string[::-1])

def create_window2():
    def submit_code():
        code = text_area.get('1.0', 'end-1c')
        exec(code)  # Execute the code entered by the user

    # Create the window
    window = tk.Tk()
    window.title("Code Input")
    window.geometry("500x500")

    # Create the text area for code input
    text_area = tk.Text(window)
    text_area.pack(expand=True, fill="both")

    # Create the button to submit the code
    submit_button = tk.Button(window, text="Submit", command=submit_code)
    submit_button.pack()

    # Run the window
    window.mainloop()

create_window2()