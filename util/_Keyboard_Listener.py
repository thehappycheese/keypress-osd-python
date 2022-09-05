


import keyboard
from keyboard import KeyboardEvent
from threading import Thread
from time import time as now

class Keyboard_Listener:
    """Starts a thread that listens to the keyboard and provides analysis"""
    unresolved_events : dict[int, KeyboardEvent]
    resolved_events   : list[tuple[KeyboardEvent, KeyboardEvent]]
    thread            : Thread

    def __init__(self):
        self.unresolved_events = {}
        self.resolved_events   = []
        self.thread = Thread(
            target=self.keyboard_listener_thread,
            daemon=True
        )
        self.thread.start()

    def keyboard_listener_thread(self):
        while True: 
            self.process_event(
                keyboard.read_event()
            )

    def process_event(self, new_event:KeyboardEvent):
        #print(new_event.name, new_event.scan_code)
        # on up-stroke try find a corresponding down-stroke
        if new_event.event_type == "up":
            if new_event.scan_code in self.unresolved_events:
                resolved_event = (
                    self.unresolved_events[new_event.scan_code],
                    new_event,
                )
                self.resolved_events.append(resolved_event)
                self.resolved_events.sort(key=lambda item:item[0].time)
                del self.unresolved_events[new_event.scan_code]
            # otherwise, discard this event
        elif new_event.event_type == "down":
            if new_event.scan_code not in self.unresolved_events:
                self.unresolved_events[new_event.scan_code] = new_event
        else:
            # ??
            pass
    
    def get_unresolved_output(self)->str:
        return "+".join(item.name for item in self.unresolved_events.values())
    
    def get_resolved_output(self)->str:
        return " ".join(down.name for (down, up) in self.resolved_events)

    def cleanup_old_resolved_events(self):
        self.resolved_events = [
            (downstroke, upstroke)
            for downstroke, upstroke 
            in self.resolved_events
            if now()-upstroke.time<1.0
        ]
# keyboard