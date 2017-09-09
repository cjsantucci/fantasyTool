"""

Modified on Aug 18, 2017
@author: Ken

Created on Aug 16, 2017
@author: Chris 

"""
from ffl.projTableBase import ProjTableBase
from ffl import attemptFloatParse, executeClassMain

class NF_names( ProjTableBase ):
    
    _finalRemap= { "NUMBERFIRE_FP": "PROJECTED_PTS" }
    _nameRegex= "numberfire"
    _saveCSV= None
    _statColRemap= None
    _tableColumnNames= ["Player"]
    _headerFound= False
    _subHeaderFound= False
    _tableHeaderTag= "th"
    _tableSubHeaderTag= "th"

    def __init__( self, **kwargs ):
        columnMethodOverRideList= [ ( 1, self._pname ) ]
        
        super( NF_names, self ).__init__( **kwargs ) # run base constructor
        self._excludeFromProcTypeCheck= True
        self.columnMethodOverRide= columnMethodOverRideList

    def _pname( self, playerDict, aRow, aTag, rowNum, colNum, site  ):
        tList= aTag.text.strip().split("\n")
        playerDict["NAME"]= self._conditionNameStr( tList[0] )
        
        teamAndPos= tList[2].strip().replace( " ", "" )
        teamAndPos= teamAndPos.replace( "(", "" )
        teamAndPos= teamAndPos.replace( ")", "" ).split(",")
        
        if teamAndPos[0] == "D":
            playerDict["POSITION"]= self._retrCondDName( teamAndPos[0] )
            playerDict["TEAM"]= self._retrieveConditionedTeamName( " ".join( playerDict["NAME"].split()[0:-1] ) )
        elif teamAndPos[0] == "K":
            playerDict["POSITION"]= teamAndPos[0]
            if teamAndPos[1] == "LA":
                playerDict["TEAM"]= self._retrieveConditionedTeamName( "Rams" )
            else:
                playerDict["TEAM"]= self._retrieveConditionedTeamName( teamAndPos[1] )
        else:
            playerDict["POSITION"]= teamAndPos[0]
            if teamAndPos[1] == "LA":
                playerDict["TEAM"]= self._retrieveConditionedTeamName( "Rams" )
            else:
                playerDict["TEAM"]= self._retrieveConditionedTeamName( teamAndPos[1] )
        

    def _isTableHead( self, aRow, rowIdx ):
        if not self._headerFound:
            self._headerFound= True
            return True
        else:
            return False
    
    def _isTableSubHead( self, aRow, rowIdx ):
        if not self._subHeaderFound:
            self._subHeaderFound= True
            return True
        else:
            return False
            
    
    def _setTableBodyFromTableList( self, tableList ):
        for aTable in tableList:
            if "class" in aTable.attrs.keys():
                if "projection-table" in aTable["class"] and 'projection-table--fixed' in aTable["class"]:
                    self.tables= [ aTable ]
                    

    def _isnextSiteLink( self, aTag, pageAddress, nextTableList ):
        return False # do not update the list outside
    
    # each table is different so we over-ride this method from the base
    def _isTableHeadOfNoConcern( self, aRow, rowIdx ):
        return False
    
    def _isPlayerRow( self, aRow, rowIdx ):
        if "data-row-index" in aRow.attrs.keys():
            return True
        else:
            return False
    
    #"id" in aRow.attrs.keys()

class NF_QB( NF_names ): # inherit
    
    """Other positions should inherit from this"""
    
    _saveCSV= "numberFire_QB.csv"
    _statColRemap= {"Ints":"INT","Yds":"YDS","Att":"ATT","TDs":"TD"}
    _tableColumnNames= [ "numberFire", "PASSING", "RUSHING" ]
    _otherTblProcObjs= [ NF_names() ]
    
    def __init__( self, **kwargs ):
        columnMethodOverRideList= [ ( 2, self._CI ),\
                                    ( 5, self._passCompAttOverrid )
                                  ]

        siteList= ["https://www.numberfire.com/nfl/fantasy/remaining-projections/qb"]
        super( NF_QB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
        
    def _passCompAttOverrid( self, playerDict, aRow, aTag, rowNum, colNum, site  ):
        text= aTag.text.strip()
        playerDict["PASSING_CMP"]= attemptFloatParse( text.split("/")[0] )
        playerDict["PASSING_ATT"]= attemptFloatParse( text.split("/")[1] )
    
    def _CI( self, playerDict, aRow, aTag, rowNum, colNum, site  ):
        text= aTag.text.strip()
        playerDict["CI_LOWER"]= attemptFloatParse( text.split("-")[0] )
        playerDict["CI_UPPER"]= attemptFloatParse( text.split("-")[1] )
    
    def _setTableBodyFromTableList( self, tableList ):
        for aTable in tableList:
            if "class" in aTable.attrs.keys():
                if "projection-table" in aTable["class"] and 'no-fix' in aTable["class"]:
                    self.tables= [ aTable ]
                    return
    
        
    def _isTableHead( self, aRow, rowIdx ):
        thList= aRow.findAll("th")
        if len( thList ) > 0 and thList[0].text.strip() == "numberFire":
            self._headerFound= True
            return True
        else:
            return False
    
    def _isTableSubHead( self, aRow, rowIdx ):
        if self._headerFound == False:
            return
        
        thList= aRow.findAll("th")
        if len( thList ) > 0 and thList[0].attrs["title"] == 'Standard Fantasy Points':
            return True
        else:
            return False 
class NF_RB( NF_QB ): # inherit
    
    """Other positions should inherit from this"""
    
    _saveCSV= "numberFire_RB.csv"
    _statColRemap= {"Ints":"INT","Yds":"YDS","Att":"ATT","TDs":"TD"}
    _tableColumnNames= [ "numberFire", "RUSHING", "RECEIVING" ]
    _otherTblProcObjs= [ NF_names() ]
    
    def __init__( self, **kwargs ):
        columnMethodOverRideList= [ ( 2, self._CI ) ]

        siteList= ["https://www.numberfire.com/nfl/fantasy/remaining-projections/rb"]
        super( NF_RB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList

class NF_WR( NF_QB ): # inherit
    
    """Other positions should inherit from this"""
    
    _saveCSV= "numberFire_WR.csv"
    _statColRemap= {"Ints":"INT","Yds":"YDS","Att":"ATT","TDs":"TD"}
    _tableColumnNames= [ "numberFire", "RUSHING", "RECEIVING" ]
    _otherTblProcObjs= [ NF_names() ]
    
    def __init__( self, **kwargs ):
        columnMethodOverRideList= [ ( 2, self._CI ) ]

        siteList= ["https://www.numberfire.com/nfl/fantasy/remaining-projections/wr"]
        super( NF_WR, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList

class NF_TE( NF_QB ): # inherit
    
    """Other positions should inherit from this"""
    
    _saveCSV= "numberFire_TE.csv"
    _statColRemap= {"Ints":"INT","Yds":"YDS","Att":"ATT","TDs":"TD"}
    _tableColumnNames= [ "numberFire", "RUSHING", "RECEIVING" ]
    _otherTblProcObjs= [ NF_names() ]
    
    def __init__( self, **kwargs ):
        columnMethodOverRideList= [ ( 2, self._CI ) ]

        siteList= ["https://www.numberfire.com/nfl/fantasy/remaining-projections/te"]
        super( NF_TE, self ).__init__( **kwargs ) # run bexecuteClassMainase constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList

class NF_K( NF_QB ): # inherit
    
    """Other positions should inherit from this"""
    
    _saveCSV= "numberFire_K.csv"
    _statColRemap= {"XPM":"XP_MADE","FGA":"FG_ATT","FGM":"FG_MADE",\
                    "0-19":"0-19_MADE","20-29":"20-29_MADE","30-39":"30-39_MADE",\
                    "40-49":"40-49_MADE","50+":"50+_MADE"}
                
    _tableColumnNames= [ "numberFire", "Kicking", "FG Made By Distance" ]
    _otherTblProcObjs= [ NF_names() ]
    
    def __init__( self, **kwargs ):
        columnMethodOverRideList= [ ( 2, self._CI )
                                  ]

        siteList= ["https://www.numberfire.com/nfl/fantasy/remaining-projections/k"]
        super( NF_K, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList

class NF_D( NF_QB ): # inherit
    
    """Other positions should inherit from this"""
    
    _saveCSV= "numberFire_D.csv"
    _statColRemap= {"Ints":"INT","Yds":"YDS","Att":"ATT","TDs":"TD"}
    _tableColumnNames= [ "numberFire", "Defense" ]
    _otherTblProcObjs= [ NF_names() ]
    
    def __init__( self, **kwargs ):
        columnMethodOverRideList= [ ( 2, self._CI )
                                  ]

        siteList= ["https://www.numberfire.com/nfl/fantasy/remaining-projections/d"]
        super( NF_D, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
         
if __name__ == '__main__':
#     classInstancesList= [ NF_QB(), NF_RB(), NF_WR(), NF_TE(), NF_K(), NF_D() ]
#     outputList= projTableBase.executeClassMain( classInstancesList, save2csv= True )
    outputList= executeClassMain()
    