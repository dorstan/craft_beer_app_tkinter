#!/usr/bin/env python3

from datetime import datetime
import os
from os import path
import csv
from sqlite3 import Date
import tkinter as tk
from tkinter import RAISED, ttk
import math as mt
from images import BEER_APP_LOGO

class LabelInput(tk.Frame):
    """This class contains label and input together."""
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
        """Redefines the grid function and automate some processes"""
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        """Redefines the get function and uses try to handle TypeErrors when numeric fields are empty."""
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
        """Redefines the set fuction"""
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

        # Constructing the Frames 
        record = tk.LabelFrame(self, text="Bière - Feuille de Spécifications")
        record.grid(row=0, column=0, sticky=(tk.W + tk.E))

        beer_type = tk.LabelFrame(self, text="Ingrédients - Composition & Répartition")
        beer_type.grid(row=0, column=1, sticky=(tk.W + tk.E))

    
        # Constructing the Widgets 
        # 1. Bière - Feuille de Spécifications
        self.inputs["Essai N°"] = LabelInput(record, "Essai N° d/h", input_var=tk.StringVar())
        self.inputs["Essai N°"].grid(row=0, column=0, sticky = (tk.W + tk.E))

        self.inputs["Rdm Instalation"] = LabelInput(record, "Rendement Instalation (%)", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values":[70, 75, 80, 85, 90, 95, 100]})
        self.inputs["Rdm Instalation"].grid(row=1, column=0, sticky = (tk.W + tk.E))
        
        self.inputs["Base Bière"] = LabelInput(record, "Base Bière", input_class=ttk.Combobox, input_var=tk.StringVar() ,input_args={"values":["Claire 80%", "Amber 78%", "Dark 76%"]})
        self.inputs["Base Bière"].grid(row=2, column=0, sticky = (tk.W + tk.E)) 

        self.inputs["Couleur en EBC"] = LabelInput(record, "Couleur Recherchée (EBC)", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(1, 80))})
        self.inputs["Couleur en EBC"].grid(row=3, column=0, sticky = (tk.W + tk.E))

        self.inputs["Volume Fin Ebullition"] = LabelInput(record, "Qantité Bière (L)", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(10, 51))})
        self.inputs["Volume Fin Ebullition"].grid(row=5, column=0, sticky = (tk.W + tk.E))

        self.inputs["Densite de maiche (°P)"] = LabelInput(record, "Densité de Maiche (°P)", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(0, 16))})
        self.inputs["Densite de maiche (°P)"].grid(row=6, column=0, sticky = (tk.W + tk.E))

        self.inputs["Amertume en IBU"] = LabelInput(record, "Amertume Recherché (IBU)", input_class=ttk.Combobox, input_var=tk.IntVar() ,input_args={"values": list(range(1, 80))})
        self.inputs["Amertume en IBU"].grid(row=7, column=0, sticky = (tk.W + tk.E))

    
        # 2.1 Ingrédients - Composition & Répartition
        self.inputs["Type Grain"] = LabelInput(beer_type, "Choix du Malt\n", input_class= tk.Entry, input_var=tk.StringVar())
        self.inputs["Type Grain"].grid(row=0, column=0, sticky = (tk.W + tk.E))

        self.inputs["Type Grain2"] = LabelInput(beer_type, "", input_class= tk.Entry, input_var=tk.StringVar())
        self.inputs["Type Grain2"].grid(row=1, column=0, sticky = (tk.W + tk.E))

        self.inputs["Type Grain3"] = LabelInput(beer_type, "", input_class= tk.Entry, input_var=tk.StringVar())
        self.inputs["Type Grain3"].grid(row=2, column=0, sticky = (tk.W + tk.E))

        self.inputs["Notes"] = LabelInput(beer_type, "Spécifications\n", input_class=tk.Entry, input_var=tk.StringVar())
        self.inputs["Notes"].grid(row=0, column=1, sticky = (tk.W + tk.E))

        self.inputs["Notes2"] = LabelInput(beer_type, "", input_class=tk.Entry, input_var=tk.StringVar())
        self.inputs["Notes2"].grid(row=1, column=1, sticky = (tk.W + tk.E))

        self.inputs["Notes3"] = LabelInput(beer_type, "", input_class=tk.Entry, input_var=tk.StringVar())
        self.inputs["Notes3"].grid(row=2, column=1, sticky = (tk.W + tk.E))

        self.inputs["EBCgr"] = LabelInput(beer_type, "Couleur (EBC)\n", input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 1, "to": 80, "increment": 1})
        self.inputs["EBCgr"].grid(row=0, column=2, sticky = (tk.W + tk.E))

        self.inputs["EBCgr2"] = LabelInput(beer_type, "", input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 1, "to": 80, "increment": 1})
        self.inputs["EBCgr2"].grid(row=1, column=2, sticky = (tk.W + tk.E))

        self.inputs["EBCgr3"] = LabelInput(beer_type, "", input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 1, "to": 80, "increment": 1})
        self.inputs["EBCgr3"].grid(row=2, column=2, sticky = (tk.W + tk.E))

        self.inputs["Masse grains (Mgrain)"] = LabelInput(beer_type, "Quantité (kg.)\n", input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 1000, "increment": .1})
        self.inputs["Masse grains (Mgrain)"].grid(row=0, column=3, sticky = (tk.W + tk.E))

        self.inputs["Masse grains (Mgrain)2"] = LabelInput(beer_type, "", input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 1000, "increment": .1})
        self.inputs["Masse grains (Mgrain)2"].grid(row=1, column=3, sticky = (tk.W + tk.E))

        self.inputs["Masse grains (Mgrain)3"] = LabelInput(beer_type, "", input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 1000, "increment": .1})
        self.inputs["Masse grains (Mgrain)3"].grid(row=2, column=3, sticky = (tk.W + tk.E))


        # 2.2
        self.inputs["Choix du Houblon"] = LabelInput(beer_type, "Nom Houblon\n(pellet/cône)", input_class= tk.Entry, input_var=tk.StringVar())
        self.inputs["Choix du Houblon"].grid(row=3, column=0, sticky = (tk.W + tk.E))

        self.inputs["Choix du Houblon2"] = LabelInput(beer_type, "", input_class= tk.Entry, input_var=tk.StringVar())
        self.inputs["Choix du Houblon2"].grid(row=4, column=0, sticky = (tk.W + tk.E))

        self.inputs["Choix du Houblon3"] = LabelInput(beer_type, "", input_class= tk.Entry, input_var=tk.StringVar())
        self.inputs["Choix du Houblon3"].grid(row=5, column=0, sticky = (tk.W + tk.E))

        self.inputs["Acides Alpha"] = LabelInput(beer_type, "Acides Alpha (%)\n", input_class=tk.Spinbox, input_var=tk.StringVar() ,input_args={"from_": 1, "to": 100, "increment": .1})
        self.inputs["Acides Alpha"].grid(row=3, column=1, sticky = (tk.W + tk.E))

        self.inputs["Acides Alpha2"] = LabelInput(beer_type, "", input_class=tk.Spinbox, input_var=tk.StringVar() ,input_args={"from_": 1, "to": 100, "increment": .1})
        self.inputs["Acides Alpha2"].grid(row=4, column=1, sticky = (tk.W + tk.E))

        self.inputs["Acides Alpha3"] = LabelInput(beer_type, "", input_class=tk.Spinbox, input_var=tk.StringVar() ,input_args={"from_": 1, "to": 100, "increment": .1})
        self.inputs["Acides Alpha3"].grid(row=5, column=1, sticky = (tk.W + tk.E))

        self.inputs["Quantité utilisée (gr.)"] = LabelInput(beer_type, "Quantité utilisée (gr.)\n",  input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 100, "increment": .1})
        self.inputs["Quantité utilisée (gr.)"].grid(row = 3, column=2, sticky=(tk.W + tk.E))

        self.inputs["Quantité utilisée (gr.)2"] = LabelInput(beer_type, "",  input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 100, "increment": .1})
        self.inputs["Quantité utilisée (gr.)2"].grid(row = 4, column=2, sticky=(tk.W + tk.E))

        self.inputs["Quantité utilisée (gr.)3"] = LabelInput(beer_type, "",  input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 100, "increment": .1})
        self.inputs["Quantité utilisée (gr.)3"].grid(row = 5, column=2, sticky=(tk.W + tk.E))

        self.inputs["Temps Ebullition"] = LabelInput(beer_type, "Temps Ebullition\n/Densité",  input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 0.301, "increment": .001})
        self.inputs["Temps Ebullition"].grid(row = 3, column=3, sticky=(tk.W + tk.E))

        self.inputs["Temps Ebullition2"] = LabelInput(beer_type, "",  input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 0.301, "increment": .001})
        self.inputs["Temps Ebullition2"].grid(row = 4, column=3, sticky=(tk.W + tk.E))

        self.inputs["Temps Ebullition3"] = LabelInput(beer_type, "",  input_class=tk.Spinbox, input_var=tk.StringVar(), input_args={"from_": 0, "to": 0.301, "increment": .001})
        self.inputs["Temps Ebullition3"].grid(row = 5, column=3, sticky=(tk.W + tk.E))
        

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
        self.geometry("1700x1000")
        #self.resizable(width=False, height=False)

      
        # 1 Label containing the logo of the app
        self.logo = tk.PhotoImage(file=BEER_APP_LOGO)
        tk.Label(self, image=self.logo).grid(row=0)
        

        # 2 Frame containing widgets class
        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10)


        # 3 Buttons 
        self.visual_button = ttk.Button(self, text=f"{'':>4}Démarer Recette de Base{'':>4}", command=self.return_recette_base)
        self.visual_button.grid(row=2, sticky = tk.W, padx=10)

        self.balance_button = ttk.Button(self, text="Balancer Recette", command=self.return_recette_balance)
        self.balance_button.grid(sticky=tk.E, row=2, padx=10)

        self.savebutton = ttk.Button(self, text="Sauvegarder", command=self.on_save)
        self.savebutton.grid(sticky=(tk.E+tk.W), row=4, padx=10)


        # 4 Labels
        #self.data_set displays the base recipe
        self.data_set=tk.StringVar()
        self.data_set.set(f"""{'':>59}\n\n\n\n\n\n\n\n""")
        self.visual_data = ttk.Label(self, textvariable=self.data_set)
        self.visual_data.grid(row=3, sticky=(tk.W+tk.N), padx=10)

        #self.balance_set displays the formulas result
        self.balance_set=tk.StringVar()
        self.balance_set.set(f"""{'':>60}\n\n\n\n\n\n\n\n""")
        self.balance_data = ttk.Label(self, textvariable=self.balance_set)
        self.balance_data.grid(sticky=(tk.E+tk.N), row=3, padx=10)

        # self.statusdisplays the number of recipes saved
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=6, padx=10)

        self.records_saved = 0
    
    
    def return_recette_base(self):
        """Function that displays the base recipe command button"""
        self.recette_base = self.return_data()
        self.data_set.set(f"""
{'':>11}RECETTE DE BASE\n
Volume Moût Début Ebullition: {self.recette_base["debut ebullition"]:.1f} l
Quantité Malt:{'': >28}{self.recette_base["quantité malt"]:.1f} kg
Volume Eau Empatage:{'': >13}{self.recette_base["volume empatage"]:.1f} l
Volume Eau Rinçage:{'': >17}{self.recette_base["volume rinçage"]:.1f} l\n
        """)

    def return_data(self):
        """Calculates the formula for grain mass"""
        for x, y in self.recordform.get().items():
            if x == "Densite de maiche (°P)":
                self.maiche = float(y)
            elif x == "Volume Fin Ebullition":
                self.fin_ebullition = float(y)
            elif x == "Rdm Instalation":
                self.instalation = float(y)
            elif x == "Base Bière":
                if y == "Claire 80%":
                    self.base_bière = 80
                elif y == "Amber 78%":
                    self.base_bière = 78
                else:
                    self.base_bière = 76
        self.result = (self.maiche*100*self.fin_ebullition)/(self.instalation*self.base_bière)
        self.start_volume = self.fin_ebullition * 1.085
        self.water_volume = self.result * 3
        self.washing_volume = (self.start_volume-self.water_volume+self.result)*1.2

        self.result_formula = {"quantité malt": self.result, "debut ebullition": self.start_volume, "volume empatage": self.water_volume, "volume rinçage": self.washing_volume}
        return self.result_formula


    def return_recette_balance(self):
        """Function that displays the balanced recipe command button"""
        self.ebc_result = self.ebc_color()
        self.ibu_result = self.ibu_amertume()
        self.valeur_base = self.recordform.get()
        # save data in a list
        self.save_data_list = []
        self.save_data_list.append(float(self.valeur_base["Couleur en EBC"]) - self.ebc_result)
        self.save_data_list.append(float(self.valeur_base["Amertume en IBU"]) - self.ibu_result)
        for number in self.save_data_list:
            if number > 0.2:
                self.balance_set.set(f"""
{'':>8}ÉQUILIBREZ LA RECETTE\n
Couleur Recherchée{'': >11}EBC: {self.valeur_base["Couleur en EBC"]}
Couleur Actuelle{'': >17}EBC: {self.ebc_result:.1f}\n
Amertume Recherchée{'': >7}IBU: {self.valeur_base["Amertume en IBU"]}
Amertume Actuelle{'': >13}IBU: {self.ibu_result:.1f}
""")
            elif number < -0.2:
                self.balance_set.set(f"""
{'':>8}ÉQUILIBREZ LA RECETTE\n
Couleur Recherchée{'': >11}EBC: {self.valeur_base["Couleur en EBC"]}
Couleur Actuelle{'': >17}EBC: {self.ebc_result:.1f}\n
Amertume Recherchée{'': >7}IBU: {self.valeur_base["Amertume en IBU"]}
Amertume Actuelle{'': >13}IBU: {self.ibu_result:.1f}
""")
            else:
                self.balance_set.set(f"""
{'':>11}BIÈRE ÉQUILIBRÉE\n
Couleur Recherchée{'': >11}EBC: {self.valeur_base["Couleur en EBC"]}
Couleur Actuelle{'': >17}EBC: {self.ebc_result:.1f}\n
Amertume Recherchée{'': >7}IBU: {self.valeur_base["Amertume en IBU"]}
Amertume Actuelle{'': >13}IBU: {self.ibu_result:.1f}
""")


    def ebc_color(self):
        """Calculates the Colour of the beer in EBC"""
        self.sum_ebc = []
        self.grain_mass_items = {}

        for x, y in self.recordform.get().items():
            self.grain_mass_items[x] = y
            if x == "Volume Fin Ebullition":
                self.fin_ebullition = float(y)

        self.grain_mass_list = ["Masse grains (Mgrain)", "Masse grains (Mgrain)2", "Masse grains (Mgrain)3"]
        self.ebc_list = ["EBCgr", "EBCgr2", "EBCgr3"]
        
        self.result_grain = []
        for gr_mass in self.grain_mass_list:
            if self.grain_mass_items[gr_mass]:
                self.result_grain.append(self.grain_mass_items[gr_mass])

        self.result_ebc = []
        for ebc_mass in self.ebc_list:
            if self.grain_mass_items[ebc_mass]:
                self.result_ebc.append(self.grain_mass_items[ebc_mass])

        for item1, item2 in zip(self.result_grain, self.result_ebc):
            self.sum_item = float(item1)*float(item2)
            self.sum_ebc.append(self.sum_item)
        self.formula_total = mt.fsum(self.sum_ebc)
        self.multiplicator = 7.5
        self.formula_total = self.formula_total * self.multiplicator/self.fin_ebullition

        return self.formula_total

    def ibu_amertume(self):
        """Calculates the bitterness of the beer in IBU"""
        self.list_formula_ibu_quantity = []
        self.dict_data_ibu = {}
        
        for dict_key, dict_value in self.recordform.get().items():
            self.dict_data_ibu[dict_key] = dict_value
            if dict_key == "Volume Fin Ebullition":
                self.volume_beer = float(dict_value)

        self.list_ibu_amertume = ["Acides Alpha", "Acides Alpha2", "Acides Alpha3"]
        self.list_ibu_amertume2 = ["Quantité utilisée (gr.)", "Quantité utilisée (gr.)2", "Quantité utilisée (gr.)3"]
        self.list_ibu_amertume3 = ["Temps Ebullition", "Temps Ebullition2", "Temps Ebullition3"]

        for r1, r2, r3 in zip(self.list_ibu_amertume, self.list_ibu_amertume2, self.list_ibu_amertume3):
            if self.dict_data_ibu[r1] != "":
                if self.dict_data_ibu[r2] != "":
                    if self.dict_data_ibu[r3] != "":
                        self.result_ibu_amertume = float(self.dict_data_ibu[r1]) * float(self.dict_data_ibu[r2]) * float(self.dict_data_ibu[r3])
                        self.list_formula_ibu_quantity.append(self.result_ibu_amertume * 10 / self.volume_beer)
            else: pass
                
        self.aau_formula = mt.fsum(self.list_formula_ibu_quantity)
        return self.aau_formula
    
    def on_save(self):
        """Handles save button clicks"""
        #datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "./beer_log.csv"
        newfile = not os.path.exists(filename)

        data = self.recordform.get()

        with open(filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

        self.status.set(
            "La recette a été sauveguardée")
        self.recordform.reset()
        self.data_set.set(f"""{'':>60}\n\n\n\n\n\n\n\n""")
        self.balance_set.set(f"""{'':>60}\n\n\n\n\n\n\n\n""")

if __name__ == "__main__":
    app = Application()
    app.mainloop()