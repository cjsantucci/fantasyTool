'''
Created on Aug 29, 2016

@author: chris
'''
import numpy as np
import pandas as pd

class dataPoints( object ):
    def __init__( self ) :
        self.passtd= 3
        self.rushtd= 6
        self.rcvtd= 6
        self.passpat= 1
        self.rushpat= 2
        self.rcvpat= 2
        self.ptPerYardPass= 1/25
        self.ptPerYardRush= 1/10
        self.ptPerYardRcv= 1/10
        self.hundredYardRushBonus= 3
        self.hundredYardRcvBonus= 3
        self.threeHundredYardPass= 3
        self.fumble= -1
        self.interception= -1
        self.fieldGoal= 3
        self.kickingPAT= 1
        self.fortyYardBonusKick= 1
        self.D_tdint= 6
        self.D_tdfumb= 6
        self.kickOrPuntReturn= 6
        self.blockKickReturn= 6
        self.otherReturns= 6
        self.safety= 2
        self.D_interception= 1
        self.D_fumble= 1
        self.sack= 1
        
        self.D_points_allowed_0= 10
        self.D_points6= 7
        self.D_points13= 4
        self.D_points17= 1
        self.D_points27= 0
        self.D_points34= -1
        self.D_points35= -4
    
def process(useESPN= False):
    oDP= dataPoints()
    pData= pd.read_csv( "/home/chris/Desktop/fflEspn.csv" )
    if useESPN:
         pData["projected"]= pData.proj_espn
         return pData
    tmp= np.empty(( len(pData),1))
    tmp[:]= np.NaN
    pData["projected"]= tmp
    pData= processNormal( pData, oDP )
    pData= processKickers( pData, oDP )
    pData= processD( pData, oDP )
    
    pData.loc[pData.position=="TE","position"]= "WR"
    
    return pData

def processD( pData, oDP ):
    isD= pData.position== "Defense"
    pData.loc[isD,"projected"] = pData.loc[isD,"proj_espn"]
    return pData

def processKickers( pData, oDP ):    
    isK= pData.position== "K"
    pData.loc[isK,"projected"] = pData.loc[isK,"proj_espn"]
    return pData
    
def processNormal( pData, oDP ):

    proj= pData.rush_td*oDP.rushtd + \
    pData.rush_yds*oDP.ptPerYardRush + \
    \
    pData.pass_td*oDP.passtd + \
    pData.pass_yds*oDP.ptPerYardPass+ \
    pData.pass_int* oDP.interception+ \
    \
    pData.rcv_tds*oDP.rcvtd + \
    pData.rcv_yds*oDP.ptPerYardRcv
    
    
    notD= pData.position != "Defense"
    pData.loc[notD,"projected"]= proj[notD]
    return pData
    
if __name__ == '__main__':
    process()