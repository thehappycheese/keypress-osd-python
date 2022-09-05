import tkinter as tk
from keyboard import KeyboardEvent
import threading
import time
from util import Grip, Keyboard_Listener



root = tk.Tk()
root.geometry("400x46")
root.resizable(False, False)
root.overrideredirect(True)
root.attributes("-topmost", True)
root.bind('<Double-Button-1>', lambda event: exit())

text_out  = tk.Text(
    root,
    fg="#EEEEEE",
    bg="#222222",
    font=("Arial", 20),
    relief="flat",
    padx=5,
    pady=5,
    cursor="arrow",
    state=tk.DISABLED
)

text_out.pack(fill=tk.BOTH, expand=1)
text_out.tag_configure("inactive", foreground="#EEEEEE", justify=tk.CENTER)
text_out.tag_configure("active", foreground="red", justify=tk.CENTER)


grip = Grip(root)

keyboard_listener = Keyboard_Listener()    

def thread_output_display():
    while True:
        time.sleep(0.1)
        keyboard_listener.cleanup_old_resolved_events()
        
        events:list[tuple[str, KeyboardEvent]] = [
            *[
                ("unresolved", item)
                for item
                in keyboard_listener.unresolved_events.values()
            ],
            *[
                ("resolved", downstroke)
                for downstroke, upstroke
                in keyboard_listener.resolved_events
            ]
        ]
        events.sort(key=lambda item:item[1].time)
        text_out.config(state=tk.NORMAL)
        text_out.delete(0.0,"end")
        if len(events)==0:
            #text_out.insert("end","...")
            pass
        else:
            for (item_type, item) in events:
                if item_type == "unresolved":
                    text_out.insert("end", " " + item.name, ("active",))
                else:
                    text_out.insert("end", " " + item.name, ("inactive",))
        text_out.config(state=tk.DISABLED)

threading.Thread(
    target=thread_output_display,
    daemon=True
).start()


root.mainloop()