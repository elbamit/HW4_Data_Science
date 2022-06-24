from tkinter import StringVar, Tk, Label, Button, Entry, IntVar, Text, END, W, E, filedialog
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
        self.df = None
        self.filepath = StringVar()
        self.num_of_clusters_k = IntVar()
        self.num_of_runs = IntVar()
        self.label = None
        self.model = None

        

        # Text of "select file"
        self.browse_file_label = Label(root,text="Select file",width=40, height=2,fg="black")
        self.browse_file_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

        self.browse_file_entry = Entry(root, width=40, justify='left', textvariable=self.filepath)
        self.browse_file_entry.grid(row=1, column=0, sticky=W, padx=10, pady=10)

        # Button of "browse"
        self.browse_file_button = Button(root, text='Browse', command=self.fileopen)
        self.browse_file_button.grid(row=2, column=0, sticky=W, padx=10, pady=10)

        

        



        # Text of "number of clusters_k"
        self.num_of_clusters_k_label = Label(root,text="Number of clusters k", width=40, height=2,fg="black")
        self.num_of_clusters_k_label.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        # Text box for number of clusters_k
        self.num_of_clusters_k_entry = Entry(root, width=40, textvariable=self.num_of_clusters_k)
        self.num_of_clusters_k_entry.grid(row=4, column=0, sticky=W, padx=10, pady=10)



         # Text of "number of runs"
        self.num_of_runs_label = Label(root,text="Number of runs", width=40, height=2,fg="black")
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







        #TODO I tought this could help to display the scatter plot in the GUI but I didnt understand how it works..

        # figure3 = Figure(figsize=(5,4), dpi=100)
        # ax3 = figure3.add_subplot(111)
        # ax3.scatter(df3['Interest_Rate'],df3['Stock_Index_Price'], color = 'g')
        # scatter3 = FigureCanvasTkAgg(figure3, root) 
        # scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        # ax3.legend(['Stock_Index_Price']) 
        # ax3.set_xlabel('Interest Rate')
        # ax3.set_title('Interest Rate Vs. Stock Index Price')






    def fileopen(self):
        filepath = filedialog.askopenfilename(filetypes=(("xlsx", "*.xlsx"), ("all files", "*.*"))) #===assigns the path to filepath
        self.browse_file_entry.insert(0, filepath)
        self.filepath.set(filepath)

         

    # TODO make checks like if its xlsx or other format. 
    # Loads dataframe, cleans and normalize
    def preprocess(self):
        self.df = km.load_xlsx(self.filepath.get())
        self.df = km.complete_missing_numerical_values(self.df)
        self.df = km.standardize_df(self.df)
        self.df = km.group_by_country(self.df)
        # return



    def cluster(self):
        self.model = km.create_KMeans_model(self.df, self.num_of_clusters_k.get(), self.num_of_runs.get())
        fig = km.scatter_plot(self.model)

        scatterplot_canvas = FigureCanvasTkAgg(fig, master=root)
        scatterplot_canvas.draw()
        scatterplot_canvas.get_tk_widget().grid(row=10, column=0)

        if km.horopleth_map(self.model):
            im = Image.open("Horopleth.png") 

            im_tk = ImageTk.PhotoImage(im.resize((500,300)))
            country_canvas_tk = Label(root,image=im_tk)
            country_canvas_tk.image = im_tk
            country_canvas_tk.grid(column=1, row=10)
        # scatter plot
        # horopleth_map

    


if __name__ == "__main__":
    root = Tk()
    # root.geometry("550x350")
    my_gui = gui(root)
    root.mainloop()


