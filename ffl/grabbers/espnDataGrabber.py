'''
Created on Aug 27, 2016

@author: chris
'''

from ffl import attemptFloatParse, executeClassMain
from ffl.projTableBase import ProjTableBase
import re
    
class ESPN_Normal( ProjTableBase ): # inherit
    
    _finalRemap= {"TOTAL_PTS":"PROJECTED_PTS"}
    _nameRegex= "ESPN"
    _saveCSV= "fflEspnNormal.csv"
    _statColRemap= {"RUSH":"ATT"}
    _tableColumnNames= [ "PASSING","RECEIVING", "RUSHING", "TOTAL" ]
    _tableHeaderTag= "th"
    _tableSubHeaderTag= "td"
    
    def __init__( self, **kwargs ):
        
        columnMethodOverRideList= [ ( 1, self._setRank ),\
                                    ( 2, self._parsePlayerNameData ),\
                                    ( 3, self._passCompAttOverrid ), \
                                   ]
        siteList= [ ( "http://games.espn.com/ffl/tools/projections?slotCategoryId=0", "QB" ),\
                    ( "http://games.espn.com/ffl/tools/projections?slotCategoryId=2", "RB" ),\
                    ( "http://games.espn.com/ffl/tools/projections?slotCategoryId=4", "WR" ),\
                    ( "http://games.espn.com/ffl/tools/projections?slotCategoryId=6", "TE" ),\
                     ]
        
        super( ESPN_Normal, self ).__init__( **kwargs ) # run base constructor
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
        playerDict["POSITION_RANK"]= attemptFloatParse( aTag.text )
    
    def _parsePlayerNameData( self, playerDict, aRow, aTag, rowNum, colNum, pageAddress ):
        playerLink= aTag.contents
        playerDict["SEASONID"]= int( playerLink[0]["seasonid"] )
        if re.search( "D/ST", aTag.text ):
            playerDict["POSITION"] = "DST"
            tmp= aTag.text.split(" ")
            playerDict["TEAM"]= self._retrieveConditionedTeamName( tmp[0] )
        else:
            tmp= aTag.text.split(",")
            playerDict["NAME"]= self._conditionNameStr( tmp[0].strip() )
            if len( tmp ) < 2:
                print()
            tmp2= tmp[1].split('\xa0')
            playerDict["TEAM"]= self._retrieveConditionedTeamName( tmp2[0].strip() )
            playerDict["POSITION"]= tmp2[1].strip()
    
    # each table is different so we over-ride this method from the base
    def _isTableHeadOfNoConcern( self, aRow, rowIdx ):
        return False
    
    def _isTableSubHead( self, aRow, rowIdx ):
        return "playerTableBgRowSubhead" in aRow["class"]
    
    def _isPlayerRow( self, aRow, rowIdx ):
        return "pncPlayerRow" in aRow["class"]

    def _isTableHead( self, aRow, rowIdx ):
        return "playerTableBgRowHead" in aRow["class"]

    def _setTableBodyFromTableList( self, tableList ):
        tableBodyList= []
        for aTable in tableList:
                if "tableBody" in aTable['class']:
                    tableBodyList.append( aTable )
                    self.tables= tableBodyList
                    return

class ESPN_D( ESPN_Normal ): # inherit
    
    _nameRegex= "ESPN"
    _saveCSV= "fflEspn_D.csv"
    _statColRemap= {}
    _tableColumnNames= ["DEFENSIVE", "TD RETURNS", "TOTAL" ]
    
    def __init__( self, **kwargs  ):
        
        columnMethodOverRideList= [ ( 1, self._setRank ),\
                                    ( 2, self._parsePlayerNameData ),\
                                   ]
        siteList= [ "http://games.espn.com/ffl/tools/projections?slotCategoryId=16" ]
        
        super( ESPN_D, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList

class ESPN_K( ESPN_Normal ): # inherit
    
    _nameRegex= "ESPN"
    _saveCSV= "fflEspn_K.csv"
    _statColRemap= {}
    _tableColumnNames= [ "KICKING", "TOTAL" ]
    
    def __init__( self, **kwargs ):
        
        columnMethodOverRideList= [ ( 1, self._setRank ),\
                                    ( 2, self._parsePlayerNameData ),\
                                    ( 3, self._parseOverride ),\
                                    ( 4, self._parseOverride ), \
                                    ( 5, self._parseOverride ), \
                                    ( 6, self._parseOverride ), \
                                    ( 7, self._parseOverride ), \
                                   ]
        siteList= [ "http://games.espn.com/ffl/tools/projections?slotCategoryId=17" ]
        
        super( ESPN_K, self ).__init__( **kwargs ) # run base constructor
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
#     classInstancesList= [ ESPN_Normal(), ESPN_D(), ESPN_K() ]
#     outputList= projTableBase.executeClassMain( classInstancesList, save2csv= True )
    outputList= executeClassMain()
    