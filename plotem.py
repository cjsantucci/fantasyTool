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


def makePlotsForEach( pp, pData, meanField, meanFieldRank, computedField, unqPos, unqSite= None, plotTextRanks= False, player= None ):
    
    if "DST" in unqPos and "K" in unqPos:
        numPlayers2Plt= 32 
        asc= True
    else:
        numPlayers2Plt= 30 
        asc= False
    
#     sortBySitesAndPosition( pData, fields= [ meanField ], \
#                                  ascending= asc )
    
    os.system( " ".join(["rm", "/home/chris/Desktop/fflOutput/2017plots.pdf"])  )
    
    for aPos in unqPos:
        print(aPos)
        
        if aPos == "DST":
            nameStr= "TEAM"
        else:
            nameStr= "NAME"
        
        posData= pData[ pData["POSITION"] == aPos ]
        posData= posData.sort_values( by= meanField, ascending= False )
        
        f, ax= setupSinglePlot( xlabel= "rank", title= aPos, xlim=[-0.5, numPlayers2Plt] )
        
        plt.show(block= False)
#         mng = plt.get_current_fig_manager()
#         mng.window.showMaximized()

        dataList= []
        legList= []

        if aPos == "DST":
            namesOnlyData= posData.drop_duplicates( nameStr )
        else:
            namesOnlyData= posData.drop_duplicates( nameStr )
        
        namesOnlyData= namesOnlyData.sort_values( meanField, ascending= asc ).reset_index()
        namesOnlyData= namesOnlyData[0:numPlayers2Plt]
        namesForPlot= set( namesOnlyData[nameStr] )
    
        if unqSite is None:
            unqSite= sorted( list( posData["SITE_REGEX"].unique() ) )
        for aSite in unqSite:
            tData= posData[ posData["SITE_REGEX"] == aSite ]
            if aPos == "K" or aPos == "DST":
                tData= tData.sort_values( meanField, ascending= True ).reset_index()
            else:
                tData= tData.sort_values( meanField, ascending= False ).reset_index()

            lNames= np.ndarray( shape= (len(tData,)), dtype=bool )
            for aNameForPlot in namesForPlot:
                lNames= np.logical_or( lNames, tData[ nameStr ] == aNameForPlot )
                
            tData= tData.loc[ lNames ]
            
            checkNames= set( tData[ nameStr ] )
            check1= namesForPlot.difference( checkNames )
            check2= checkNames.difference( namesForPlot )
            assert len( check1 ) == 0 and len( check2 ) == 0, "lens do not match logic error--check check1 and check2"
                
            plt.plot( np.arange(len(tData.NAME)), tData[computedField], "o", markersize=4 )
            dataList.append( list(tData[computedField].values.copy()) )
            legList.append( aSite + "_" + computedField )
            
            if meanField == "PROJECTED_PTS_mean":
                rankField= "projected_rank"
            else:
                rankField= "computed_rank" 
            
            if plotTextRanks:
                count= 0
                for _, row in tData.iterrows():
    #                 print(row)
                    idx= tData.index[count]
                    ax.text(count, tData[computedField][idx], str( int( tData[rankField][idx] ) ) )
                    count += 1

        # just pick CBS, since the mean is stored in any of them
        cpmData= posData[ posData["SITE_REGEX"] == "CBS" ]
        if aPos == "K" or aPos == "DST":
            cpmData= cpmData.sort_values( meanField, ascending= True )
        else:
            cpmData= cpmData.sort_values( meanField, ascending= False ).reset_index()
        cpmData= cpmData[ 0:numPlayers2Plt ]
        
        plt.plot( np.arange(len(cpmData.NAME)), cpmData[meanField], "+" )
        plt.step( np.arange(len(cpmData.NAME)), cpmData[meanField] )
        dataList.append( list(cpmData[meanField].values.copy()) )
        legList.append( meanField )
        
        if aPos == "K" or aPos == "DST":
            ax.legend(legList, bbox_to_anchor=(0.3, 0.8))
        else:            
            ax.legend(legList, bbox_to_anchor=(0.8, 0.8))
        
        mins= list( np.array(dataList).transpose().min(axis=1) )
        count= 0
        for _, row in cpmData.iterrows():
            if aPos == "DST":
                textStrPlot= row.TEAM
            else:
                textStrPlot= row.NAME + ", " + row.TEAM
            
            if aPos == "DST" or aPos == "K":
                yLabelShift= 2
            else:
                yLabelShift= 2
                
            txtHandle= ax.text(count, mins[count]-yLabelShift, textStrPlot,\
                    rotation= 90)
            count += 1
            
        pp.savefig( f )

if __name__ == '__main__':
    
#     obj= Auction( csv= "/home/chris/Desktop/fflOutput/fflAll_2017.csv" )
#     obj.process()
#     pData= obj.pData.copy()
    pData= pd.read_csv( '/home/chris/Desktop/fflOutput/fflAll_withComputed2017.csv' )
    
    pp= PdfPages( '/home/chris/Desktop/fflOutput/2017plots.pdf' )
    
    unqPos= [ "WR", "RB", "QB" ]
#     unqPos= [ "WR" ]
    unqSite= None
#     unqSite= [ "ESPN" ]
    player= None
    #player= "Kelvin Benjamin"
#     unqSite= ["FFTODAY"]
    makePlotsForEach( pp, pData, "computed_projected_mean", "computed_projected_mean_rank" , "computed_projected", unqPos, unqSite, player= player )
    
    unqPos= [ "DST"  ]
    makePlotsForEach( pp, pData, "computed_projected_mean_rank", "computed_projected_mean_rank" , "computed_rank", unqPos, unqSite, player= player )
#     makePlotsForEach( pData, "PROJECTED_PTS_mean", "projected_mean_rank", "PROJECTED_PTS", unqPos, unqSite )
    pp.close()

    print("Done")