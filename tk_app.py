#!/usr/bin/env python3

from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk

class LabelInput(tk.Frame):
    """A widget containing a label and input together."""
    def __init__(self, parent, label='', input_class=ttk.Entry,
                input_var=None, input_args=None, label_args=None,
                **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var
        
        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
              # happens when numeric fields are empty.
              return ''

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
                self.variable.set(bool(value))
        elif self.variable:
                self.variable.set(value, *args, **kwargs)
        elif type(self.input).__name__.endswith('button'):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)

class DataRecordForm(tk.Frame):
    """This class contains the form for our widget"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # A dict to keep track of input widgets
        self.inputs = {}

        # Constructing the Widgets 
        # ---------------------------------------------------------

        record = tk.LabelFrame(self, text="Fiche d'information")
        record.grid(row=0, column=0, sticky=(tk.W + tk.E))

        beer_type = tk.LabelFrame(self, text="Style de Biere")
        beer_type.grid(row=1, column=0, sticky=(tk.W + tk.E))

        malt_type = tk.LabelFrame(self, text="Variété de Malt")
        malt_type.grid(row=2, column=0, sticky=(tk.W + tk.E))

        hops_type = tk.LabelFrame(self, text="Houblon")
        hops_type.grid(row=3, column=0, sticky=(tk.W + tk.E))

    
        # Constructing the Widgets 
        # --------------------------------------------------------------

        self.inputs["Date"] = LabelInput(record, "Date", input_var=tk.StringVar())
        self.inputs["Date"].grid(row=0, column=0)
        
        self.inputs["Base Bière"] = LabelInput(record, "Base Bière", input_class=ttk.Combobox, input_var=tk.StringVar() ,input_args={"values":["Claire 80%", "Amber 78%", "Dark 76%"]})
        self.inputs["Base Bière"].grid(row=0, column=1) 

        self.inputs["Essai d/h"] = LabelInput(record, "Essai d/h", input_var=tk.StringVar())
        self.inputs["Essai d/h"].grid(row=0, column=2)

        self.inputs["Rdm Instalation"] = LabelInput(record, "Rdm Instalation", input_var=tk.IntVar())
        self.inputs["Rdm Instalation"].grid(row=0, column=3)

        self.inputs["Volume Fin Ebullition"] = LabelInput(record, "Volume Fin Ebullition", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(10, 51))})
        self.inputs["Volume Fin Ebullition"].grid(row=1, column=0)

        self.inputs["Densite de maiche (°P)"] = LabelInput(record, "Densite de maiche (°P)", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(0, 16))})
        self.inputs["Densite de maiche (°P)"].grid(row=1, column=1)

        self.inputs["Couleur en EBC"] = LabelInput(record, "Couleur en EBC", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(1, 80))})
        self.inputs["Couleur en EBC"].grid(row=1, column=2)

        self.inputs["Amertume en IBU"] = LabelInput(record, "Amertume en IBU", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(1, 80))})
        self.inputs["Amertume en IBU"].grid(row=1, column=3)

        # Second Frame
        self.inputs["Type Grain"] = LabelInput(beer_type, "Type Grain", input_var=tk.StringVar())
        self.inputs["Type Grain"].grid(row=0, column=0)

        self.inputs["Type Grain2"] = LabelInput(beer_type, "", input_var=tk.StringVar())
        self.inputs["Type Grain2"].grid(row=1, column=0)

        self.inputs["Type Grain3"] = LabelInput(beer_type, "", input_var=tk.StringVar())
        self.inputs["Type Grain3"].grid(row=2, column=0)

        self.inputs["Masse grains (Mgrain)"] = LabelInput(beer_type, "Masse grains (Mgrain)", input_var=tk.StringVar())
        self.inputs["Masse grains (Mgrain)"].grid(row=0, column=1)

        self.inputs["Masse grains (Mgrain)2"] = LabelInput(beer_type, "", input_var=tk.StringVar())
        self.inputs["Masse grains (Mgrain)2"].grid(row=1, column=1)

        self.inputs["Masse grains (Mgrain)3"] = LabelInput(beer_type, "", input_var=tk.StringVar())
        self.inputs["Masse grains (Mgrain)3"].grid(row=2, column=1)

        self.inputs["EBCgr"] = LabelInput(beer_type, "EBCgr", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(1, 80))})
        self.inputs["EBCgr"].grid(row=0, column=2)

        self.inputs["EBCgr2"] = LabelInput(beer_type, "", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(1, 80))})
        self.inputs["EBCgr2"].grid(row=1, column=2)

        self.inputs["EBCgr3"] = LabelInput(beer_type, "", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(1, 80))})
        self.inputs["EBCgr3"].grid(row=2, column=2)

        self.inputs["Notes"] = LabelInput(beer_type, "Notes", input_class=tk.Entry, input_var=tk.StringVar())
        self.inputs["Notes"].grid(row=0, column=3)

        self.inputs["Notes"] = LabelInput(beer_type, "", input_class=tk.Entry, input_var=tk.StringVar())
        self.inputs["Notes"].grid(row=1, column=3)

        self.inputs["Notes"] = LabelInput(beer_type, "", input_class=tk.Entry, input_var=tk.StringVar())
        self.inputs["Notes"].grid(row=2, column=3, sticky = (tk.W + tk.E))

        #default the form
        self.reset()

    def get(self):
        """Retrieve data from form as a dict"""
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        """Resets the form entries"""
        for widget in self.inputs.values():
            widget.set('')    





    


class Application(tk.Tk):
    """Application root window"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Bière Artisanale")
        self.geometry("850x1000+800+950")
        self.resizable(width=False, height=False)
      
        ttk.Label(
            self,
            text="Bière Artisanale",
            font=("TkDefaultFont", 16)).grid(row=0)

        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10)

        self.savebutton = ttk.Button(self, text="Save", command=self.on_save)
        self.savebutton.grid(sticky=tk.E, row=2, padx=10)

        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

        self.records_saved = 0

    def on_save(self):
        """Handles save button clicks"""

        # For now, we save to a hardcoded filename with a datestring.
        # If it doesnt' exist, create it,
        # otherwise just append to the existing file
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "/Users/dorinstanchescu/Kode/craft_beer_app_tkinter/beer_log{}.csv".format(datestring)
        newfile = not os.path.exists(filename)

        data = self.recordform.get()

        with open(filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

        self.records_saved += 1
        self.status.set(
            "{} records saved this session".format(self.records_saved))
        self.recordform.reset()

if __name__ == "__main__":
    app = Application()
    app.mainloop()