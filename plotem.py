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
    ax.set_ylabel( "projections" )
    
    return fig, ax


def makePlotsForEach( pData, meanField, meanFieldRank, computedField, unqPos, unqSite= None, plotTextRanks= False ):
    
    
    sortBySitesAndPosition( pData, fields= [ meanField ], \
                                 ascending= False )
    
    numPlayers2Plt= 30 
    os.system( " ".join(["rm", "/home/chris/Desktop/fflOutput/2017plots.pdf"])  )
    pp= PdfPages( '/home/chris/Desktop/fflOutput/2017plots.pdf')
    
    for aPos in unqPos:
        print(aPos)
        posData= pData[ pData["POSITION"] == aPos ]
        posData= posData.sort_values( by= meanField, ascending= False )
        
        f, ax= setupSinglePlot( xlabel= "rank", title= aPos, xlim=[-0.5, numPlayers2Plt] )
        plt.show(block= False)

        dataList= []
        legList= []
        
        # just pick CBS, since the mean is stored in any of them
        cpmData= posData[ posData["SITE_REGEX"] == "CBS" ]
        cpmData= cpmData[ 0:numPlayers2Plt ]
        plt.plot( np.arange(len(cpmData.NAME)), cpmData[meanField], "+" )
        dataList.append( list(cpmData[meanField].values.copy()) )
        legList.append( meanField )
    
        if unqSite is None:
            unqSite= sorted( list( posData["SITE_REGEX"].unique() ) )
        for aSite in unqSite:
            tData= posData[ posData["SITE_REGEX"] == aSite ]
            tData= tData[ 0:numPlayers2Plt ]
            plt.plot( np.arange(len(tData.NAME)), tData[computedField], "o" )
            dataList.append( list(tData[computedField].values.copy()) )
            legList.append( aSite + "_" + computedField )
            
            
            if meanField == "PROJECTED_PTS_mean":
                rankField= "site_rank"
            else:
                rankField= "computed_rank" 
            
            if plotTextRanks:
                count= 0
                for _, row in tData.iterrows():
    #                 print(row)
                    idx= tData.index[count]
                    ax.text(count, tData[computedField][idx], str( int( tData[rankField][idx] ) ) )
                    count += 1

#             plt.plot( np.arange(len(tData.NAME)), tData["PROJECTED_PTS"], "o" )
#             dataList.append( list(tData["PROJECTED_PTS"].values.copy()) )
#             legList.append( aSite + "PROJECTED_PTS" )
        ax.legend(legList)      
        
        mins= list( np.array(dataList).transpose().min(axis=1) )
        count= 0
        for _, row in cpmData.iterrows():
            if aPos == "Defense":
                textStrPlot= row.TEAM
            elif aPos == "K":
                textStrPlot= row.NAME + ", " + row.TEAM
            else:
                textStrPlot= row.NAME + ", " + row.TEAM
                 
            txtHandle= ax.text(count, mins[count]-10, textStrPlot,\
                 rotation= 90)
            count += 1

        pp.savefig( f )

    pp.close()
    

if __name__ == '__main__':
    
#     obj= Auction( csv= "/home/chris/Desktop/fflOutput/fflAll_2017.csv" )
#     obj.process()
#     pData= obj.pData.copy()
    pData= pd.read_csv( '/home/chris/Desktop/fflOutput/fflAll_withComputed2017.csv' )
    
    #unqPos= sorted( list( pData["POSITION"].unique() ) )
    unqPos= [ "WR" ]
    unqPos= [ "WR", "RB", "QB" ]
    unqSite= None
#     unqSite= ["FFTODAY"]
    
    makePlotsForEach( pData, "computed_projected_mean", "computed_projected_mean_rank" , "computed_projected", unqPos, unqSite )
#     makePlotsForEach( pData, "PROJECTED_PTS_mean", "projected_mean_rank", "PROJECTED_PTS", unqPos, unqSite )

    print("Done")