import queue
import keyboard  
import threading
import time
import tkinter as tk
from util import Grip


modifier_order = [
    "ctrl",
    "alt",
    "shift",
]

def get_index_of_item(item:str):
    try:
        return modifier_order.index(item)
    except ValueError:
        return len(modifier_order)+1


root = tk.Tk()
root.geometry("500x50")
root.resizable(False, False)
root.overrideredirect(True)
root.attributes("-topmost", True)
root.bind('<Double-Button-1>', lambda event: exit())

stringvar = tk.StringVar()
stringvar.set("...")
text_out = tk.Label(root, textvariable=stringvar, fg="#EEEEEE", bg="#222222", font=("Arial", 40))
text_out.pack(fill=tk.BOTH, expand=1)

grip = Grip(root)

def keyboard_listener_thread(stringvar:tk.StringVar):
    keysdown = set()
    def delayline(name:str):
        nonlocal keysdown
        if name in keysdown:
            time.sleep(0.5)
            keysdown.remove(name)
            stringvar.set("+".join(sorted(keysdown, key=get_index_of_item)))
    while True:
        result:keyboard.KeyboardEvent = keyboard.read_event()
        if result.modifiers is not None:
            print(result.modifiers)
        if result.event_type == "down":
            keysdown.add(result.name)
        else:
            threading.Thread(target = delayline, args=(result.name,), daemon=True).start()
        stringvar.set("+".join(sorted(keysdown, key=get_index_of_item)))

main_loop_thread = threading.Thread(target=keyboard_listener_thread, args=(stringvar, ), daemon=True)
#main_loop_thread.daemon = True 
main_loop_thread.start()

root.mainloop()