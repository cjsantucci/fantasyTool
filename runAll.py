'''
Created on Aug 3, 2017

@author: chris
'''
import ffl
from ffl.projTableBase import ProjTableBase
import pandas as pd
from importlib import import_module
import inspect
from multiprocessing import Pool
import os
import re
import warnings

def main( all2run ):
    outputList= []
    for anObject in all2run:
        tOutput= anObject.process()
        outputList += tOutput
        
    save( outputList )    

def save( outputList ):
    fflData= pd.DataFrame( outputList )
    fflData.to_csv( "/home/chris/Desktop/fflOutput/fflAll_2017.csv" )
#     fflData.to_hdf( "/home/chris/Desktop/fflOutput/fflAll_2017.h5", key="fflData" )

def mainParallel( all2run ):
    with Pool( processes= 4 ) as p:
        results= [ p.map_async( runProcess, (anObject,) ) for anObject in all2run ]
    
        outputList= []    
        for aRes in results:
            tData= aRes.get()
            outputList += tData[0]
            
    save( outputList )

def runProcess( anObject ):
    return anObject.process()
  
def load_h5():
    fflData= pd.read_hdf("/home/chris/Desktop/fflOutput/fflAll_2017.h5", key="fflData")
    
def load_csv():
    fflData= pd.read_csv("/home/chris/Desktop/fflOutput/fflAll_2017.csv", key="fflData")
    
if __name__ == '__main__':
    #load_h5()
    #load_csv()
    all2run= []
    
    """ Get the names of any .py file that ends in Grabber.py"""
    packageObject= inspect.getmodule( ffl )
    packageDir= os.path.dirname( packageObject.__file__ )
    listings= os.listdir( packageDir )
    print("retrieving all names which end in Grabber.py ...")
    full_files= [ os.path.join( packageDir, aListing ) for aListing in listings 
            if os.path.isfile( os.path.join( packageDir, aListing ) ) and 
             os.path.join( packageDir, aListing ).endswith(".py") and
             re.search( ".*Grabber\.py$" , aListing ) ]
    
    importModuleNames= [ "ffl." + os.path.split( aName )[-1].split( ".py" )[0] for aName in full_files ]
    
    
    """Grab all of the class objects excluding specific ones"""
    exclusionClassList= [ "NFG_names", "ProjTableBase" ]
    classes2Construct=[]
    for aModuleName in importModuleNames:
        moduleMembers= inspect.getmembers( import_module( aModuleName ) )
        for aModuleName, aModuleObject  in moduleMembers:
            if inspect.isclass( aModuleObject ) and aModuleName not in exclusionClassList:
                classes2Construct.append( aModuleObject )
    
    """Construct the class for processing."""
    tAll2run= [ aClass() for aClass in classes2Construct ]
    
    """Check the types"""
    all2run= []
    for aClassInstance in tAll2run:
        if isinstance( aClassInstance, ProjTableBase ):
            all2run.append( aClassInstance )
        else:
            warnings.warn( "Class not correct type: " + str( aClassInstance ) )

    mainParallel( all2run )
    #main( all2run )
    
    print("---------------------All Complete---------------------")
    
    