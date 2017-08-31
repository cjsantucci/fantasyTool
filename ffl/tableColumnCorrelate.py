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
    
    """Use this tag to search for column widths"""
    
    def __init__( self, nameRegex= None, columnNames= None, statColRemap= None, tableHeaderTag= "td", tableSubHeaderTag= "td" ):
        
        self.col2ColumnCategory= {}
        self.col2ColumnName= {}
        self.columnCategoryToColumnNumber= {}
        self._statColRemap= None
        self._tableColumnNames= None
        
        self._nameRegex= nameRegex
        self._tableHeaderTag= tableHeaderTag
        self._tableSubHeaderTag= tableSubHeaderTag
        self.tableColumnNames= columnNames
        self.statColRemap= statColRemap
    
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
         
        for aData in aRow.findAll( self._tableHeaderTag ):
            if self.tableColumnNames is None:
                return
                
            if "colspan" in aData.attrs.keys():
                cspan= aData[ "colspan" ]
            else:
                cspan=1
                
            newCols= list( np.arange( lastCol+1, lastCol+1+int( cspan ) ) )
            
            if aData.string.strip() != "" and aData.string.strip() is not None and \
                aData.string.strip().upper() in self.tableColumnNames:
                self.columnCategoryToColumnNumber[ aData.string.strip().upper() ]= newCols
                allCols= allCols+newCols
                
            lastCol += int( cspan )
    
        self.columnCategoryToColumnNumber[ self.allColsKey ]= allCols
    
    def _mapCategory2ColumnNums_NoHeader( self, aRow ):
        """This is the case that handles when there is no main header when tableColumnNames is None"""
        allColData= aRow.findAll( self._tableSubHeaderTag )
        newCols= [ idx+1 for idx, anElement in enumerate( allColData ) ]
        
        self.columnCategoryToColumnNumber[ "" ]= newCols
        self.columnCategoryToColumnNumber[ self.allColsKey ]= newCols
    
    def _mapColumns2Category( self, aRow ):
        
        if self.tableColumnNames is None: # special case for some sites
            self._mapCategory2ColumnNums_NoHeader( aRow )
        
        col= 0
        for aData in aRow.findAll( self._tableSubHeaderTag ):
            col += 1
            if col in self.columnCategoryToColumnNumber[ self.allColsKey ]:
                self.col2ColumnName[ col ]= aData.text.strip().upper()
                self.col2ColumnCategory[ col ]= self._findCategoryWord( col )
                
    def getTableColumnNames( self ):
        return self._tableColumnNames 
    
    def setTableColumnNames( self, inArg ):
        if inArg is None:
            return
        
        assert isinstance( inArg, list ), "tableColumnNames must be list or type None"
        
        for argListIdx, anItem in enumerate( inArg ):
            assert isinstance( anItem, str ), str(anItem) + " must be type string in tableColumnNames list"
            inArg[ argListIdx ]= anItem.upper()
        
        
        self._tableColumnNames= inArg
        
    def getStatColRemap( self ):
        return self._tableColumnNames 
    
    def setStatColRemap( self, inArg ):
        if inArg is None:
            return
        
        assert isinstance( inArg, dict ), "tableColumnNames must be list or type None"
        
        for argListIdx, aKey in enumerate( list( inArg.keys() ) ):
            assert isinstance( inArg[aKey], str ), str( inArg[aKey] ) + " must be type string in statColRemap dict"
            if aKey != aKey.upper():
                inArg[ aKey.upper() ]= inArg[ aKey ]
                del inArg[ aKey ]
        
        
        self._statColRemap= inArg
    
    # end setTableColumnNames
    
    statColRemap= property( getStatColRemap, setStatColRemap )
    tableColumnNames= property( getTableColumnNames, setTableColumnNames )