import os
import re

from matplotlib import style

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

    # split filepath into root and extension
    splitTuple = os.path.splitext(filePath)

    # extract the filename
    filename = splitTuple[0]

    # extract the file extension
    fileExtension = splitTuple[1]

    # check the extension of the file
    if(fileExtension != None and fileExtension == '.html'):
        
        # open the file
        textFile = open('index.html', 'r+')
        # read the file as a string
        htmlText = textFile.read()

        #close the file
        textFile.close()
        
        # check if the file contains a special expression at the beginning of the file
        if(htmlText.find('<!DOCTYPE html>') >= len(htmlText) - len(htmlText.lstrip())):
            
            # separate tags into a list
            tagList = re.findall(r'<[^>\n]+>', htmlText)
            # remove <!DOCTYPE html> from tag list
            tagList = tagList[1 : ]
            tagList = [tag[1 : -1] for tag in tagList]

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

                for tag in tagList:
                    if('link' in tag.split() and 'rel="stylesheet"' in tag.split()): # reduce it to 'stylesheet' search
                        tagList.remove(tag)
                        htmlText = htmlText.replace('<' + tag + '>', '')

                tagsToBeRemovedWithoutContent = ['big', 'strong', 'em', 
                                                 'i', 'kbd' 'mark',
                                                 'var', 'big', 'blink']
                
                for tag in tagList:
                    openTag = tag.split()[0]
                    if(openTag in tagsToBeRemovedWithoutContent):
                        tagList.remove(tag)
                        tagList.remove('/' + openTag)
                        htmlText = htmlText.replace('<' + openTag, '')
                        htmlText = htmlText.replace('</' + openTag + '>', '')
                
                for tag in tagList:
                    attributesWithValues = re.findall(r'[^\s\n]+\s*=\s*"[^>\n]+"', tag)
                    for attribute in attributesWithValues:
                        attributeName = attribute.split('=')[0]
                        attributeValue = attribute.split('=')[1][1 : ].replace('"', '')
                        if (attributeName == 'style'
                        or   (attributeName == 'marginheight'
                           or attributeName == 'marginwidth'
                           and int(attributeValue) > 20)
                        or   (attributeName == 'frameborder'
                           or attributeName == 'border'
                           and int(attributeValue) > 1)
                        or   (attributeName == 'size'
                           and int(attributeValue) > 40)
                        or   (attributeName == 'height'
                           or attributeName == 'width'
                           and int(attributeValue) > 300)):

                            newTag = tag.replace(attribute, '')
                            tagList[tagList.index(tag)] = newTag
                            htmlText = htmlText.replace(attribute, '')

                # delete double spaces
                while(htmlText.find('  ') != -1):
                    htmlText = htmlText.replace('  ', '', 1)
                # delete double new lines
                while(htmlText.find('\n\n') != -1):
                    htmlText = htmlText.replace('\n\n', '\n', 1)
                # delete double new lines
                while(htmlText.find('\n ') != -1):
                    htmlText = htmlText.replace('\n ', '\n', 1)

                with open(filename + '-sans-decor.html', 'w') as outfile:
                    outfile.writelines(htmlText)