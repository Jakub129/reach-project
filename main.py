# ________________ TODOs ________________
"""
- import data to the plot
- save/download the plot
- change the plot scales: linear/log
- light/dark mode?
- improve the UI and visuals
- Desmos features: zoom in/out, move around the plot, etc...
"""


#  ________________ LIBRARIES ________________
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import colorchooser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams



# ________________ MAIN PROGRAM _______________
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graphical Preview")
        self.geometry("1080x720")
        self.setup_widgets()


    def setup_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.fig, self.ax  = plt.subplots()
        self.xdata, self.ydata = [x for x in range(-10, 10)], [x**2 for x in range(-10,10)]   
        self.ax.plot(self.xdata, self.ydata)

        # Some default plot
        self.ax.set(title="Enter a title...", xlabel="x", ylabel="y")

        self.matplot_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.matplot_canvas.draw()
        self.matplot_canvas.get_tk_widget().grid(row=0, column=0, rowspan=6, padx=10, pady=10, sticky="nsew")

        self.title_entry = EntryPlaceholder(self, placeholder="Plot Title: ")
        self.title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.title_button = ttk.Button(self, 
                                text="Apply", 
                                cursor="hand2",
                                command=lambda: self.change_title()).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.xaxis_entry = EntryPlaceholder(self, placeholder="Label the x-axis: ")
        self.xaxis_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.xaxis_button = ttk.Button(self, 
                                text="Apply", 
                                cursor="hand2",
                                command=lambda: self.change_xaxis()).grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        
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
                                command=lambda: self.change_colour()).grid(
            row=5, column=2, padx=10, pady=10, sticky="ew"
        )


    def change_title(self):
        if self.title_entry.get() == self.title_entry.placeholder:
            self.ax.set_title("")
        else:
            self.ax.set_title(self.title_entry.get())
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
            rcParams["lines.marker"] = "o"
            self.matplot_canvas.draw()
        elif self.var_points.get() == 0:
            rcParams["lines.marker"] = "none"
            self.matplot_canvas.draw()

    def change_colour(self):
        self.colour_code = colorchooser.askcolor(title="Choose colour")
        #rcParams["lines.color"] = self.colour_code[1]
        self.ax.set_prop_cycle(color=[self.colour_code[1]])
        self.matplot_canvas.draw()


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
