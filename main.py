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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt



# ________________ MAIN PROGRAM _______________
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graphical Preview")
        self.geometry("1080x720")
        
        self.setup_widgets()


    def setup_widgets(self):
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.fig, self.ax  = plt.subplots()
        self.xdata, self.ydata = [x for x in range(0, 5)], [x**2 for x in range(0,5)]   
        self.ax.plot(self.xdata, self.ydata)

        self.ax.set_title("Enter a title...")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        self.matplot_canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.matplot_canvas.draw()
        self.matplot_canvas.get_tk_widget().grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")

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