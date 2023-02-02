#bindetect.py detects strings inside a .bin file
#bin file structure info can be found here https://github.com/Ravernstal/gof2-bin-info
from os import PathLike
from typing import List, Literal, Union, overload

BinType = Literal['names', 'stations', 'systems']
FilePathType = Union[str, PathLike[str]]

@overload
def detectStrings(binFile: FilePathType, binType: BinType, returnType: Literal['string']) -> str: ...
@overload
def detectStrings(binFile: FilePathType, binType: BinType, returnType: Literal['list', 'string'] = 'list') -> List[str]: ...

def detectStrings(binFile: FilePathType, binType: BinType, returnType: Literal['list', 'string'] = 'list') -> Union[str, List[str]]:
    """
    detects the strings inside a bin file and places them into an array

    :param str binFile: path to the .bin file
    :param str binType: Type of bin file. Valid binTypes are: 'names', 'stations', 'systems'
    :param str returnType: Determines what type of object should be returned in the end. Valid returntypes are: 'list', 'string'
    """
    names: List[str] = []
    
    #for "names_" .bin files
    if binType == 'names':
        with open(binFile, 'rb') as f:
            
            #00 00 00 NUM SEP
            f.read(3)
            amount = ord(f.read(1)) #extract amount of bytes
            

            try:
                for i in range(0, amount ):

                    f.read(1)#skip seperator
                    length = ord(f.read(1)) #read length
                    name = f.read(length).decode() #extract name

                    names.append(name)

            except EOFError:
                print("EOF reached!")
            
            
            f.close()
    

    #for the stations.bin file
    if binType == 'stations':
        with open(binFile, 'rb') as f:
            reachedEnd = False
            try:
                while reachedEnd == False:

                    f.read(1) #seperator
                    length = ord(f.read(1)) #read length
                    name = f.read(length).decode() #extract name
                    names.append(name)

                    f.read(16) #skip Station ID, System ID, Tech level and Planet Background    
            except Exception as e:
                print(e)
                reachedEnd = True


    #for the systems.bin file
    if binType == 'systems':
        with open(binFile, 'rb') as f:
            reachedEnd = False
            try:
                while reachedEnd == False:

                    f.read(1) #seperator
                    length = ord(f.read(1)) #read length
                    name = f.read(length).decode() # extract name
                    names.append(name)

                    f.read(48) #skip risk lvl, visibility, faction, coordinates, jumpgate station, star colour and the unknown block
                    
                    f.read(3)
                    stationBlock = ord(f.read(1))
                    f.read(stationBlock * 4) #skip stations
                    #print(f"skipped {stationBlock}")

                    f.read(3)
                    linkedBlock = ord(f.read(1))
                    f.read(linkedBlock * 4) #skip linked systems
                    #print(f"skipped {linkedBlock}")
                    
                    f.read(16) #skip last unknown block

            except Exception as e:
                print(e)
                reachedEnd = True
            
    if returnType == 'list':
        return names
    elif returnType == 'string':
        return "\n".join(names)
