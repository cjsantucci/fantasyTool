'''
Created on Sep 3, 2016

@author: chris
'''
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import pyplot as plt
from mpldatacursor import datacursor 

class fflMain(object):
    '''
    classdocs
    '''


    def __init__( self, pandasData ):
        self.createFigure()
        self.createListBox()
        print()
        
    def createListBox( self ):
        self.lbMain= tk.Listbox()
    
    def createFigure( self ):
#         tkf= tk.Frame()
#         self.mainFig= matplotlib.figure.Figure(figsize= (5,5),dpi=100)
        self.mainFig= plt.figure()
        a = self.mainFig.add_subplot(111)
        line= a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

#         plt.show( block= False )

        root= tk.Tk()
        root.iconbitmap('/home/chris/Desktop/download.jpg')
        root.title("blah")
        canvas= FigureCanvasTkAgg( self.mainFig, master= root )
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, root)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        dcObj= datacursor(line, snap= True)
        print() 
        
if __name__ == '__main__':
    pData= pd.read_csv( "/home/chris/Desktop/fflEspn.csv" )
    fflMain( pData )
        