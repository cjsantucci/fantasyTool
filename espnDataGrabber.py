'''
Created on Aug 27, 2016

@author: chris
'''

from ffl import projTableBase
from ffl.projTableBase import ProjTableBase
import re
    
class ESPN_Normal( ProjTableBase ): # inherit
    
    _finalRemap= {"TOTAL_PTS":"PROJECTED_PTS"}
    _nameRegex= "ESPN"
    _saveCSV= "fflEspn.csv"
    _statColRemap= {"RUSH":"ATT"}
    _tableColumnNames= [ "PASSING","RECEIVING", "RUSHING", "TOTAL" ]
    
    def __init__( self ):
        
        columnMethodOverRideList= [ ( 1, self._setRank ),\
                                    ( 2, self._parsePlayerNameData ),\
                                    ( 3, self._passCompAttOverrid ), \
                                   ]
        siteList= [ "http://games.espn.com/ffl/tools/projections?slotCategoryId=0",\
                     "http://games.espn.com/ffl/tools/projections?slotCategoryId=2",\
                     "http://games.espn.com/ffl/tools/projections?slotCategoryId=4",\
                     "http://games.espn.com/ffl/tools/projections?slotCategoryId=6",\
                     ]
        
        super( ESPN_Normal, self ).__init__() # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
    
    def _isnextSiteLink( self, aTag, pageAddress, nextTableList ):
        return re.search( 'projection.*startIndex', aTag['href'] ) and re.search( "NEXT", aTag.text.strip() ) 
    
    def _passCompAttOverrid( self, playerDict, aRow, aTag, rowNum, colNum, site  ):
        
        try:
            splitList= aTag.string.split("/")
            playerDict["PASSING_CMP"]= float( splitList[0] )
            playerDict["PASSING_ATT"]= float( splitList[0] )
            
        except:
            return
    
        
    def _setRank( self, playerDict, aRow, aTag, rowNum, colNum, site  ):
        playerDict["POSITION_RANK"]= projTableBase.attemptFloatParse( aTag.text )
    
    def _parsePlayerNameData( self, playerDict, aRow, aTag, rowNum, colNum, pageAddress ):
        playerLink= aTag.contents
        playerDict["SEASONID"]= int( playerLink[0]["seasonid"] )
        if re.search( "D/ST", aTag.text ):
            playerDict["POSITION"] = "DST"
            tmp= aTag.text.split(" ")
            playerDict["TEAM"]= tmp[0]
        else:
            tmp= aTag.text.split(",")
            playerDict["NAME"]= tmp[0].strip()
            if len( tmp ) < 2:
                print()
            tmp2= tmp[1].split('\xa0')
            playerDict["TEAM"]= tmp2[0].strip()
            playerDict["POSITION"]= tmp2[1].strip()
    
    # each table is different so we over-ride this method from the base
    def _isTableHeadOfNoConcern( self, aRow ):
        out= False
        if hasattr( aRow, "class" ):
            classListOfTableRow= aRow["class"]
            for aClass in classListOfTableRow:
                if re.search( "HEAD", aClass.upper() ):
                    return True 
        else:
            return False
    
    def _isTableSubHead( self, aRow ):
        return "playerTableBgRowSubhead" in aRow["class"]
    
    def _isPlayerRow( self, aRow ):
        return "pncPlayerRow" in aRow["class"]

    def _isTableHead( self, aRow ):
        return "playerTableBgRowHead" in aRow["class"]

    def _getTableBodyFromTableList( self, tableList ):
        tableBodyList= []
        for aTable in tableList:
                if "tableBody" in aTable['class']:
                    tableBodyList.append( aTable )
                    
        return tableBodyList

class ESPN_D( ESPN_Normal ): # inherit
    
    _nameRegex= "ESPN"
    _saveCSV= "fflEspn_D.csv"
    _statColRemap= {}
    _tableColumnNames= ["DEFENSIVE", "TD RETURNS", "TOTAL" ]
    
    def __init__( self ):
        
        columnMethodOverRideList= [ ( 1, self._setRank ),\
                                    ( 2, self._parsePlayerNameData ),\
                                   ]
        siteList= [ "http://games.espn.com/ffl/tools/projections?slotCategoryId=16" ]
        
        super( ESPN_D, self ).__init__() # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList

class ESPN_K( ESPN_Normal ): # inherit
    
    _nameRegex= "ESPN"
    _saveCSV= "fflEspn_K.csv"
    _statColRemap= {}
    _tableColumnNames= [ "KICKING", "TOTAL" ]
    
    def __init__( self ):
        
        columnMethodOverRideList= [ ( 1, self._setRank ),\
                                    ( 2, self._parsePlayerNameData ),\
                                    ( 3, self._parseOverride ),\
                                    ( 4, self._parseOverride ), \
                                    ( 5, self._parseOverride ), \
                                    ( 6, self._parseOverride ), \
                                    ( 7, self._parseOverride ), \
                                   ]
        siteList= [ "http://games.espn.com/ffl/tools/projections?slotCategoryId=17" ]
        
        super( ESPN_K, self ).__init__() # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
    
    def _parseOverride( self, playerDict, aRow, aTag, rowNum, colNum, pageAddress  ):
        
        try:
            if colNum == 3:
                name= "1-39"
            elif colNum == 4:
                name= "40-49"
            elif colNum == 5:
                name= "50+"
            elif colNum == 6:
                name= "TOT"
            elif colNum == 7:
                name= "XP"
            else:
                return
            splitList= aTag.string.split("/")
            playerDict[ name + "_ATT" ]= float( splitList[0] )
            playerDict[ name + "_MADE" ]= float( splitList[0] )
            
        except:
            return
        
          
         
if __name__ == '__main__':
    oESPNList= [ ESPN_Normal(), ESPN_D(), ESPN_K() ]
    outputList= []
    for anObj in oESPNList:
        outputList += anObj.process( save2csv= True )