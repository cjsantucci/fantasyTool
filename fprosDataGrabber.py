'''

Created on Aug 13, 2017
@author: Ken

'''

import projTableBase
from projTableBase import ProjTableBase
import re

class FPROS_QB( ProjTableBase ): # inherit
    
    _finalRemap= {"FPTS":"PROJECTED_PTS"}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_QB.csv"
    _statColRemap= {"TDS":"TD","INTS":"INT"}
    """ what to do about fumble? """
    _tableColumnNames= [ "PASSING", "RUSHING", "MISC" ]
    
    def __init__( self, **kwargs ):
        """
        typical constructor for the child classes -- this is really here so the comment
        below won't show up in the docs for this class
        """
        
        """ Had to use this strange long version of this link.
        When parsing the "Next Page link it only gives stuff after the "?" in the link
        So in order to navigate to the next page I had to use this link to throw them together.
        look at the _isnextSiteLink method to see what I was saying
        
        not sure if fantasy pros needs this... keeping for now
        """
        siteList= [ "https://www.fantasypros.com/nfl/projections/qb.php?week=draft" ]
        columnMethodOverRideList= [ ( 2, self._pname ),\
                                    ( 3, self._pteam )
                                   ]
        
        super( FPROS_QB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
    
    def _isnextSiteLink( self, aTag, pageAddress, nextTableList ):
        tagStr= aTag.text.strip()
        if re.search( "Next Page", tagStr ):
            newLink= pageAddress.split("?")[0] + aTag[ "href" ]
            nextTableList.append( newLink )
            
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

    def _getTableBodyFromTableList( self, tableList ):
        tableBodyList= []
        for aTable in tableList:
            tableRows= aTable.findAll("tr")
            for aRow in tableRows:
                if len( aRow.attrs ) > 0 and "class" in aRow.attrs.keys() and re.search( "tablehdr", aRow.attrs["class"][0] ):
                    tableBodyList.append( aTable )
                    return tableBodyList
                    
                    """ Ken here are some notes for you. Python does some fancy things. For instance, it allows what is called subscripting.
                    In this case When you subscript the object aRow (which is not really a row it's just a tag, but it's a row in many cases for tables it appears)
                    All it does is accesses the property "attrs" of the object which is actually a dictionary.
                    
                    --aRow.attrs["class"] is the same as aRow["class"] because the object was designed this way for convenience.
                    
                        >>> type(aRow)
                        <class 'bs4.element.Tag'>    
                    
                        >>> type( aRow.attrs )
                        <class 'dict'>
                    
                    The proper way to check if a field is in a dictionary is to check the keys()--see above
                    
                    Since the type of aRow["class"] is a list as seen below we must grab the zeroth element to get the string
                        >>> type( aRow.attrs["class"] )
                        <class 'list'>
                    
                    """
    
class FPROS_RB( FPROS_QB ): # inherit
    
    _finalRemap= {"FPts":"PROJECTED_PTS"}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_RB.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC"}
    _tableColumnNames= [ "RUSHING", "RECEIVING", "Fantasy" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/rb.php?week=draft" ]
        
        super( FPROS_RB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FPROS_WR( FPROS_QB ): # inherit
    
    _finalRemap= {"FPts":"PROJECTED_PTS"}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_WR.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC"}
    _tableColumnNames= [ "RECEIVING", "RUSHING", "Fantasy" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/wr.php?week=draft" ]
        
        super( FPROS_WR, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FPROS_TE( FPROS_QB ): # inherit
    
    _finalRemap= {"FPts":"PROJECTED_PTS"}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_TE.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC"}
    _tableColumnNames= [ "RECEIVING", "Fantasy" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/te.php?week=draft" ]
        
        super( FPROS_TE, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FPROS_K( FPROS_QB ): # inherit
    
    _finalRemap= {"FPTS":"PROJECTED_PTS"}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_K.csv"
    _statColRemap= {"YD":"YDS","RECPT":"REC" }
    _tableColumnNames= None
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/k.php?week=draft" ]
        
        super( FPROS_K, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList

class FPROS_D( FPROS_QB ): # inherit
    
    _finalRemap= {"FPTS":"PROJECTED_PTS"}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_D.csv"
    _statColRemap= {"YD":"YDS","RECPT":"REC" }
    _tableColumnNames= None
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/dst.php?week=draft" ]
        
        super( FPROS_D, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
         
if __name__ == '__main__':
    oFantasyPROsList= [ FPROS_QB(), FPROS_RB(), FPROS_WR(), FPROS_TE() ] #, FPROS_K(), FPROS_D() ]
    outputList= []
    for anObj in oFantasyPROsList:
        outputList += anObj.process( save2csv= True )
    