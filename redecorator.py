import os
import re

# TODO: reading file and files from path

def checkTagMatching(tagList):

    stack = []
    voidElements = ['<area', '<base', '<br', '<col', '<command', '<embed',
                    '<hr', '<img', '<input', '<keygen', '<link', '<meta',
                    '<param', '<source', '<track', '<video', '<audio', '<wbr']

    for tag in tagList:
        if(tag[1] != '/'):
            # check if the tag does not need closing 
            if(not set(voidElements).intersection(set(tag[ : len(tag) - 1].split()))):
                stack.append(tag)
        else:
            if(len(stack) > 0):
                openTag = stack[len(stack) - 1]
                closeTag = tag
                if(' ' in openTag):
                    openTag = openTag.split(' ')[0][1 : ]
                else:
                    openTag = openTag[1 : len(openTag) - 1]
                closeTag = closeTag[2 : len(closeTag) - 1]
                if(openTag == closeTag):
                    stack.pop()
                else:
                    return False
            else:
                return False

    if(len(stack)) == 0:
        return True
    else:
        return False
    

# get the file path
filePath = 'index.html'  

# check if the file exists
if(os.path.isfile(filePath)):

    # split filename into root and extension
    splitTuple = os.path.splitext(filePath)
    # extract the file extension
    fileExtension = splitTuple[1]

    # check the extension of the file
    if(fileExtension != None and fileExtension == '.html'):
        
        # open the file
        textFile = open('index.html', 'r+')
        # read the file
        htmlText = textFile.read()
        
        # check if the file contains a special expression at the beginning of the file
        if(htmlText.find('<!DOCTYPE html>') >= len(htmlText) - len(htmlText.lstrip())):
            # separate tags into a list
            tagList = re.findall(r'<[^>\n]+>', htmlText)
            # remove <!DOCTYPE html> from tag list
            tagList = tagList[1 : ]
            print(tagList)
            print(checkTagMatching(tagList))
            #close file
            textFile.close()