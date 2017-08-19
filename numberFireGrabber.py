"""
Created on Aug 16, 2017
@author: Chris 

"""
from ffl.projTableBase import ProjTableBase

class NFG_names( ProjTableBase ):
    
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
        
#         siteList= [ "https://www.numberfire.com/nfl/fantasy/remaining-projections/qb" ]
        super( NFG_names, self ).__init__( **kwargs ) # run base constructor
        self.columnMethodOverRide= columnMethodOverRideList

    def _pname( self, playerDict, aRow, aTag, rowNum, colNum, site  ):
        tList= aTag.text.strip().split("\n")
        playerDict["PLAYER"]= tList[0]
        
        teamAndPos= tList[2].strip().replace( " ", "" )
        teamAndPos= teamAndPos.replace( "(", "" )
        teamAndPos= teamAndPos.replace( ")", "" ).split(",")
        playerDict["POSITION"]= teamAndPos[0]
        playerDict["TEAM"]= teamAndPos[1]

    def _isTableHead( self, aRow ):
        if not self._headerFound:
            self._headerFound= True
            return True
        else:
            return False
    
    def _isTableSubHead( self, aRow ):
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
                    return
                    

    def _isnextSiteLink( self, aTag, pageAddress, nextTableList ):
        return False # do not update the list outside
    
    # each table is different so we over-ride this method from the base
    def _isTableHeadOfNoConcern( self, aRow ):
        return False
    
    def _isPlayerRow( self, aRow ):
        if "data-row-index" in aRow.attrs.keys():
            return True
        else:
            return False
    
    #"id" in aRow.attrs.keys()

class NFG_QB( NFG_names ): # inherit
    
    """Other positions should inherit from this"""
    
    _saveCSV= "numberFire.csv"
    _statColRemap= {"Ints":"INT","Yds":"YDS","Att":"ATT","TDs":"TD"}
    _tableColumnNames= [ "numberFire", "PASSING", "RUSHING" ]
    _otherTblProcObjs= [ NFG_names() ]
    
    def __init__( self, **kwargs ):
        columnMethodOverRideList= [ ( 2, self._CI ),\
                                    ( 5, self._CA )
                                  ]

        siteList= ["https://www.numberfire.com/nfl/fantasy/remaining-projections/qb"]
        super( NFG_QB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
        
    def _CA( self, playerDict, aRow, aTag, rowNum, colNum, site  ):
        text= aTag.text.strip()
        playerDict["PASSING_CMP"]= projTableBase.attemptFloatParse( text.split("/")[0] )
        playerDict["PASSING_ATT"]= projTableBase.attemptFloatParse( text.split("/")[1] )
    
    def _CI( self, playerDict, aRow, aTag, rowNum, colNum, site  ):
        text= aTag.text.strip()
        playerDict["CI_LOWER"]= projTableBase.attemptFloatParse( text.split("-")[0] )
        playerDict["CI_UPPER"]= projTableBase.attemptFloatParse( text.split("-")[1] )
    
    def _setTableBodyFromTableList( self, tableList ):
        for aTable in tableList:
            if "class" in aTable.attrs.keys():
                if "projection-table" in aTable["class"] and 'no-fix' in aTable["class"]:
                    self.tables= [ aTable ]
                    return
    
        
    def _isTableHead( self, aRow ):
        thList= aRow.findAll("th")
        if len( thList ) > 0 and thList[0].text.strip() == "numberFire":
            self._headerFound= True
            return True
        else:
            return False
    
    def _isTableSubHead( self, aRow ):
        if self._headerFound == False:
            return
        
        thList= aRow.findAll("th")
        if len( thList ) > 0 and thList[0].attrs["title"] == 'Standard Fantasy Points':
            return True
        else:
            return False 
         
if __name__ == '__main__':
    oNFList= [ NFG_QB() ]
    outputList= []
    for anObj in oNFList:
        outputList += anObj.process( save2csv= True )
    