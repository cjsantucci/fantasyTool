'''
Created on Aug 3, 2017

@author: chris
'''
from ffl.compute import ComputeData
import numpy as np 

class Auction( ComputeData ):

    def __init__( self, **kwargs ):
        '''
        Constructor
        '''
        super( Auction, self ).__init__( **kwargs ) # run base constructor
    
    def process( self ):
        super( Auction, self ).process()
        self.pData.loc[ self.pData.POSITION == "TE", "POSITION" ]= "WR"
    
    def wrExtraSort( self ):
        pData= self.pData
        for aSite in sorted( list( pData["SITE_REGEX"].unique() ) ):
            lAll= np.logical_and( pData["SITE_REGEX"] == aSite, pData["POSITION"] == "WR" ) 
            tData= posData[ lSite ]
            tData= tData.sort_values( by= meanField, ascending= False )
        
if __name__ == '__main__':
    oAuction= Auction( csv= "/home/chris/Desktop/fflOutput/fflAll_2017.csv" )
    oAuction.process()
        