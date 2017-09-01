'''
Created on Aug 30, 2016

@author: chris
'''
from ffl.auctionLeague import Auction
from ffl.compute import sortBySitesAndPosition
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
import os

def setupSinglePlot( xlabel= "X", title= "", xlim= None, grid= True ):
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    ax.grid( grid )
    ax.set_title( title )
    if xlim is not None:
        ax.set_xlim( xlim )
    ax.set_xlabel( xlabel )
    
    return fig, ax


def makePlotsForEach( pp, pData, meanField, meanFieldRank, computedField, unqPos, unqSite= None, plotTextRanks= False, player= None ):
    
    numPlayers2Plt= 32
    
    for aPos in unqPos:
        print(aPos)
        
        if aPos == "DST":
            nameStr= "TEAM"
        else:
            nameStr= "NAME"
            
        if aPos == "DST" or aPos == "K":
            asc= True
            ylabelStr= "position rank"
        else:
            asc= False
            ylabelStr= "projections"
            
        posData= pData[ pData["POSITION"] == aPos ]
        posData= posData[[ nameStr, "SITE_REGEX", meanField, computedField ]]
        pivData= posData.pivot_table( index= [ nameStr, "SITE_REGEX" ] )
        tmp= pivData.unstack()
        sortedTabMeanField= tmp[ meanField ].sort_values( "CBS", ascending= asc )
        sortedTabMeanField= sortedTabMeanField[0:numPlayers2Plt]
        sortedTabCompField= tmp.loc[ sortedTabMeanField.index ][ computedField ]
        sortedTabCompField= sortedTabCompField[0:numPlayers2Plt]
        
        f, ax= setupSinglePlot( xlabel= "rank", title= aPos, xlim=[-0.5, numPlayers2Plt] )
        
        ax.set_ylabel( "projections" )
        
        plt.show(block= False)
#         mng = plt.get_current_fig_manager()
#         mng.window.showMaximized()
        legList= []
        
        plt.plot( np.arange(len(sortedTabMeanField)), sortedTabMeanField.CBS, "+" )
        
        plt.step( np.arange(len(sortedTabMeanField)), sortedTabMeanField.CBS )
        legList.append( meanField )
        legList.append( meanField )
        
        for aSite in list( sortedTabCompField.columns ):
            plt.plot( np.arange(len(sortedTabMeanField)), sortedTabCompField[aSite], 'o', markersize= 2 )
            legList.append( aSite )
            
        if aPos == "K" or aPos == "DST":
            ax.legend(legList, bbox_to_anchor=(0.5, 0.8))
        else:            
            ax.legend(legList, bbox_to_anchor=(0.5, 0.8))
        
        count= 0
        yLabelShift= 2
        for name, row in sortedTabMeanField.iterrows():
            
            tMin= sortedTabCompField.loc[ name ]
            tMin= min( tMin.values[ np.logical_not( np.isnan( tMin.values ) ) ] )
            
            _= ax.text(count, tMin-yLabelShift, name,\
                    rotation= 90, fontsize= 7)
            count += 1
            
        pp.savefig( f )

if __name__ == '__main__':

    os.system( " ".join(["rm", "/home/chris/Desktop/fflOutput/2017plots.pdf"])  )
    pData= pd.read_csv( '/home/chris/Desktop/fflOutput/fflAll_withComputed2017.csv' )
    
    pp= PdfPages( '/home/chris/Desktop/fflOutput/2017plots.pdf' )
    
    unqPos= [ "WR", "RB", "QB" ]
    unqSite= None
    player= None

    makePlotsForEach( pp, pData, "computed_projected_mean", "computed_projected_mean_rank" , "computed_projected", unqPos, unqSite, player= player )
    
    unqPos= [ "K", "DST" ]
    makePlotsForEach( pp, pData, "computed_projected_mean_rank", "computed_projected_mean_rank" , "computed_rank", unqPos, unqSite, player= player )
    
    pp.close()

    print("Done")