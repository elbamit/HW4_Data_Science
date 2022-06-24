import os
from tkinter import StringVar, Tk, Label, Button, Entry, IntVar, Text, END, W, E, filedialog, messagebox
import matplotlib
from matplotlib.pyplot import plot
import pandas as pd
import KMeans as km

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from PIL import Image, ImageTk


class gui:

    def __init__(self, root):
        self.root = root
        self.root.title("K Means Clustering")
        self.df = None
        self.filepath = StringVar()
        self.num_of_clusters_k = IntVar()
        self.num_of_runs = IntVar()
        self.label = None
        self.model = None

        self.pathFlag = False

        # Text of "select file"
        self.browse_file_label = Label(root, text="Select file", width=40, height=2, fg="black")
        self.browse_file_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.browse_file_entry = Entry(root, state='disabled', width=40, justify='left', textvariable=self.filepath)
        self.browse_file_entry.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        # Button of "browse"
        self.browse_file_button = Button(root, text='Browse', command=self.fileopen)
        self.browse_file_button.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        # Text of "number of clusters_k"
        self.num_of_clusters_k_label = Label(root, text="Number of clusters k", width=40, height=2, fg="black")
        self.num_of_clusters_k_label.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        # Text box for number of clusters_k
        self.num_of_clusters_k_entry = Entry(root, width=40, textvariable=self.num_of_clusters_k)
        self.num_of_clusters_k_entry.grid(row=4, column=0, sticky=W, padx=10, pady=10)

        # Text of "number of runs"
        self.num_of_runs_label = Label(root, text="Number of runs", width=40, height=2, fg="black")
        self.num_of_runs_label.grid(row=5, column=0, sticky=W, padx=10, pady=10)

        # Text box for number of runs
        self.num_of_runs_entry = Entry(root, width=40, textvariable=self.num_of_runs)
        self.num_of_runs_entry.grid(row=6, column=0, sticky=W, padx=10, pady=10)

        # Button of "Pre-process"
        self.browse_file_button = Button(root, text='Pre-process', command=self.preprocess)
        self.browse_file_button.grid(row=7, column=0, sticky=W, padx=10, pady=10)

        # Button of "Cluster"
        self.browse_file_button = Button(root, text='Cluster', command=self.cluster)
        self.browse_file_button.grid(row=9, column=0, sticky=W, padx=10, pady=10)

        # TODO I tought this could help to display the scatter plot in the GUI but I didnt understand how it works..

        # figure3 = Figure(figsize=(5,4), dpi=100)
        # ax3 = figure3.add_subplot(111)
        # ax3.scatter(df3['Interest_Rate'],df3['Stock_Index_Price'], color = 'g')
        # scatter3 = FigureCanvasTkAgg(figure3, root) 
        # scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        # ax3.legend(['Stock_Index_Price']) 
        # ax3.set_xlabel('Interest Rate')
        # ax3.set_title('Interest Rate Vs. Stock Index Price')

    def fileopen(self):
        filepath = filedialog.askopenfilename(
            filetypes=(("xlsx", "*.xlsx"), ("all files", "*.*")))  # ===assigns the path to filepath
        self.browse_file_entry.insert(0, filepath)
        self.filepath.set(filepath)
        if self.filepath.get() != "":
            self.pathFlag = True
        else:
            self.pathFlag = False

    # TODO make checks like if its xlsx or other format.
    # Loads dataframe, cleans and normalize
    def preprocess(self):

        if self.findErrors():
            return
        else:
            self.df = km.load_xlsx(self.filepath.get())
            if self.df is None:
                messagebox.showinfo(title="K Means Clustering", message="\n You must select a valid file first (excel)")
            else:
                self.df = km.complete_missing_numerical_values(self.df)
                self.df = km.standardize_df(self.df)
                self.df = km.group_by_country(self.df)
                self.df.to_excel("PreProcessedData.xlsx")
                messagebox.showinfo(title="K Means Clustering", message="\n Preprocessing completed successfully!")


    def findErrors(self):
        errorsString = ""
        k_is_empty = False
        runs_is_empty = False

        # validate the path box
        if not self.pathFlag:
            errorsString = "\n - You must select a valid file first"

        # validate the num_of_k
        try:
            self.num_of_clusters_k.get()
        except:
            errorsString += "\n - You must insert the number of clusters"
            k_is_empty = True
        finally:
            if not k_is_empty:
                if not 0 < self.num_of_clusters_k.get() <= 50:
                    errorsString += "\n - The number of clusters must be between 1 - 50"

            # validate the num_of_runs
            try:
                self.num_of_runs.get()
            except:
                errorsString += "\n - You must insert the number of runs"
                runs_is_empty = True
            finally:
                if not runs_is_empty:
                    if not 0 < self.num_of_runs.get() <= 50:
                        errorsString += "\n - The number of runs must be between 1 - 50"

                # checks if there are any errors
                if errorsString:
                    messagebox.showinfo(title="K Means Clustering", message=errorsString)
                    return True  # There is some Errors
                else:
                    return False  # There is no Errors

    def cluster(self):
        self.model = km.create_KMeans_model(self.df, self.num_of_clusters_k.get(), self.num_of_runs.get())
        fig = km.scatter_plot(self.model)

        scatterplot_canvas = FigureCanvasTkAgg(fig, master=root)
        scatterplot_canvas.draw()
        scatterplot_canvas.get_tk_widget().grid(row=10, column=0)

        if km.choropleth_map(self.model):
            im = Image.open("Horopleth.png")

            im_tk = ImageTk.PhotoImage(im.resize((500, 400)))
            country_canvas_tk = Label(root, image=im_tk)
            country_canvas_tk.image = im_tk
            country_canvas_tk.grid(column=1, row=10)
            messagebox.showinfo(title="K Means Clustering", message="\n The clustering process has been completed!")


if __name__ == "__main__":
    root = Tk()
    # root.geometry("550x350")
    my_gui = gui(root)
    root.mainloop()




# 3. when selecting file, clear it, and then select again -> error

