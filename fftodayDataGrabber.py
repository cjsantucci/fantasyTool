'''

Created on Aug 5, 2017
@author: Ken

Created on Aug 7, 2017
@author: Ken

'''

import projTableBase
from projTableBase import ProjTableBase
import re

class FFTODAY_QB( ProjTableBase ): # inherit
    
    _finalRemap= {"FPts":"PROJECTED_PTS"}
    _nameRegex= "FFTODAY"
    _saveCSV= "fflFFTODAY_QB.csv"
    _statColRemap= {"Att":"ATT","Comp":"CMP","Yard":"YDS"}
    _tableColumnNames= [ "PASSING", "RUSHING", "Fantasy" ]
    _tableHeaderTag= "td"
    _tableSubHeaderTag= "td"
    
    def __init__( self, **kwargs ):
        """
        typical constructor for the child classes -- this is really here so the comment
        below won't show up in the docs for this class
        """
        
        """ Had to use this strange long version of this link.
        When parsing the "Next Page link it only gives stuff after the "?" in the link
        So in order to navigate to the next page I had to use this link to throw them together.
        look at the _isnextSiteLink method to see what I was saying
        """
        siteList= [ "http://fftoday.com/rankings/playerproj.php?Season=2017&PosID=10&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=0" ]
        columnMethodOverRideList= [ ( 2, self._pname ),\
                                    ( 3, self._pteam )
                                   ]
        
        super( FFTODAY_QB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
    
    def _isnextSiteLink( self, aTag, pageAddress, nextLinkList ):
        tagStr= aTag.text.strip()
        if re.search( "Next Page", tagStr ):
            newLink= pageAddress.split("?")[0] + aTag[ "href" ]
            nextLinkList.append( newLink )
            
        return False # do not update the list outside
    
    def _pname( self, playerDict, aRow, aTag, rowNum, colNum, pageAddress ):
        playerDict["NAME"]= aTag.text.strip()
        playerDict["POSITION_RANK"]= rowNum
        
        myName= self.__class__
        # get class from my own name.
        reMatch= re.match( ".*([a-zA-Z]+)", str( myName ).split("_")[-1] )
        playerDict["POSITION"]= reMatch.group()
    
    def _pteam( self, playerDict, aRow, aTag, rowNum, colNum, pageAddress ):
        playerDict["TEAM"]= aTag.text.strip()
    
    # each table is different so we over-ride this method from the base
    def _isTableHeadOfNoConcern( self, aRow ):
        return False
    
    def _isTableHead( self, aRow ):
        
        if "class" in aRow.attrs.keys() and re.search( "tablehdr", aRow.attrs["class"][0] ):
            return True
        else:
            return False
    
        
    
    def _isTableSubHead( self, aRow ):
        
        if "class" in aRow.attrs.keys() and re.search( "tableclmhdr", aRow.attrs["class"][0] ):
            return True
        else:
            return False
    
    def _isPlayerRow( self, aRow ):
        tdList= aRow.findAll( "td" )
        if len( tdList ) >0 and \
            "class" in tdList[0].attrs.keys() and \
            re.search( "sort1", tdList[0].attrs["class"][0] ):
            
            return True
        
        else:
            return False
    
    #"id" in aRow.attrs.keys()

    def _setTableBodyFromTableList( self, tableList ):
        tableBodyList= []
        for aTable in tableList:
            tableRows= aTable.findAll("tr")
            for aRow in tableRows:
                if len( aRow.attrs ) > 0 and "class" in aRow.attrs.keys() and re.search( "tablehdr", aRow.attrs["class"][0] ):
                    tableBodyList.append( aTable )
                    self.tables= tableBodyList
                    return
                    

    
class FFTODAY_RB( FFTODAY_QB ): # inherit
    
    _finalRemap= {"FPts":"PROJECTED_PTS"}
    _nameRegex= "FFTODAY"
    _saveCSV= "fflFFTODAY_RB.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC"}
    _tableColumnNames= [ "RUSHING", "RECEIVING", "Fantasy" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "http://fftoday.com/rankings/playerproj.php?Season=2017&PosID=20&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=0" ]
        
        super( FFTODAY_RB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FFTODAY_WR( FFTODAY_QB ): # inherit
    
    _finalRemap= {"FPts":"PROJECTED_PTS"}
    _nameRegex= "FFTODAY"
    _saveCSV= "fflFFTODAY_WR.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC"}
    _tableColumnNames= [ "RECEIVING", "RUSHING", "Fantasy" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "http://fftoday.com/rankings/playerproj.php?Season=2017&PosID=30&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=0" ]
        
        super( FFTODAY_WR, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FFTODAY_TE( FFTODAY_QB ): # inherit
    
    _finalRemap= {"FPts":"PROJECTED_PTS"}
    _nameRegex= "FFTODAY"
    _saveCSV= "fflFFTODAY_TE.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC"}
    _tableColumnNames= [ "RECEIVING", "Fantasy" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "http://fftoday.com/rankings/playerproj.php?Season=2017&PosID=40&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=0" ]
        
        super( FFTODAY_TE, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FFTODAY_K( FFTODAY_QB ): # inherit
    
    _finalRemap= {"FPTS":"PROJECTED_PTS"}
    _nameRegex= "CBS"
    _saveCSV= "fflFFTODAY_K.csv"
    _statColRemap= {"YD":"YDS","RECPT":"REC" }
    _tableColumnNames= None
    
    def __init__( self, **kwargs ):
        
        siteList= [ "http://fftoday.com/rankings/playerproj.php?Season=2017&PosID=80&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=0" ]
        
        super( FFTODAY_K, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList

class FFTODAY_D( FFTODAY_QB ): # inherit
    
    _finalRemap= {"FPTS":"PROJECTED_PTS"}
    _nameRegex= "CBS"
    _saveCSV= "fflFFTODAY_D.csv"
    _statColRemap= {"YD":"YDS","RECPT":"REC" }
    _tableColumnNames= None
    
    def __init__( self, **kwargs ):
        
        siteList= [ "http://fftoday.com/rankings/playerproj.php?Season=2017&PosID=99&LeagueID=1&order_by=FFPts&sort_order=DESC&cur_page=0" ]
        
        super( FFTODAY_D, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
         
if __name__ == '__main__':
    oFFTodayList= [ FFTODAY_QB(), FFTODAY_RB(), FFTODAY_WR(), FFTODAY_TE(), FFTODAY_K(), FFTODAY_D() ]
    outputList= []
    for anObj in oFFTodayList:
        outputList += anObj.process( save2csv= True )
    