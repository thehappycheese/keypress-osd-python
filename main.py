from telnetlib import STATUS
import keyboard  
import threading
import time
import tkinter as tk
from util import Grip, Keyboard_Listener


root = tk.Tk()
root.geometry("400x50")
root.resizable(False, False)
root.overrideredirect(True)
root.attributes("-topmost", True)
root.bind('<Double-Button-1>', lambda event: exit())


stringvar = tk.StringVar()
stringvar.set("...")
text_out  = tk.Label(root, textvariable=stringvar, fg="#EEEEEE", bg="#222222", font=("Arial", 15))
text_out.pack(fill=tk.BOTH, expand=1)


grip = Grip(root)


keyboard_listener = Keyboard_Listener()
    

def thread_output_display(stringvar:tk.StringVar):
    while True:
        time.sleep(0.1)
        keyboard_listener.cleanup_old_resolved_events()
        #resolved   = keyboard_listener.get_resolved_output()
        #unresolved = keyboard_listener.get_unresolved_output()
        # stringvar.set(
            # f"{resolved} {unresolved}"
        # )
        events = [
            *keyboard_listener.unresolved_events.values(),
            *[
                downstroke 
                for downstroke, upstroke
                in keyboard_listener.resolved_events
            ]
        ]
        events.sort(key=lambda item:item.time)
        
        stringvar.set(
            " ".join(item.name for item in events)
        )
        


threading.Thread(
    target=thread_output_display,
    args=(stringvar, ),
    daemon=True
).start()

root.mainloop()