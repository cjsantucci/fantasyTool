'''
Created on Aug 3, 2017

@author: chris
'''

import numpy as np
import re
import warnings

class ColumnCorrelate( object ):
    """
    
    This class has the data to column correlate the headers of the tables
    
    """
    allColsKey= "allcols_found"
    col2ColumnCategory= {}
    col2ColumnName= {}
    columnCategoryToColumnNumber= {}
    _nameRegex= None
    
    """Use this tag to search for column widths"""
    _siteTag= "td"
    
    _statColRemap= None
    _tableColumnNames= None
    
    def __init__( self, nameRegex= None, columnNames= None, statColRemap= None ):
        self._nameRegex= nameRegex
        self._setSiteTag()
        self.tableColumnNames= columnNames
        self._statColRemap= statColRemap
            
    def _setSiteTag( self ):
        if re.search( self._nameRegex, "CBS" ) or re.search( self._nameRegex, "FFTODAY" ):
            self._setSite= "td"
        elif re.search( self._nameRegex, "ESPN" ):
            self._siteTag= "th"
        else:
            warnings.warn( "Unhandled Case will default to \"td\" for site: " + self._nameRegex )
            
    
    def _findCategoryWord( self, col ):
        for aKey in self.columnCategoryToColumnNumber.keys():
            if col in self.columnCategoryToColumnNumber[ aKey ] and aKey != self.allColsKey:
                return aKey
            
        return None  
            
    def _mapCategory2ColumnNums( self, aRow ):
        """Takes in the header row and keys off of html "colspan" to determine
        How many columns belong to RUSHING,PASSING, etc
        Use it later to group/rename data appropriately"""
        
        
        lastCol= 0
        allCols= []
         
        for aData in aRow.findAll( self._siteTag ):
            if self.tableColumnNames is None:
                return
                
            if "colspan" in aData.attrs.keys():
                cspan= aData[ "colspan" ]
            else:
                cspan=1
                
            newCols= list( np.arange( lastCol+1, lastCol+1+int( cspan ) ) )
            
            if aData.string is not None and aData.string.upper() in self.tableColumnNames:
                self.columnCategoryToColumnNumber[ aData.string.upper() ]= newCols
                allCols= allCols+newCols
                
            lastCol += int( cspan )
    
        self.columnCategoryToColumnNumber[ self.allColsKey ]= allCols
    
    def _mapCategory2ColumnNums_NoHeader( self, aRow ):
        """This is the case that handles when there is no main header when tableColumnNames is None"""
        allColData= aRow.findAll( self._siteTag )
        newCols= [ idx+1 for idx, anElement in enumerate( allColData ) ]
        
        self.columnCategoryToColumnNumber[ "" ]= newCols
        self.columnCategoryToColumnNumber[ self.allColsKey ]= newCols
    
    def _mapColumns2Category( self, aRow ):
        
        if self.tableColumnNames is None: # special case for some sites
            self._mapCategory2ColumnNums_NoHeader( aRow )
        
        col= 0
        for aData in aRow.findAll( "td" ):
            col += 1
            if col in self.columnCategoryToColumnNumber[ self.allColsKey ]:
                self.col2ColumnName[ col ]= aData.text.strip()
                self.col2ColumnCategory[ col ]= self._findCategoryWord( col )
                
    def getTableColumnNames( self ):
        return self._tableColumnNames 
    
    def setTableColumnNames( self, inArg ):
        if inArg is None:
            return
        
        assert type( inArg ) is type( list() ), "tableColumnNames must be list or type None"
        
        for anItem in inArg:
            assert type( anItem ) is type( str() ), str(anItem) + " must be type string in tableColumnNames list" 
            
        self._tableColumnNames= inArg
    
    # end setTableColumnNames
    
    tableColumnNames= property( getTableColumnNames, setTableColumnNames )