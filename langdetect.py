#langdetect extracts the strings of a lang file and dumps them into a list
import os
from os import PathLike
from typing import Union

FilePathType = Union[str, PathLike[str]]

def extractLang(langPath: FilePathType) -> list[str]: 
    """
    extracts the strings of a .lang file and dumps them into a list
    
    :param str langPath: Path of the .lang file
    """

    langList = []
    reachedEnd = False

    #lang structure: LENGTH1 LENGTH2 STR LENGTH1 LENGTH2 STR ...
    #LENGTH1 is =0 in most cases, but when strings do exceed a certain length, that length will be inside LENGTH1 and LENGTH2
    with open(langPath, 'rb') as f:
        file_size = os.stat(langPath).st_size

        try:
            #try until it reaches the end of the file
            while f.tell() < file_size:          
                length = int.from_bytes(f.read(2), byteorder='big') #reads next two bytes, as the length is stored in those two
                extractedStr = f.read(length).decode('utf-8')
                if extractedStr == '':
                    break
                else:
                    langList.append(extractedStr)

        except Exception as e:
            print(e)

        f.close()
    
    return langList


def writeLang(langList: list[str], exportPath: FilePathType):
    """
    Takes a list of strings and writes a .lang file

    :param list langList: the list of strings
    :param FilePathType exportPath: Path of the exported file. Should end with ".lang"
    """
    with open(exportPath, 'wb') as f:

        for i in langList:
             
             lengthByte = len(bytes(i, 'utf-8')).to_bytes(2, 'big')
             
             f.write(lengthByte)
             f.write(bytes(i, 'utf-8'))