'''
Created on Aug 3, 2017

@author: chris

'''
'''
Created on Aug 29, 2016

@author: chris
'''
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
from abc import abstractmethod, abstractproperty, ABCMeta

class ComputeData( object, metaclass= ABCMeta ):
    
    _pointsDict= { "PASSING_TD": 3.0, "RUSHING_TD": 6.0,"RECEIVING_TD": 6.0, \
                         "fumble":-1.0, "PASSING_INT": -1.0, \
                         "passing_300":3.0, "passing_400":3.0, "passing_pts_per_yards":1.0/25.0, \
                         "rushing_100":3.0, "rushing_200":3.0, "rushing_pts_per_yards":1.0/10.0, \
                         "receiving_100":3.0, "receiving_200":3.0, "receiving_pts_per_yards":1.0/10.0,
                         
                         }
    
    pData= None
    
    def __init__( self, csv= None ) :
        self.csv= csv
        self.pData= pd.read_csv( self.csv )
    
    
    def process( self ):
        
        self.pData= self.pData.copy()
        pData= self.pData
        
        self.processNormal()
        self.processKickers()
        self.processD()
    
        self.computeMeanProjected()
        self.computeRanks()
    
    def computeRanks( self ):
        """Store the index as it was in the website before we start sorting stuff around"""
        
        pData= self.pData
        
        unqPos= list( pData["POSITION"].unique() )
        unqSite= list( pData["SITE_REGEX"].unique() )
        for aSite in unqSite:
            for aPos in unqPos:
                lAll= np.logical_and( pData["POSITION"] == aPos, pData["SITE_REGEX"] == aSite )
                
                tmpTable= pData.loc[ lAll ]
                rankArray= tmpTable.reset_index().index+1
                pData.loc[lAll,"projected_rank"]= rankArray.astype(float)
                
                tmpTable= pData.loc[ lAll ]
                tmpTable= tmpTable.sort_values( "computed_projected" , ascending= False )
                rankArray= np.arange( 0, len( tmpTable.index ) )+1
                pData.loc[ tmpTable.index, "computed_rank" ]= rankArray.astype(float) 
                
                
#                 tmpTable= pData.loc[ lAll ]
#                 tmpTable= tmpTable.sort_values( "computed_projected_mean" , ascending= False )
#                 rankArray= np.arange( 0, len( tmpTable.index ) )+1
#                 pData.loc[ tmpTable.index, "computed_projected_mean_rank" ]= rankArray.astype(float) 
#                 
#                 tmpTable= pData.loc[ lAll ]
#                 tmpTable= tmpTable.sort_values( "PROJECTED_PTS_mean" , ascending= False )
#                 rankArray= np.arange( 0, len( tmpTable.index ) )+1
#                 pData.loc[ tmpTable.index, "projected_mean_rank" ]= rankArray.astype(float) 
                
        unqPos= list( pData["POSITION"].unique() )
        for aPos in unqPos:
            if aPos == "DST":
                pField= "TEAM"
            else:
                pField= "NAME"
            
            unqPlayer= list( pData[ pField ].unique() )
            
            for aPlayer in unqPlayer:
                lAll= np.logical_and( pData["POSITION"] == aPos, pData[ pField ] == aPlayer )
                pData.loc[ lAll , "projected_mean_rank" ]= pData.loc[ lAll , "projected_rank" ].mean()
                pData.loc[ lAll , "computed_projected_mean_rank" ]= pData.loc[ lAll , "computed_rank" ].mean()
                
                
    
    def computeMeanProjected( self ):
        """ compute the means for each player as projected by league points"""
        
        pData= self.pData
        
        unqPos= list( pData["POSITION"].unique() )
        for aPos in unqPos:
            lPos= pData["POSITION"] == aPos 
            
            if aPos == "DST":
                fieldStr= "TEAM"
            else:
                fieldStr= "NAME"
             
            unqPlayer= list( pData.loc[ lPos, fieldStr ].unique() )
            for aPlayer in unqPlayer:
                lPlayer= pData[ fieldStr ] == aPlayer
                lAll= np.logical_and( lPos, lPlayer )
                
                pData.loc[lAll, 'computed_projected_mean']= pData.loc[lAll, "computed_projected" ].mean()
                pData.loc[lAll, 'PROJECTED_PTS_mean']= pData.loc[lAll, "PROJECTED_PTS" ].mean()

#               
    def processD( self ):
        pData= self.pData
        
        isD= pData["POSITION"]== "DST"
        pData.loc[isD,"computed_projected"] = pData.loc[isD,"PROJECTED_PTS"]
    
    def processKickers( self ):
        pData= self.pData
            
        isK= pData["POSITION"]== "K"
        pData.loc[isK,"computed_projected"] = pData.loc[isK,"PROJECTED_PTS"]
        
    def processNormal( self ):
        pData= self.pData
        podi= self._pointsDict
        
        temp= pData.fillna(0)
        
        proj= temp["RUSHING_TD"]*podi["RUSHING_TD"] + \
        temp["RUSHING_YDS"]*podi["rushing_pts_per_yards"] + \
        \
        temp["PASSING_TD"]*podi["PASSING_TD"] + \
        temp["PASSING_YDS"]*podi["passing_pts_per_yards"]+ \
        temp["PASSING_INT"]* podi["PASSING_INT"]+ \
        \
        temp["RECEIVING_TD"]*podi["RECEIVING_TD"] + \
        temp["RECEIVING_YDS"]*podi["receiving_pts_per_yards"]
        
        
        notD= np.logical_and( pData["POSITION"] != "DST",  pData["POSITION"] != "K")
        pData.loc[notD,"computed_projected"]= proj[notD]
        
def sortBySitesAndPosition( pData, fields= None, positions= None, ascending= False ):
    """ Sort position groups for each site by whatever field requested """
    
    assert isinstance( pData, pd.DataFrame ), "pData must be pandas DataFrame"
    assert isinstance( fields, list ), "fields must be a list of fields to sort"
    
    if positions is None:
        positions= sorted( pData["POSITION"].unique() )
        
    for aSite in sorted( list( pData["SITE_REGEX"].unique() ) ):
        for aPosition in positions:
            lAll= np.logical_and( pData["SITE_REGEX"] == aSite, pData["POSITION"] == aPosition )
            tData= pData.loc[ lAll ]
            tDataSort= tData.sort_values( fields , ascending= ascending )
            tDataSort.reset_index()
            tDataSort.index= list(tData.index)
            pData.loc[ lAll ]= tDataSort    
            
    
if __name__ == '__main__':
    oComp= ComputeData( csv= "/home/chris/Desktop/fflOutput/fflAll_2017.csv" )
    oComp.process()