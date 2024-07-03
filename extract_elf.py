#!/usr/bin/python3

import sys
import io
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

def getELFSize(ELFStream):
    buf = io.BytesIO(ELFStream)
    elffile = ELFFile(buf)
    
    
    
    e_ehsize = int(elffile.header['e_ehsize'])
    e_phnum = int(elffile.header['e_phnum'])
    e_phentsize = int(elffile.header['e_phentsize'])
    e_shnum = int(elffile.header['e_shnum'])
    e_shentsize = int(elffile.header['e_shentsize'])
    e_shoff = int(elffile.header['e_shoff'])
    
    
    prelimFileSize = (e_ehsize + (e_phnum * e_phentsize) + (e_shnum * e_shentsize))
    
    ELF64size = e_shoff + (e_shentsize * e_shnum)
    print(prelimFileSize)
    print(ELF64size)
    return ELF64size 


filename = sys.argv[1]
current_offset = 0
ELFFiles = []
with open(filename, 'rb') as fd:
    while True:
        byte = fd.read(1)
        if not byte:
            break
        current_offset += 1
        if byte == b'\x7f':
            next3 = fd.read(3)
            if next3 == b'ELF': #If ELF header detected
                fd.seek(current_offset - 1)
                ELFHeader = fd.read(64)
                try:
                    ELFSize = getELFSize(ELFHeader)
                except:
                    fd.seek(current_offset)
                    continue
                fd.seek(current_offset - 1)
                try:
                    ELFBytes = fd.read(ELFSize)
                except:
                    continue
                ELFFiles.append(ELFBytes)
                current_offset += ELFSize - 1 

            else:
                fd.seek(current_offset)


fileCount = 0
for file in ELFFiles:
    outputFilename = "outputELF" + str(fileCount)
    with open(outputFilename, 'wb') as fd2:
        fd2.write(file)
    fileCount += 1 

