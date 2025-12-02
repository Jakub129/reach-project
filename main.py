# ________________ TODOs ________________
"""
- Import data to the plot --> DONE
--> Read data correctly and interpret into a suitable plot
- Save/download the plot --> DONE
- Change the plot scales: linear/log -> DONE
- improve the UI and visuals: MENUS (settings?)
- Desmos features: zoom in/out, move around the plot, etc... --> DONE
- Line/marker properties: colour, width/size, etc... --> WORKING ON IT
- Error bars: use AI confidence score?
- plot types - bar, radar etc?
- plot a theoretical equation?
- "Live" time animtation of the data 
"""


#  ________________ LIBRARIES ________________
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import colorchooser
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.pyplot as plt
from matplotlib import rcParams

from sympy import Symbol, lambdify, N
from sympy.parsing.latex import parse_latex 

import numpy as np
import pandas as pd


# ________________ MAIN PROGRAM _______________
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graphical Preview")
        self.geometry("1366x768")
        self.setup_widgets()


    def setup_widgets(self):
        ROWSPAN = 9
        COLUMNSPAN = 3

        for column in range(COLUMNSPAN):
            self.grid_columnconfigure(column, weight=1)

        for row in range(ROWSPAN):
            self.grid_rowconfigure(row, weight=1)
  

        self.fig, self.ax  = plt.subplots()
        self.xdata, self.ydata = [x for x in range(-10, 10)], [x**2 for x in range(-10,10)]   
        self.line, = self.ax.plot(self.xdata, self.ydata)

        # Some default plot
        self.ax.set(title="Enter a title...", xlabel="x", ylabel="y")

        self.matplot_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.matplot_canvas.draw()
        self.matplot_canvas.get_tk_widget().grid(row=0, column=0, rowspan=(ROWSPAN-1), padx=5, pady=5, sticky="nsew")


        self.title_entry = EntryPlaceholder(self, placeholder="Plot Title: ")
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.title_button = ttk.Button(self, 
                                text="Apply", 
                                cursor="hand2",
                                command=self.change_title).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.xaxis_entry = EntryPlaceholder(self, placeholder="Label the x-axis: ")
        self.xaxis_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.xaxis_button = ttk.Button(self, 
                                text="Apply", 
                                cursor="hand2",
                                command=self.change_xaxis).grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        
        self.yaxis_entry = EntryPlaceholder(self, placeholder="Label the y-axis: ")
        self.yaxis_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.yaxis_button = ttk.Button(self, 
                                text="Apply", 
                                cursor="hand2",
                                command=lambda: self.change_yaxis()).grid(row=2, column=2, padx=10, pady=10, sticky="ew")
        
        var_yaxis = tk.IntVar()
        var_xaxis = tk.IntVar()
        self.rbutton_xlin = ttk.Radiobutton(self, text="x-axis linear", variable=var_xaxis, value=1, command=self.select_xlinear).grid(
            row=3, column=1, padx=10, pady=10, sticky="ew"
        )
        self.rbutton_ylin = ttk.Radiobutton(self, text="y-axis linear", variable=var_yaxis, value=2, command=self.select_ylinear).grid(
            row=4, column=1, padx=10, pady=10, sticky="ew"
        )
        self.rbutton_xlog = ttk.Radiobutton(self, text="x-axis log", variable=var_xaxis, value=3, command=self.select_xlog).grid(
            row=3, column=2, padx=10, pady=10, sticky="ew"
        )
        self.rbutton_ylog = ttk.Radiobutton(self, text="y-axis log", variable=var_yaxis, value=4, command=self.select_ylog).grid(
            row=4, column=2, padx=10, pady=10, sticky="ew"
        )

        self.var_grid = tk.IntVar()
        self.show_grid_tbox = ttk.Checkbutton(self, text="Show plot grid", variable=self.var_grid, onvalue=1, offvalue=0, command=self.show_grid).grid(
            row=5, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        self.var_points = tk.IntVar()
        self.show_plot_points = ttk.Checkbutton(self, text="Show plot points", variable=self.var_points, onvalue=1, offvalue=0, command=self.show_points).grid(
            row=5, column=1, padx=10, pady=10, sticky="ew"
        )

        self.colour_code = "FFFFFF"
        self.colour_button = ttk.Button(self, 
                                text="Change points colour", 
                                cursor="hand2",
                                command=self.change_colour).grid(
            row=5, column=2, padx=10, pady=10, sticky="ew"
        )

        self.filename = ""
        self.file_button = ttk.Button(self, 
                                text="Import a file", 
                                cursor="hand2",
                                command=self.select_file).grid(
            row=6, column=1, padx=10, pady=10, sticky="ew"
        )

        self.scale_var = tk.DoubleVar()
        self.line_width_bar = ttk.Scale(self, from_= 0, to=10, variable=self.scale_var, cursor="hand2").grid(
            row=7, column=2, padx=10, pady=10, sticky="ew"
        )

        self.scale_button = ttk.Button(self, 
                                text="Change line width", 
                                cursor="hand2",
                                command= self.change_line_width).grid(
            row=6, column=2, padx=10, pady=10, sticky="ew"
        )

        self.line_width_options = [0, 1, 2, 3, 4, 5]
        self.option = tk.StringVar(value=0)
        self.option_menu = ttk.OptionMenu(self, self.option, *self.line_width_options).grid(
            row=7, column=1, padx=10, pady=10, sticky="ew"
        )


        self.toolbar = tkagg.NavigationToolbar2Tk(self.matplot_canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=8, column=0)    


    def change_title(self):
        if self.title_entry.get() == self.title_entry.placeholder:
            self.ax.set_title("")
        else:
            self.fig_title = self.title_entry.get()
            self.ax.set_title(self.fig_title)
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, self.title_entry.placeholder)
        self.title_entry["fg"] = self.title_entry.placeholder_colour
        self.matplot_canvas.draw()

    def change_xaxis(self):
        if self.xaxis_entry.get() == self.xaxis_entry.placeholder:
            self.ax.set_xlabel("")
        else:
            self.ax.set_xlabel(self.xaxis_entry.get())
        self.xaxis_entry.delete(0, tk.END)
        self.xaxis_entry.insert(0, self.xaxis_entry.placeholder)
        self.xaxis_entry["fg"] = self.xaxis_entry.placeholder_colour
        self.matplot_canvas.draw()

    def change_yaxis(self):
        if self.yaxis_entry.get() == self.yaxis_entry.placeholder:
            self.ax.set_ylabel("")
        else:
            self.ax.set_ylabel(self.yaxis_entry.get())
        self.yaxis_entry.delete(0, tk.END)
        self.yaxis_entry.insert(0, self.yaxis_entry.placeholder)
        self.yaxis_entry["fg"] = self.yaxis_entry.placeholder_colour
        self.matplot_canvas.draw()


    def select_xlinear(self):
        self.ax.set_xscale("linear")
        self.matplot_canvas.draw()

    def select_ylinear(self):
        self.ax.set_yscale("linear")
        self.matplot_canvas.draw()

    def select_xlog(self):
        self.ax.set_xscale("log")
        self.matplot_canvas.draw()

    def select_ylog(self):
        self.ax.set_yscale("log")
        self.matplot_canvas.draw()

    def show_grid(self):
        if self.var_grid.get() == 1:
            self.ax.grid()
            self.matplot_canvas.draw()
        elif self.var_grid.get() == 0:
            self.ax.grid(visible=None)
            self.matplot_canvas.draw()

    def show_points(self):
        if self.var_points.get() == 1:
            self.line.set_marker("o")
            self.matplot_canvas.draw()
        elif self.var_points.get() == 0:
            self.line.set_marker("")
            self.matplot_canvas.draw()

    def change_colour(self):
        self.colour_code = colorchooser.askcolor(title="Choose colour")
        self.line.set_color(self.colour_code[1])
        self.matplot_canvas.draw()


    def select_file(self):
        filetypes = (
            ('All files', '*.*'),
            ('text files', '*.txt')
        )
        #self.fig.clear()
        self.ax.cla()

        self.filename = fd.askopenfilename(
            title='Open a file',
            initialdir='%USERPROFILE%\\source\\repos',
            filetypes=filetypes)
        
        df = pd.read_csv(self.filename, header=10)
        date = df["Date"]
        time = df["Time"]
        etime = df["Elapsed Time (secs)"]
        value = df.iloc[:,-1:]
        self.xdata = etime.tolist()
        

        if value.columns[0] == "Results Text":
            self.ax.set_ylabel("Text Frequency")
            text_count = df["Results Text"].value_counts()
            text_count = text_count[text_count > 1]
            text_count.plot(kind="bar")


        if value.columns[0] == "test-AverageRGB":
            self.ax.set_ylabel("RGB values")

            red = df['test-AverageRGB'].apply(lambda x: int(x.split(',')[0])).tolist()
            green = df['test-AverageRGB'].apply(lambda x: int(x.split(',')[1])).tolist()
            blue = df['test-AverageRGB'].apply(lambda x: int(x.split(',')[2])).tolist()

            self.line = self.ax.plot(self.xdata, red, label="Red", color="red")
            self.ax.plot(self.xdata, green, label="Green", color="green")
            self.ax.plot(self.xdata, blue, label="Blue", color="blue")
            self.ax.set_xlabel("Elapsed Time (secs)")
            self.change_xaxis

        if value.columns[0] == "colour change alert-AverageRGB":
            self.ax.set_ylabel("RGB values")

            red = df['colour change alert-AverageRGB'].apply(lambda x: int(x.split(',')[0])).tolist()
            green = df['colour change alert-AverageRGB'].apply(lambda x: int(x.split(',')[1])).tolist()
            blue = df['colour change alert-AverageRGB'].apply(lambda x: int(x.split(',')[2])).tolist()
    
            #self.line = self.ax.plot(self.xdata, red, label="Red", color="red")
            self.ax.plot(self.xdata, red, label="red", color="red")
            self.ax.plot(self.xdata, green, label="Green", color="green")
            self.ax.plot(self.xdata, blue, label="Blue", color="blue")
            self.ax.set_xlabel("Elapsed Time (secs)")
            
        self.matplot_canvas.draw()
        

    def change_line_width(self):
        self.line.set_linewidth(f"{self.scale_var.get()}")
        self.matplot_canvas.draw()


    def save_plot(self):
        self.fig.savefig(self.save_entry.get())
        self.save_entry.delete(0, "end")

    def on_close(self):
        self.quit()
        self.destroy()


class EntryPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="default", colour="grey"):
        tk.Entry.__init__(self, master)

        self.placeholder = placeholder
        self.placeholder_colour = colour
        self.text_colour = self["fg"]
        
        self.insert(0, self.placeholder)
        self["fg"] = self.placeholder_colour
        self.bind("<FocusIn>", self.delete_placeholder)
        self.bind("<FocusOut>", self.apply_placeholder)


    def delete_placeholder(self, event):
        if self["fg"] == self.placeholder_colour:
            self.delete(0, "end")
            self["fg"] = self.text_colour

    def apply_placeholder(self, event):
        if self.get() == "":
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_colour


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()