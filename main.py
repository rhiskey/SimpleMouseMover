import random
import threading

import pyautogui
import sys
import keyboard
import time
import tkinter as tk
from tkinter import ttk
import os
from dotenv import load_dotenv

load_dotenv()
print('Press Ctrl-C/q to quit.')
width, height = pyautogui.size()
pyautogui.FAILSAFE = False
is_running = True


def run_move():
    try:
        if not is_running:
            return

        while is_running:
            # x, y = pyautogui.position()
            # position_str = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)

            rand_x = random.randint(0, width)
            rand_y = random.randint(0, height)

            pyautogui.moveTo(rand_x, rand_y, 0.5, pyautogui.easeInOutQuad)  # moves mouse to X of 100, Y of 200.
            # start and end fast, slow in middle

            delay_cfg = int(os.getenv('DELAY'))
            time.sleep(delay_cfg)

            click_cfg = bool(os.getenv('IS_AUTOCKICK_ENABLED'))

            if click_cfg:
                pyautogui.click()

        return

    except KeyboardInterrupt:
        print('\n')
        sys.exit()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.stop = tk.Button(self, text="Stop", command=self.stop_moving)
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.start = tk.Button(self)
        self.label_delay = tk.Label(self,
                                    text="Delay")
        self.entry_delay = tk.Entry(self)

        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start["text"] = "Start\n(Stop)"
        self.start["command"] = self.start_move_mouse
        self.start.grid(row=0, column=0, sticky=tk.W, pady=4)
        self.stop.grid(row=0, column=1, sticky=tk.W, pady=4)
        self.label_delay.grid(row=1, column=0)
        self.entry_delay.grid(row=1, column=1)
        delay_cfg = int(os.getenv('DELAY'))
        self.entry_delay.insert(0, delay_cfg)
        self.quit.grid(row=2, column=0, sticky=tk.W, pady=4)

    def start_move_mouse(self):
        self.start_moving()
        self.start.config(state=tk.DISABLED)
        thread = threading.Thread(target=run_move)
        thread.daemon = True
        print(threading.main_thread().name)
        print(thread.name)
        thread.start()
        self.check_thread(thread)

    def check_thread(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.check_thread(thread))
        else:
            self.start.config(state=tk.NORMAL)

    def start_moving(self):
        delay = self.entry_delay.get()
        os.environ['DELAY'] = delay

        global is_running
        is_running = True

    def stop_moving(self):
        delay = self.entry_delay.get()
        os.environ['DELAY'] = delay

        global is_running
        is_running = False


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    # start()
