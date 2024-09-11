import tkinter as tk
import cv2
import mediapipe as mp
import pyautogui
import time
from PIL import Image, ImageTk

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def count_fingers(lst):
    cnt = 0
    seuil = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

    if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > seuil:
        cnt += 1

    if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > seuil:
        cnt += 1

    if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > seuil:
        cnt += 1

    if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > seuil:
        cnt += 1

    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
        cnt += 1

    return cnt

def start_hand_tracking():
    cap = cv2.VideoCapture(0)
    drawing = mp.solutions.drawing_utils
    hands = mp.solutions.hands
    hand_obj = hands.Hands(max_num_hands=1)
    prev = -1
    curr = -1
    command_start_time = 0
    command_duration = 0.5
    hand_keyPoints = None
    play_pause_flag = False

    def process_frame():
        nonlocal prev, curr, command_start_time, hand_keyPoints, play_pause_flag
        _, frm = cap.read()
        frm = cv2.flip(frm, 1)
        frm_rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
        res = hand_obj.process(frm_rgb)

        if res.multi_hand_landmarks:
            hand_keyPoints = res.multi_hand_landmarks[0]
            curr = count_fingers(hand_keyPoints)

            if curr != prev:
                prev = curr
                command_start_time = time.time()
            elif curr == prev and time.time() - command_start_time >= command_duration:
                if curr == 1:
                    pyautogui.press("right")
                elif curr == 2:
                    pyautogui.press("left")
                elif curr == 3:
                    pyautogui.press("up")
                elif curr == 4:
                    pyautogui.press("down")

            if curr == 5:
                if not play_pause_flag:
                    pyautogui.press("space")
                    play_pause_flag = True
                    command_start_time = time.time()
            else:
                play_pause_flag = False
        # Convert the frame to ImageTk format
        img = Image.fromarray(frm_rgb)
        img_tk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        video_label.configure(image=img_tk)
        video_label.image = img_tk

        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            cap.release()
            root.destroy()
        else:
            root.after(1, process_frame)

    process_frame()
def on_resize(event):
    button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root = tk.Tk()
root.title("Wireless Media Controller")
root.geometry("900x900")

# Load the logo image
logo_image = Image.open("Desktop\logo5.png")
logo_image = logo_image.resize((250, 250))  # Resize the image if needed
logo_photo = ImageTk.PhotoImage(logo_image)

# Create a Label widget to display the logo
logo_label = tk.Label(root, image=logo_photo, border=0)
logo_label.pack(pady=20)

# Styling the GUI
root.configure(bg="#FFFFFF")
root.resizable(True, True)
root.bind("<Configure>", on_resize)

#title_label = tk.Label(root, text="Wireless Media Controller", font=("Arial", 16, "bold"))
#title_label.pack(pady=30)
#title_label.configure(bg=root.cget("bg"))

video_label = tk.Label(root)
video_label.pack(pady=20)

label_text = "© 2023 Labas Oussama. All rights reserved"
label = tk.Label(root, text=label_text, font=("Arial", 10, "bold"))
label.pack(side=tk.BOTTOM, pady=(0, 20))
label.configure(bg=root.cget("bg"))

#version_label = tk.Label(root, text="v1.0", font=("Arial", 10))
#version_label.pack(side=tk.RIGHT, anchor=tk.SE, padx=(0, 20), pady=(0, 20))
#version_label.configure(bg=root.cget("bg"))

button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=(250, 50))
button = tk.Button(button_frame, text="Start", font=("Roboto", 14, "bold"), command=start_hand_tracking, padx=10, pady=10, bg="#F3E5AB", fg="#000000", relief=tk.RAISED)
button.pack(expand=True)

# Center the window on the screen
center_window(root)

root.mainloop()
