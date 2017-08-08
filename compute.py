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
        self.computeMeans()
        self.computeComputedRank()

    def computeComputedRank( self ):
        pass
    
    def computeMeans( self ):
        pData= self.pData
        
        unqPos= list( pData["POSITION"].unique() )
        for aPos in unqPos:
            lPos= pData["POSITION"] == aPos 
            unqPlayer= list( pData.loc[ lPos, "NAME" ].unique() ) 
            for aPlayer in unqPlayer:
                lPlayer= pData["NAME"] == aPlayer
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
        
        proj= pData["RUSHING_TD"]*podi["RUSHING_TD"] + \
        pData["RUSHING_YDS"]*podi["rushing_pts_per_yards"] + \
        \
        pData["PASSING_TD"]*podi["PASSING_TD"] + \
        pData["PASSING_YDS"]*podi["passing_pts_per_yards"]+ \
        pData["PASSING_INT"]* podi["PASSING_INT"]+ \
        \
        pData["RECEIVING_TD"]*podi["RECEIVING_TD"] + \
        pData["RECEIVING_YDS"]*podi["passing_pts_per_yards"]
        
        
        notD= np.logical_and( pData["POSITION"] != "DST",  pData["POSITION"] != "K")
        self.pData.loc[notD,"computed_projected"]= proj[notD]
        
#     def processBinomial_onManyYards( self ):
#         
#         n, p = 16, 
    
if __name__ == '__main__':
    oComp= ComputeData( csv= "/home/chris/Desktop/fflOutput/fflAll_2017.csv" )
    oComp.process()