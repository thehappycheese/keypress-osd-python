import tkinter as tk
from typing import Union

class Grip:
    """Makes a window draggable by the provided widget argument."""

    widget:Union[tk.Widget, tk.Tk]
    root:Union[tk.Tk, tk.Toplevel]
    
    def __init__ (self, widget:Union[tk.Widget, tk.Tk]):
        self.widget = widget
        self.root = widget.winfo_toplevel()

        self.widget.bind('<Button-1>', self.relative_position)
        self.widget.bind('<ButtonRelease-1>', self.drag_unbind)

    def relative_position (self, event):
        cx, cy = self.widget.winfo_pointerxy()
        geo = self.root.geometry().split("+")
        self.oriX, self.oriY = int(geo[1]), int(geo[2])
        self.relX = cx - self.oriX
        self.relY = cy - self.oriY

        self.widget.bind('<Motion>', self.drag_wid)

    def drag_wid (self, event):
        cx, cy = self.widget.winfo_pointerxy()
        x = cx - self.relX
        y = cy - self.relY
        self.root.geometry(f'+{x:.0f}+{y:.0f}')

    def drag_unbind (self, event):
        self.widget.unbind('<Motion>')