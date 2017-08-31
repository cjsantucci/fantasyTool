'''
Created on Aug 3, 2017

@author: chris
'''
from ffl.compute import ComputeData, sortBySitesAndPosition
import numpy as np 

class Auction( ComputeData ):

    def __init__( self, **kwargs ):
        '''
        Constructor
        '''
        super( Auction, self ).__init__( **kwargs ) # run base constructor
    
    def process( self, saveCSV ):
        super( Auction, self ).process()
        self.pData.loc[ self.pData.POSITION == "TE", "POSITION" ]= "WR"
        self.wrExtraSort()
        if saveCSV:
            print("saved")
            self.pData.to_csv( "/home/chris/Desktop/fflOutput/fflAll_withComputed2017.csv" )
        
    
    def wrExtraSort( self ):

        sortBySitesAndPosition( self.pData, fields= ["computed_projected_mean"], \
                                     positions= ["QB", "RB", "WR"] , \
                                     ascending= False )
        
if __name__ == '__main__':
    oAuction= Auction( csv= "/home/chris/Desktop/fflOutput/fflAll_2017.csv" )
    oAuction.process( saveCSV= True )
    print("finished")
        