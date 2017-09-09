'''

Created on Aug 5, 2017
@author: Ken

Created on Aug 7, 2017
@author: Ken

'''

from ffl import executeClassMain
from ffl.projTableBase import ProjTableBase
import re

class _QB( ProjTableBase ): # inherit
    
    _finalRemap= {}
    _nameRegex= ""
    _saveCSV= "_QB.csv"
    _statColRemap= {}
    _tableColumnNames= []
    _tableHeaderTag= "td"
    _tableSubHeaderTag= "td"
    
    def __init__( self, **kwargs ):
    
        siteList= []
        columnMethodOverRideList= []
        
        super( _QB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
    
    def _isnextSiteLink( self, aTag, pageAddress, nextLinkList ):
                    
        return False # do not update the list outside
    
    def _pname( self, playerDict, aRow, aTag, rowNum, colNum, pageAddress ):
        pass
    
    def _pteam( self, playerDict, aRow, aTag, rowNum, colNum, pageAddress ):
        pass
    
    def _isTableHeadOfNoConcern( self, aRow, rowIdx ):
        return False
    
    def _isTableHead( self, aRow, rowIdx ):
        return False
        
    
    def _isTableSubHead( self, aRow, rowIdx ):
        return False
    
    def _isPlayerRow( self, aRow, rowIdx ):
        return False 
    
    def _setTableBodyFromTableList( self, tableList ):
        self.tables= []

class _RB( _QB ): # inherit
    
    _nameRegex= ""
    _saveCSV= "_RB.csv"
    _statColRemap= {}
    _tableColumnNames= []
    
    def __init__( self, **kwargs ):
        
        siteList= [ "" ]
        
        super( _RB, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class _WR( _QB ): # inherit
    
    _nameRegex= ""
    _saveCSV= "_WR.csv"
    _tableColumnNames= []
    
    def __init__( self, **kwargs ):
        
        siteList= []
        
        super( _WR, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class _TE( _QB ): # inherit
    
    _nameRegex= ""
    _saveCSV= "_TE.csv"
    _tableColumnNames= []
    
    def __init__( self, **kwargs ):
        
        siteList= []
        
        super( _TE, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
    
class _K( _QB ): # inherit
    
    _nameRegex= ""
    _saveCSV= "_K.csv"
    _tableColumnNames= None
    
    def __init__( self, **kwargs ):
        
        siteList= []
        
        super( _K, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList

class FFTODAY_D( _K ): # inherit
    
    _nameRegex= ""
    _saveCSV= "_D.csv"
    _tableColumnNames= None
    
    def __init__( self, **kwargs ):
        
        columnMethodOverRideList= []
        siteList= []
        
        super( FFTODAY_D, self ).__init__( **kwargs ) # run base constructor
        self.sites= siteList
        self.columnMethodOverRide= columnMethodOverRideList
         
if __name__ == '__main__':
#     classInstancesList= [ FFTODAY_D(), FFTODAY_K(), FFTODAY_QB(), FFTODAY_RB(), FFTODAY_TE(), FFTODAY_WR()  ]
#     outputList= projTableBase.executeClassMain( classInstancesList, save2csv= True )
    outputList= executeClassMain()
    