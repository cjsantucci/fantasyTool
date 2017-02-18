'''
Created on Aug 27, 2016

@author: chris
'''

import requests as rq
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import h5py as h5
import re
import numpy as np
import pandas as pd

class pageData(object):
    def __init( self ):
        self._rowDataList= list()
    
class espnDataGrabber(object):
    '''
    classdocs
    '''

    def __init__( self ):
        self._site= "http://games.espn.com/ffl/tools/projections"
        self.maxDepth= 1000
        topList = list()
        outputList, levelDownRecurse= self._processPage( self._site, topList, 0 ) # recursive
        fflData= pd.DataFrame( outputList )
        fflData.to_csv("/home/chris/Desktop/fflEspn.csv")
        print()

    def _init( self ):
       pass
    
    def _processPage( self, pageAddress, topList, levelDownRecurse ):
        levelDownRecurse += 1
        print("level_down" + str(levelDownRecurse))
        session= rq.session()
        req= session.get( pageAddress )
        if req.ok:
            doc= bs( req.content, 'lxml' )
        else:
            assert False, "not ok"
        
        hyperList= doc.findAll('a')
        
        nextTableList= list()
        for aTag in hyperList:
            if re.search( 'projection.*startIndex', aTag['href'] ) and re.search( "NEXT", aTag.text ):
                if aTag['href'] not in nextTableList:
                    nextTableList.append( aTag['href'] )
                    
        tmpTableList= doc.findAll('table')
        tableBodyList= list()
        for aTable in tmpTableList:
            if "tableBody" in aTable['class']:
                tableBodyList.append( aTable )
            
        assert len(tableBodyList)  == 1, "table list too long."
        
        thisTable= tableBodyList[0]
        playerRows= thisTable.findAll("tr")
        for aRow in playerRows:
            if not self.isTableHead( aRow ):
                topList.append( self.parseTableRowTag( aRow ) )
    
        if len( nextTableList ) > 0 and levelDownRecurse <= self.maxDepth:
            topList, levelDownRecurse= self._processPage( nextTableList[0], topList, levelDownRecurse )
        
        return topList, levelDownRecurse
    # en processPage
        
    def parseTableRowTag( self, aRow ):
        tagDataList= aRow.findAll( 'td' ) 
        playerDict = dict()
        colCount= 0;
        for aTag in tagDataList:
            if aTag["class"] == ['playertablePlayerName']:
                playerLink= aTag.contents
                playerDict["seasonid"]= int( playerLink[0]["seasonid"] )
                if re.search( "D/ST", aTag.text ):
                    playerDict["position"] = "Defense"
                    tmp= aTag.text.split(" ")
                    playerDict["team"]= tmp[0]
                else:
                    tmp= aTag.text.split(",")
                    playerDict["name"]= tmp[0].strip()
                    if len( tmp ) < 2:
                        print()
                    tmp2= tmp[1].split('\xa0')
                    playerDict["team"]= tmp2[0].strip()
                    playerDict["position"]= tmp2[1].strip()
                
            elif "playertableStat" in aTag["class"]:
                if colCount== 0:
                    pass # attempt
                elif colCount==1:
                    playerDict["pass_yds"]= attemptFloatParse(aTag.text)
                elif colCount==2:
                    playerDict["pass_td"]= attemptFloatParse(aTag.text)
                elif colCount==3:
                    playerDict["pass_int"]= attemptFloatParse(aTag.text)
                elif colCount==4:
                    playerDict["rushes"]= attemptFloatParse(aTag.text)
                elif colCount==5:
                    playerDict["rush_yds"]= attemptFloatParse(aTag.text)
                elif colCount==6:
                    playerDict["rush_td"]= attemptFloatParse(aTag.text)
                elif colCount==7:
                    playerDict["receptions"]= attemptFloatParse(aTag.text)
                elif colCount==8:
                    playerDict["rcv_yds"]= attemptFloatParse(aTag.text)
                elif colCount==9:
                    playerDict["rcv_tds"]= attemptFloatParse(aTag.text)
                elif colCount==10:
                    playerDict["proj_espn"]= attemptFloatParse(aTag.text)
                colCount+=1
            else:
                print()
              
        return playerDict
        
    def isTableHead( self, aRow ):
        out= False
        if hasattr( aRow, "class" ):
            classListOfTableRow= aRow["class"]
            for aClass in classListOfTableRow:
                if re.search( "HEAD", aClass.upper() ):
                    return True 
        else:
            return False
        
def attemptFloatParse(strIn):
    try:
        return( float( strIn) )
    except:
        return np.NAN
    
if __name__ == '__main__':
    oESPN= espnDataGrabber()