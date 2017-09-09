__license__ = """
Copyright (c) 2012 mpldatacursor developers
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__version__ = '1.0'

__all__= [ "tableColumnCorrelate" ]

import ffl
import ffl.grabbers
from importlib import import_module
import inspect
import numpy as np
import os
import re
import traceback
import warnings

def is_numeric( inArg ):
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all( hasattr( inArg, attr ) for attr in attrs )
 
def attemptFloatParse(strIn):
    try:
        return( float( strIn) )
    except:
        return np.NAN
    
def getSelfModuleName( levelUp= 1 ):
    fName= inspect.getouterframes( inspect.currentframe() )[ levelUp ].filename
    
    modName= os.path.basename( fName ).split( ".py" )[ 0 ]
    
    tPathName= fName.split( "ffl" )
    packageName= os.path.basename( os.path.dirname( tPathName[1] ) )
    return "ffl." + packageName + "." + modName

def getAllModules():
    """ Get the names of any .py file that ends in Grabber.py"""
    packageObject= inspect.getmodule( ffl.grabbers )
    packageDir= os.path.dirname( packageObject.__file__ )
    listings= os.listdir( packageDir )
    print("retrieving all names which end in Grabber.py ...")
    full_files= [ os.path.join( packageDir, aListing ) for aListing in listings 
            if os.path.isfile( os.path.join( packageDir, aListing ) ) and 
             os.path.join( packageDir, aListing ).endswith(".py") and
             re.search( ".*Grabber\.py$" , aListing ) ]
    
    importModuleNames= [ "ffl.grabbers." + os.path.split( aName )[-1].split( ".py" )[0] for aName in full_files ]
    return importModuleNames

def executeClassMain( classInstancesList= None, save2csv= True ):
    """ INtended to be called from main of a Grabber.py """
    if classInstancesList is None:
        classInstancesList= getClassInstances( levelUp= 3 )
        
    outputList= []
    for anObj in classInstancesList:
        outputList += anObj.process( save2csv= save2csv )
        
    return outputList

def getClassInstances( importModuleNames= None, levelUp= 2 ):
    """ Get all instances for a set of modules """
    if importModuleNames is None:
        importModuleNames= [ getSelfModuleName( levelUp= levelUp ) ]
    
    """Grab all of the class objects excluding specific ones"""
    exclusionClassList= [ "NF_names", "ProjTableBase" ]
    classes2Construct=[]
    for aModuleName in importModuleNames:
        moduleMembers= inspect.getmembers( import_module( aModuleName ) )
        for moduleMemberName, aModuleObject  in moduleMembers:
            if inspect.isclass( aModuleObject ) and moduleMemberName not in exclusionClassList:
                classes2Construct.append( aModuleObject )
    
    """Construct the class for processing."""
    tAll2run= []
    for aClass in classes2Construct:
        try:
            tAll2run.append( aClass() )
        except:
            traceback.print_exc()
    
    """Check the types"""
    all2run= []
    for aClassInstance in tAll2run:
        if isinstance( aClassInstance, ffl.projTableBase.ProjTableBase ):
            all2run.append( aClassInstance )
        else:
            warnings.warn( "Class not correct type: " + str( aClassInstance ) )
    
    return all2run

def initConditionedTeamNameDict():
    """ Make sure lots of possible team names come out to something consistent each time """
    """ Second one in the tuple pairs is the actual name. """
    
    
    nameCityPairs= [ ( "Arizona Cardinals", "Cardinals"), ( "Denver Broncos", "Broncos" ), ( "Kansas City Chiefs", "Chiefs" ), \
      ( "Philadelphia Eagles", "Eagles" ), ( "Miami Dolphins", "Dolphins" ), ( "New England Patriots", "Patriots" ), \
      ( "Seattle Seahawks", "Seahawks" ), ( "Green Bay Packers", "Packers" ), ( "New York Giants", "Giants" ), \
      ( "Carolina Panthers", "Panthers" ), ( "Los Angeles Chargers", "Chargers" ), ( "Jacksonville Jaguars", "Jaguars" ), \
      ( "Tampa Bay Buccaneers", "Buccaneers" ), ( "Minnesota Vikings", "Vikings" ), ( "Houston Texans", "Texans" ), \
      ( "Washington Redskins", "Redskins" ), ( "Pittsburgh Steelers", "Steelers" ), ( "Buffalo Bills", "Bills" ), \
      ( "Los Angeles Rams", "Rams" ), ( "Indianapolis Colts", "Colts" ), ( "Baltimore Ravens", "Ravens" ), \
      ( "Oakland Raiders", "Raiders" ), ( "Tennessee Titans", "Titans" ), ( "Atlanta Falcons", "Falcons" ), \
      ( "Dallas Cowboys", "Cowboys" ), ( "Cincinnati Bengals", "Bengals" ), ( "Detroit Lions", "Lions" ), \
      ( "San Francisco 49ers", "49ers" ), ( "New Orleans Saints", "Saints" ), ( "Chicago Bears", "Bears" ), \
      ( "Cleveland Browns", "Browns" ), ( "New York Jets", "Jets" ) ]
    
    # the city names could be identifiers
    cityNameList= []
    for cityName, name in nameCityPairs:
        city= " ".join( cityName.strip().split()[0:-1] )
        cityNameList.append( ( city, name ) )
    
    abbrevPairs= [ ( "GB", "Packers" ), ( "NE", "Patriots" ), \
      ( "NO", "Saints" ), ( "TB", "Buccaneers" ), ( "SEA", "Seahawks" ), \
      ( "ATL", "Falcons" ), ( "IND", "Colts" ), ( "LAC", "Chargers" ), ( "TEN", "Titans" ), ( "DET", "Lions" ), \
      ( "HOU", "Texans" ), ( "PIT", "Steelers" ), ( "CAR", "Panthers" ), ( "CIN", "Bengals" ), ( "DAL", "Cowboys" ), \
      ( "WAS", "Redskins" ), ( "OAK", "Raiders" ), ( "NYG", "Giants" ), ( "ARI", "Cardinals" ), ( "PHI", "Eagles" ), \
      ( "BUF", "Bills" ), ( "KC", "Chiefs" ), ( "BAL", "Ravens" ), ( "MIN", "Vikings" ), ( "MIA", "Dolphins" ), \
      ( "DEN", "Broncos" ), ( "CHI", "Bears" ), ( "LAR", "Rams" ), ( "SF", "49ers" ), ( "JAC", "Jaguars" ), \
      ( "NYJ", "Jets" ), ( "CLE", "Browns" ), ( "WSH", "Redskins" ), ( "Jax", "Jaguars" ) ]
    
    # special cases
    l2= [ ( "FA", "FreeAgent" ), ( "", "" ), ( " ", "" ) ] # has 2 duplicates for ""
    
    totList= nameCityPairs+ abbrevPairs+ cityNameList+ l2
    
    willbeKeys, names= zip( *totList )
    willbeKeys= list( willbeKeys )
    names= list( names )
    
    unqNames= []
    [ unqNames.append( aName.upper() ) 
        for aName in names 
        if aName.upper() not in unqNames ]

    nameDict= {}
    for nameidx, aKey in enumerate( willbeKeys ):
        nameDict[ aKey.upper() ]= names[ nameidx ].upper()
    
    for aKey in unqNames:
        nameDict[ aKey.upper() ]= aKey.upper()
    
    nTeams= 32
    assert len( unqNames ) == nTeams + (len( l2 )-1) # see comment above
    
    return nameDict

def checkFields( obj, aPlayerDict, fieldsList ):
    keyList= sorted( aPlayerDict.keys() )
    for aField in fieldsList:
        try:
            assert aField in keyList, aField + " missing in: " + str( obj ) + ", for: " + str( aPlayerDict )
        except:
            traceback.print_exc()
        
def retrieveReqFieldList( procTypeStr ):
    if procTypeStr == "QB":
        fieldsList= [ "NAME", "PROJECTED_PTS", \
                     "PASSING_ATT", "PASSING_CMP", "PASSING_TD", \
                     "PASSING_YDS", "PASSING_TD", "PASSING_INT", \
                     "RUSHING_YDS", "RUSHING_TD", "RUSHING_ATT" ]
    elif procTypeStr == "RB":
        fieldsList= [ "NAME", "PROJECTED_PTS", \
                     "RECEIVING_YDS", "RECEIVING_REC", "RECEIVING_TD", \
                     "RUSHING_YDS", "RUSHING_TD", "RUSHING_ATT" ]
    elif procTypeStr == "WR":
        fieldsList= [ "NAME", "PROJECTED_PTS", \
                     "RECEIVING_YDS", "RECEIVING_REC", "RECEIVING_TD", \
                     "RUSHING_YDS", "RUSHING_TD", "RUSHING_ATT" ]
    elif procTypeStr == "TE":
        fieldsList= [ "NAME", "PROJECTED_PTS", \
                     "RECEIVING_YDS", "RECEIVING_REC", "RECEIVING_TD" ]
    elif procTypeStr == "DST":
        fieldsList= [ "TEAM", "PROJECTED_PTS" ]
    elif procTypeStr == "K":
        fieldsList= [ "NAME", "PROJECTED_PTS" ]
        
    return fieldsList