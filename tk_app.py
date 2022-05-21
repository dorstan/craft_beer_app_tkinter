#!/usr/bin/env python3

from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    """Application root window"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Bière Artisanale")
        self.geometry("850x1000+800+950")
        self.resizable(width=False, height=False)
      
        ttk.Label(
            self,
            text="Craft Beer App",
            font=("TkDefaultFont", 16)        
            ).grid(row=0)
      


if __name__ == "__main__":
    app = Application()
    app.mainloop()