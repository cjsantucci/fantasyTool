'''
Created on Aug 27, 2016

@author: chris
'''
from ffl import projTableBase
from ffl.projTableBase import ProjTableBase
import re
    
class CBS_Normal( ProjTableBase ): # inherit
    
    _finalRemap= {"MISC_FPTS":"PROJECTED_PTS"}
    _nameRegex= "CBS"
    _saveCSV= "fflCBS.csv"
    _statColRemap= {"YD":"YDS","RECPT":"REC" }
    _tableColumnNames= [ "PASSING","RECEIVING", "RUSHING", "MISC" ]
    
    def __init__( self ):
        
        siteList= ["https://www.cbssports.com/fantasy/football/stats/sortable/points/QB/standard/projections/2017/ytd?&print_rows=9999",\
                   "https://www.cbssports.com/fantasy/football/stats/sortable/points/RB/standard/projections/2017/ytd?&print_rows=9999",\
                   "https://www.cbssports.com/fantasy/football/stats/sortable/points/WR/standard/projections/2017/ytd?&print_rows=9999",\
                   "https://www.cbssports.com/fantasy/football/stats/sortable/points/TE/standard/projections/2017/ytd?&print_rows=9999",\
                  ]
        columnMethodOverRideList= [ ( 1, self._nameAndTeam ),\
                                   ]
        
        super( CBS_Normal, self ).__init__() # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
    
    def _isnextSiteLink( self, aTag, pageAddress, nextTableList ):
        tagStr= aTag.text.strip()
        return re.search( "NEXT", tagStr ) or re.search( "Next Page", tagStr )
    
    def _nameAndTeam( self, playerDict, aRow, aTag, rowNum, colNum, pageAddress ):
        tsplit= aTag.text.split(",")
        playerDict["NAME"]= tsplit[0]
        playerDict["TEAM"]= tsplit[1]
        playerDict["POSITION_RANK"]= rowNum
        
        checkListPositions= [ "points/QB", "points/RB", "points/WR", "points/TE", "points/K", "points/DST"  ]
        for aPosition in checkListPositions:
            if re.search( aPosition, pageAddress ):
                tSplit= aPosition.split("/")
                playerDict["POSITION"]= tSplit[1]
    
    # each table is different so we over-ride this method from the base
    def _isTableHeadOfNoConcern( self, aRow ):
        out= False
        if hasattr( aRow, "class" ):
            classListOfTableRow= aRow["class"]
            for aClass in classListOfTableRow:
                if re.search( "HEAD", aClass.upper() ) or \
                    re.search( "TITLE", aClass.upper() ) :
                    return True 
        else:
            return False
    
    def _isTableHead( self, aRow ):
        outBool = aRow["class"] == ["row1"] and \
             "id" in aRow.attrs.keys() and aRow["id"] == "special"
    
        return outBool
    
    def _isTableSubHead( self, aRow ):
        return aRow["class"] == ["label"]
    
    def _isPlayerRow( self, aRow ):
        return re.search( 'row[0-9]*', aRow["class"][0] )
    
    #"id" in aRow.attrs.keys()

    def _getTableBodyFromTableList( self, tableList ):
        return tableList.copy()
    
class CBS_K( CBS_Normal ): # inherit
    
    _finalRemap= {"FPTS":"PROJECTED_PTS"}
    _nameRegex= "CBS"
    _saveCSV= "fflCBS_K.csv"
    _statColRemap= {"YD":"YDS","RECPT":"REC" }
    _tableColumnNames= None
    
    def __init__( self ):
        
        siteList= [ "https://www.cbssports.com/fantasy/football/stats/sortable/points/K/standard/projections/2017/ytd" ]
        
        super( CBS_K, self ).__init__() # run base constructor
        self.sites= siteList

class CBS_D( CBS_Normal ): # inherit
    
    _finalRemap= {"FPTS":"PROJECTED_PTS"}
    _nameRegex= "CBS"
    _saveCSV= "fflCBS_D.csv"
    _statColRemap= {"YD":"YDS","RECPT":"REC" }
    _tableColumnNames= None
    
    def __init__( self ):
        
        siteList= [ "https://www.cbssports.com/fantasy/football/stats/sortable/points/DST/standard/projections/2017/ytd" ]
        
        super( CBS_D, self ).__init__() # run base constructor
        self.sites= siteList

if __name__ == '__main__':
    oCBSList= [ CBS_Normal(), CBS_D(), CBS_K() ]
    outputList= []
    for anObj in oCBSList:
        outputList += anObj.process( save2csv= True )
    