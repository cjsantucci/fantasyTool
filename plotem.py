'''
Created on Aug 30, 2016

@author: chris
'''
import pandas as pd
import numpy as np
import ffl.computeESPN
import matplotlib.pyplot as plt
import matplotlib.text as txt
from matplotlib.backends.backend_pdf import PdfPages
import os
import sys

if __name__ == '__main__':
    

    pData= ffl.computeESPN.process(useESPN= True)
    unqPos= list( pData["position"].unique() )
    
    numPlayers2Plt= 30 
    os.system( " ".join(["rm", "/home/chris/Desktop/fflPlotOutput/2016plots.pdf"])  )
    pp= PdfPages( '/home/chris/Desktop/fflPlotOutput/2016plots.pdf')
    for aPos in unqPos:
        fig = plt.figure()
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.grid(True)
        ax.set_title( aPos )
        
        tData= pData[pData["position"] == aPos]
        tData= tData.sort_values(by= "projected", ascending= False)
        topData= tData[0:numPlayers2Plt]
        plt.plot( np.arange(len(topData.name)), topData.projected, 'ro')
        
                    
        if aPos == "WR":
            excelDataValue= pd.read_excel("/home/chris/Desktop/2016_draftSheet.xlsx",sheetname="merge-WR")
        elif aPos == "RB":
            excelDataValue= pd.read_excel("/home/chris/Desktop/2016_draftSheet.xlsx",sheetname="merge-RB")
        elif aPos == "QB":
            excelDataValue= pd.read_excel("/home/chris/Desktop/2016_draftSheet.xlsx",sheetname="merge-QB")
        elif aPos == "Defense":
            excelDataValue= pd.read_excel("/home/chris/Desktop/2016_draftSheet.xlsx",sheetname="merge-DST")
        elif aPos == "K":
            excelDataValue= pd.read_excel("/home/chris/Desktop/2016_draftSheet.xlsx",sheetname="merge-K")
        topExcelData= excelDataValue[0:numPlayers2Plt]
        topExcelData= topExcelData[topExcelData["$"].values >= 0]
        maxVal= np.max(topData[0:numPlayers2Plt].projected)
        maxValVal= np.max(topExcelData["$"].values)
        yFitValueReal= np.polyfit( np.arange(len(topExcelData)),  topExcelData["$"].values, deg= 1)
        ax.text( int( len(topExcelData)/2 ), maxVal,  str( maxValVal ) + ", " + str( yFitValueReal ), color= "green")
        yFitValue= np.polyfit( np.arange(len(topExcelData)),  topExcelData["$"].values*(maxVal/maxValVal), deg= 1)
        #plt.plot( np.arange(len(topExcelData)), np.arange(len(topExcelData))*yFitValue[0] +  maxVal, 'g')
        for aRowIdx in np.arange( len( topData ) ):
            row= topData[aRowIdx:aRowIdx+1]

            
            if aPos == "Defense":
                textStrPlot= row.team.values[0]
            elif aPos == "K":
                textStrPlot= row.name.values[0] + ", " + row.team.values[0]
            else:
                textStrPlot= row.name.values[0] + ", " + row.team.values[0]
                
            txtHandle= ax.text(aRowIdx, row["projected"].values[0], textStrPlot,\
                 rotation= 90)
        
        
        yFit= np.polyfit( np.arange(numPlayers2Plt),  topData[0:numPlayers2Plt].projected.values, deg= 1)
        ax.set_xlim([-0.5, numPlayers2Plt])
        ax.set_xlabel("index")
        ax.set_ylabel("total projected")
        ax.text( int( numPlayers2Plt/2 ), yFit[1],  str( yFit[0] ) , color= "blue")
        plt.plot( np.arange(numPlayers2Plt), np.arange(numPlayers2Plt)*yFit[0] +  yFit[1])
        pp.savefig( fig )
    plt.show(block= False)


    pp.close()
    print("Done")