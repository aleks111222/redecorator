import os
import re
from turtle import begin_fill

from matplotlib.pyplot import close

# TODO: reading file and files from path

voidElements = ['area', 'base', 'br', 'col', 'command', 'embed',
                'hr', 'img', 'input', 'keygen', 'link', 'meta',
                'param', 'source', 'track', 'video', 'audio', 'wbr']

def checkTagMatching(tagList):

    stack = []

    for tag in tagList:
        if(tag[0] != '/'):
            # check if the tag does not need closing 
            if(not set(voidElements).intersection(set([tag.split()[0]]))):
                stack.append(tag)
        else:
            if(len(stack) > 0):
                openTag = stack[len(stack) - 1].split()[0]
                closeTag = tag[1 : ]
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
        # read the file as a string
        htmlText = textFile.read()
        
        # check if the file contains a special expression at the beginning of the file
        if(htmlText.find('<!DOCTYPE html>') >= len(htmlText) - len(htmlText.lstrip())):
            
            # separate tags into a list
            tagList = re.findall(r'<[^>\n]+>', htmlText)
            # remove <!DOCTYPE html> from tag list
            tagList = tagList[1 : ]
            tagList = [tag[1 : -1] for tag in tagList]

            print(tagList)

            if(checkTagMatching(tagList)):
                # remove script tags only and style tags with content 
                for (openTag, closeTag) in [('script', '/script'), ('style', '/style')]:
                    if(openTag in tagList):
                        beginList = tagList[ : tagList.index(openTag)]
                        endList = tagList[tagList.index(closeTag) + 1 : ]
                        tagList = beginList + endList
                        if(openTag == 'style'):
                            beginText = htmlText[ : htmlText.find('<' + openTag)]
                            endText = htmlText[htmlText.find(closeTag + '>') + len(closeTag) + 1 : ]
                            htmlText = beginText + endText
            
                print(tagList)

                tagsToBeRemovedWithContent = ['figure', 'img', 'area', 
                                              'map', 'video' 'embed',
                                              'iframe', 'object', 'picture',
                                              'portal', 'canvas', 'bgsound', 
                                              'frame', 'frameset', 'image']
                
                for tag in tagList:
                    if(tag.split()[0] in tagsToBeRemovedWithContent):
                        openTag = tag
                        beginList = tagList[ : tagList.index(openTag)]
                        beginText = htmlText[ : htmlText.find('<' + openTag.split()[0])]
                        if(not set(voidElements).intersection(set([tag.split()[0]]))):
                            closeTag = '/' + openTag
                            endList = tagList[tagList.index(closeTag) + 1 : ]
                            endText = htmlText[htmlText.find(closeTag + '>', len(beginText)) + len(closeTag) + 1 : ]
                        else:
                            closeTag = '>'
                            endList = tagList[tagList.index(openTag) + 1 : ]
                            endText = htmlText[htmlText.find(closeTag, len(beginText)) + len(closeTag): ]
                        htmlText = beginText + endText
                        tagList = beginList + endList
                
                print(tagList)

                
                
        #close the file
        textFile.close()