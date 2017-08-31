'''

Created on Aug 13, 2017
@author: Ken

'''
from ffl import projTableBase
from ffl.projTableBase import ProjTableBase
import re

class FPROS_QB( ProjTableBase ): # inherit
    
    _finalRemap= {"MISC_FPTS":"PROJECTED_PTS"}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_QB.csv"
    _statColRemap= {"TDS":"TD","INTS":"INT"}
    """ what to do about fumble? """
    _tableColumnNames= [ "PASSING", "RUSHING", "MISC" ]
    _tableHeaderTag= "td"
    _tableSubHeaderTag= "th"
    
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
        columnMethodOverRideList= [ ( 1, self._pname ),\
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
        
        myName= self.__class__
        # get class from my own name.
        reMatch= re.match( ".*([a-zA-Z]+)", str( myName ).split("_")[-1] )        
        
        tList= aTag.text.strip().split()

        playerDict["POSITION_RANK"]= rowNum
        l= len( tList )
        if reMatch.group() != "D":
            playerDict["NAME"]= self._conditionNameStr( " ".join( tList[0:l-1] ) )
            playerDict["TEAM"]= self._retrieveConditionedTeamName( tList[l-1] )
            playerDict["POSITION"]= reMatch.group()
        else: # 2
            playerDict["TEAM"]= self._retrieveConditionedTeamName( " ".join( tList ) )
            playerDict["POSITION"]= "DST"
        
        

    
    
    # each table is different so we over-ride this method from the base
    def _isTableHeadOfNoConcern( self, aRow, rowIdx ):
        return False
    
    def _isTableHead( self, aRow, rowIdx ):
        
        if rowIdx == 0:
            return True
        else:
            return False
    
    def _isTableSubHead( self, aRow, rowIdx ):
        
        if rowIdx == 1:
            return True
        else:
            return False
    
    def _isPlayerRow( self, aRow, rowIdx ):
        if rowIdx > 1:
            return True
        else:
            return False
    
    #"id" in aRow.attrs.keys()

    def _setTableBodyFromTableList( self, tableList ):
        self.tables= [ tableList[0]  ]
                    
                    
class FPROS_RB( FPROS_QB ): # inherit
    
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_RB.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC", "TDS":"TD"}
    _tableColumnNames= [ "RUSHING", "RECEIVING", "Fantasy", "MISC" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/rb.php?week=draft" ]
        
        super( FPROS_RB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FPROS_WR( FPROS_QB ): # inherit
    
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_WR.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC", "TDS":"TD"}
    _tableColumnNames= [ "RECEIVING", "RUSHING", "Fantasy", "MISC" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/wr.php?week=draft" ]
        
        super( FPROS_WR, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FPROS_TE( FPROS_QB ): # inherit
    
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_TE.csv"
    _statColRemap= {"Att":"ATT","Yard":"YDS","Rec":"REC", "TDS":"TD"}
    _tableColumnNames= [ "RECEIVING", "Fantasy", "MISC" ]
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/te.php?week=draft" ]
        
        super( FPROS_TE, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class FPROS_K( FPROS_QB ): # inherit
    
    _finalRemap= {}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_K.csv"
    _statColRemap= {"FG":"FG","FGA":"FGA","XPT":"XPT","FPTS":"PROJECTED_PTS",}
    _tableColumnNames= None
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/k.php?week=draft" ]
        
        super( FPROS_K, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        
    def _isTableHead( self, aRow, rowIdx ):
        return False

    def _isTableSubHead( self, aRow, rowIdx ):
        if rowIdx == 0:
            return True
        else:
            return False
    
    def _isPlayerRow( self, aRow, rowIdx ):
        if rowIdx > 0:
            return True
        else:
            return False

class FPROS_D( FPROS_K ): # inherit
    
    _finalRemap= {}
    _nameRegex= "FantasyPROs"
    _saveCSV= "fflFPROS_D.csv"
    _statColRemap= {"SACK":"SACK","INT":"INT","FR":"FR", \
                    "TD":"TD","ASSIST":"ASSIST","SAFETY":"SAFETY", \
                    "PA":"PA","YDS AGN":"YDS AGN", "FPTS":"PROJECTED_PTS"}
    _tableColumnNames= None
    
    def __init__( self, **kwargs ):
        
        siteList= [ "https://www.fantasypros.com/nfl/projections/dst.php?week=draft" ]
        
        super( FPROS_D, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
         
if __name__ == '__main__':
#     classInstancesList= [ FPROS_QB(), FPROS_RB(), FPROS_WR(), FPROS_TE(), FPROS_K(), FPROS_D() ]
#     outputList= projTableBase.executeClassMain( classInstancesList, save2csv= True )
    outputList= projTableBase.executeClassMain()
    