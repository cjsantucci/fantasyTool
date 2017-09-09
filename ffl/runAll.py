'''
Created on Aug 3, 2017

@author: chris
'''
from ffl import getAllModules, getClassInstances
import pandas as pd

from multiprocessing import Pool

def main( all2run ):
    
    outputList= []
    for anObject in all2run:
        tOutput= anObject.process()
        outputList += tOutput
        
    save( outputList )    

def save( outputList ):
    
    fflData= pd.DataFrame( outputList )
    fflData.to_csv( "/home/chris/Desktop/fflOutput/fflAll_2017.csv" )

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
    
def runAllDynamic():
    importModuleNames= getAllModules()
    all2run= getClassInstances( importModuleNames= importModuleNames ) 
    mainParallel( all2run )
    print("---------------------All Complete---------------------")

if __name__ == '__main__':
    runAllDynamic()
    
    