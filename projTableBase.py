'''
Created on Jul 30, 2017

@author: chris
'''

from abc import abstractmethod, abstractproperty, ABCMeta
from bs4 import BeautifulSoup as bs
import datetime
from ffl.tableColumnCorrelate import *
import getpass
import numpy as np
import os
import pandas as pd
import re
import requests as rq
import warnings

class ProjTableBase( object, metaclass= ABCMeta ):
    """
    
    This is the base class for the table readers
    
    """
    _finalRemap= {}
    _maxDepth= 50
    _topList= list()
    _year= datetime.datetime.now().year
    _oCol= None
    columnMethodOverRide= None
    _cols2override= None
    _colOverrideMethodIdx= 1
    _saveLocation = None
    _otherTblProcObjs= None
    _multiTableJoinMethod= "rowbyrow"
    _user= getpass.getuser()
    _tables= None

    def __init__( self, **kwargs  ):
        """
        Set stuff up for when "process" method is called for all classes
        """
        
        if self._user == "chris":
            self._saveLocation= "/home/chris/Desktop/fflOutput"
        elif self._user == "Ken":
            """ Ken only change this path if you want to save elsewhere"""
            self._saveLocation= "/Users/Ken/Documents/PYTHON/fantasyFootball_v2"
            
        
        if self._saveCSV is not None:
            self._addYear2SaveCSV()
            if not re.search( "/" , self._saveCSV ): # unless a specific path in the child class use the path above
                self._saveCSV= os.path.join( self._saveLocation, self._saveCSV )
        
        self._oCol= ColumnCorrelate( self._nameRegex, self._tableColumnNames, self._statColRemap, self._tableHeaderTag, self._tableSubHeaderTag ) # data object which stores object to data correlation
        
    def process( self, save2csv= False ):
        """ runs loop around main function which processes each page
        Sites like CBS have the position pages broken out separate 
        so for that subclass we process each position via an individual web page
        and we will process it in a loop in here
        """
        assert self.sites is not None, "must define sites prior to calling super constructor"
        
        outputList= []
        for siteIdx , aSite in enumerate( self._sites ):
            _, levelDownRecurse= self._processPage( self._sites[siteIdx], siteIdx, len( self._sites ), outputList, 0 ) # recursive
            
        
        if save2csv:
            fflData= pd.DataFrame( outputList )
            print( "Saving to " + self._saveCSV )
            fflData.to_csv( self._saveCSV )
        
        return outputList

    def _addYear2SaveCSV( self ):
        """manipulate csv string to include year"""
        splList= self._saveCSV.split(".")
        self._saveCSV= ".".join( splList[0:-1] ) + "_" + str( self._year ) + "." + "".join( splList[-1:] ) 
    
    def _getAllNextPlayerPages( self, doc, pageAddress ):
        hyperList= doc.findAll('a')

        nextLinkList= list()
        for aTag in hyperList:
            """Pass the table list and leave it up to the child class
            whether or not they want to modify the list directly....
            it could be slightly more complicated
            """
            if self._isnextSiteLink( aTag, pageAddress, nextLinkList ):
                if aTag[ "href" ] not in nextLinkList: # leave this on this line...protect child class from returning TRUE and modifying the list
                    nextLinkList.append( aTag["href"] )
                
        return nextLinkList
    
    def _processPage( self, pageAddress, siteIdx, numSites, topList, levelDownRecurse ):
        """Main processing function"""
        
        levelDownRecurse += 1
        print( self._nameRegex + ", " + str(siteIdx+1) + " of " + str(numSites) + " links complete, "+ "level_down: " + str(levelDownRecurse) )
        
        
        """get tables"""
        session= rq.session()
        req= session.get( pageAddress )
        if req.ok:
            doc= bs( req.content, 'lxml' )
        else:
            assert False, "not ok"
        
        
        if self._otherTblProcObjs is not None:
            obj2ProcessList= [ self ] + self._otherTblProcObjs
        else:
            obj2ProcessList= [ self ]
            
        tmpTableList= doc.findAll( 'table' )
        
        """ set tables"""
        tPlayerListsForObjs= []
        for anObj2Process in obj2ProcessList:
            anObj2Process._setTableBodyFromTableList( tmpTableList )
            assert len( anObj2Process.tables ) == 1, "for now each object is only set up for 1 table."
            tPlayerListsForObjs.append( anObj2Process._processTable( pageAddress ) )
        
        topList += self._joinTableEntries( tPlayerListsForObjs )
        
        nextTableList= self._getAllNextPlayerPages( doc, pageAddress )
        if len( nextTableList ) > 0 and levelDownRecurse <= self._maxDepth:
            _, levelDownRecurse= self._processPage( nextTableList[0], siteIdx, numSites, topList, levelDownRecurse )
        
        return topList, levelDownRecurse
    # en processPage
    
    def _joinTableEntries( self, playerListsForObjs ): 
    
        outList= []
        
        if self._otherTblProcObjs is None:
            outList= playerListsForObjs[0]
        elif self._multiTableJoinMethod == "rowbyrow":
            
            checkLen= len( playerListsForObjs[0] )
            for playerListIdx, aListOfPlayers in enumerate( playerListsForObjs ):
                assert len( aListOfPlayers ) == checkLen, "length mismatch for list: " + str( playerListIdx )
            
            """ before it was a M object by N player list of dictionaries"""
            """ now it will be N player by M Object list of dictionairies"""
            listOfTuples= list( zip( *playerListsForObjs ) )
            
            for playerListIdx, aListOfDicts in enumerate( listOfTuples ):
                for dictIdx, aDict in enumerate( aListOfDicts ):
                    if dictIdx == 0:
                        tDict= aDict
                    else:
                        tDict.update( aDict )
                outList.append( tDict )
                
        else:
            assert False, "only one method currently implemented for table joining--must have same number of rows"
        
        return outList
    
    def _processTable( self, pageAddress ):
        """Process rows"""
        playerRows= self.tables[0].findAll("tr")
        playerRow = 0
        siteListPlayers= []
        for aRow in playerRows :
            if self._isTableHeadOfNoConcern( aRow ):
                pass
            elif self._isTableHead( aRow ):
                self._oCol._mapCategory2ColumnNums( aRow )
            elif self._isTableSubHead( aRow ):
                self._oCol._mapColumns2Category( aRow )
            elif self._isPlayerRow( aRow ):
                playerRow += 1
                playerDict= self.parseTableRowTag( aRow, playerRow, pageAddress )
                playerDict["WEBSITE"]= pageAddress
                playerDict["SITE_REGEX"]= self._nameRegex
                siteListPlayers.append( playerDict )
            else:
                pass
        
        """ Remap all of the fields if necessary"""
        for aPlayerDict in siteListPlayers:
            for aKey in self._finalRemap.keys():
                if aKey in aPlayerDict:
                    aPlayerDict[ self._finalRemap[ aKey ] ]= aPlayerDict[ aKey ]
                    del aPlayerDict[ aKey ]
                    
        return siteListPlayers
    
    def parseTableRowTag( self, aRow, playerRow, pageAddress ):
        tagDataList= aRow.findAll( 'td' ) 
        playerDict = dict()
        
        colCount= 0;
        for aTag in tagDataList:
            colCount+=1
            if self._cols2override is not None and colCount in self._cols2override:
                idx= [ idx for idx, anOverride in enumerate( self._cols2override ) if self._cols2override[ idx ]==colCount ]
                dynMethod= self._columnMethodOverRide[ idx[0] ][ self._colOverrideMethodIdx ]
                dynMethod( playerDict, aRow, aTag, playerRow, colCount, pageAddress  )
                
            #elif "playertableStat" in aTag["class"]:
            elif colCount in self._oCol.col2ColumnCategory.keys():
                if colCount in self._oCol.columnCategoryToColumnNumber["allcols_found"]:
                    categoryWord= self._oCol.col2ColumnCategory[ colCount ]
                    colName= self._oCol.col2ColumnName[ colCount ]
                    
                    saveKey= colName
                    if saveKey in self._statColRemap.keys():
                        saveKey= self._statColRemap[ colName ]
                    
                    if categoryWord != "": # some pages don't have the category (defense,kickers) on cbs/espn
                        saveKey= categoryWord+ "_" + saveKey
                    
                    saveKey= saveKey.upper()
                        
                    if saveKey is not None:
                        playerDict[ saveKey ]= attemptFloatParse( aTag.text.replace( ",", "" ) ) # handle numbers with commas
            else:
                pass
              
        return playerDict
    
    def getColumnMethodOverRide( self ):
        return self._columnMethodOverRide
    
    def setColumnMethodOverRide( self, inArg ):
        if inArg is None:
            return 
        
        self._cols2override= []
        saveList= []
        assert isinstance( inArg, list ), "input must be of type list"
        for anItem in inArg:
            assert isinstance( anItem, tuple ), "types in list must be tuples"
            assert len( anItem ) == 2, "tuple must be of length 2 with column followed by method" 
            assert is_numeric( anItem[0] ), "First input must be numeric"
            str( type( anItem[ self._colOverrideMethodIdx ]) ) == "<class 'method'>", "second element in tuple must be class method"
            
            if anItem[0] not in self._cols2override: # remove duplicate specified columns 
                self._cols2override.append( anItem[0] )
                saveList.append( anItem )
            
        self._columnMethodOverRide= saveList
    
    @abstractmethod # this forces the subclass to define this
    def _isTableHeadOfNoConcern( self ):
        """Checks if the table is part of the header for each subclass"""
        return
        
    @abstractmethod # this forces the subclass to define this
    def _setTableBodyFromTableList( self ):
        """Sometimes there could be more than one table in the page, this method should
        find the body for the subclass"""
        return
    
    @abstractmethod # this forces the subclass to define this
    def _isTableHead( self, aRow ):
        """Each page has unique html tags which say where the correlation to pass,run, etc is to how many colums
        This will identify that row for each subclass"""
    
    @abstractmethod # this forces the subclass to define this    
    def _isTableSubHead( self, aRow ):
        """Each page has unique html tags which say where the correlation to pass,run, etc is to how many colums
        This will identify that row for each subclass"""
        
    @abstractmethod # this forces the subclass to define this
    def _isPlayerRow( self, aRow ):
        """Each of the player rows are identified in different ways"""
        
    @abstractproperty # this forces the subclass to define this
    def _tableColumnNames( self ):
        """The able column(s) you care about for the subclass"""
    
    @abstractproperty # this forces the subclass to define this    
    def _saveCSV( self ):
        """The csv name to which the data will be saved"""
    
    @abstractproperty # this forces the subclass to define this
    def _statColRemap( self ):
        """This will make sure the words are consistent between sites."""
    
    @abstractproperty # this forces the subclass to define this    
    def _nameRegex( self ):
        """subclass identification string"""
    
    @abstractproperty    
    def _tableHeaderTag( self ):
        """the html tag of the header data"""
    
    @abstractproperty    
    def _tableSubHeaderTag( self ):
        """the html tag of sub-header data"""

    def getSites( self ):
        return self._sites
    
    def setSites( self, inArg ):
            
        assert isinstance( inArg, list ), "_sites must be a list"
        self._sites= inArg
        
    def _isnextSiteLink( self, aTag, pageAddress, nextTableList ):
        return re.search( 'NEXT', aTag.text.strip().upper() )
    
    def getTblObj( self ):
        return self._otherTblProcObjs
    
    def setTblObj( self, inObjs ):
        assert isinstance( inObjs, list ), ""
        for anObj in inObjs:
            assert isinstance( anObj, ProjTableBase ), "Not the proper type: " + str( anObj )
            
        self._otherTblProcObjs= inObjs
    
    def getTables( self ):
        return self._tables
    
    def setTables( self, inArg ):
        assert isinstance( inArg, list )
        self._tables= inArg
         
    """special override for a column which needs weird parsing"""
    columnMethodOverRide= property( getColumnMethodOverRide, setColumnMethodOverRide )
    
    """The website(s) from which they will get pulled"""
    sites= property( getSites, setSites )
    otherTblProcObjs= property( getTblObj, setTblObj )
    tables= property( getTables, setTables )

def is_numeric( inArg ):
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all( hasattr( inArg, attr ) for attr in attrs )
 
def attemptFloatParse(strIn):
    try:
        return( float( strIn) )
    except:
        return np.NAN
    