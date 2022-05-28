import os
import re
import sys

# declare the list of elements that do not need closing tags
voidElements = ['area', 'base', 'br', 'col', 'command', 'embed',
                'hr', 'img', 'input', 'keygen', 'link', 'meta',
                'param', 'source', 'track', 'video', 'audio', 'wbr']

def extractTags(htmlText):

    tagList = re.findall(r'<[^>\n]+>', htmlText)
    # remove <!DOCTYPE html> from the tag list
    tagList = tagList[1 : ]
    # remove < and > from the tags
    tagList = [tag[1 : -1] for tag in tagList]

# method for checking the matching of the html tags
# parameter: list of opening and closing tags extracted from the file
def checkTagMatching(tagList):
    stack = []
    for tag in tagList:
        # check if the tag is not the closing tag
        if(tag[0] != '/'):
            # check if the tag belongs to the void elements 
            if(not set(voidElements).intersection(set([tag.split()[0]]))):
                stack.append(tag)
        else:
            # decrease the stack if the closing tag has its closing
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

def removeStyleAndScriptTags(tagList, htmlText):
    for (openTag, closeTag) in [('script', '/script'), ('style', '/style')]:
        if(openTag in tagList):
            beginList = tagList[ : tagList.index(openTag)]
            endList = tagList[tagList.index(closeTag) + 1 : ]
            tagList = beginList + endList
            if(openTag == 'style'):
                beginText = htmlText[ : htmlText.find('<' + openTag)]
                endText = htmlText[htmlText.find(closeTag + '>') + len(closeTag) + 1 : ]
                htmlText = beginText + endText
    return tagList, htmlText

def removeTagsWithContent(tagList, htmlText):

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

    return tagList, htmlText

def removeStyleLinking(tagList, htmlText):
    for tag in tagList:
        if('link' in tag.split() and 'rel="stylesheet"' in tag.split()):
            tagList.remove(tag)
            htmlText = htmlText.replace('<' + tag + '>', '')

    return tagList, htmlText

def removeTagsWithoutContent(tagList, htmlText):

    tagsToBeRemovedWithoutContent = ['big', 'strong', 'em', 
                                     'i', 'kbd' 'mark',
                                     'var', 'big', 'blink']
                    
    for tag in tagList:
        openTag = tag.split()[0]
        if(openTag in tagsToBeRemovedWithoutContent):
            tagList.remove(tag)
            tagList.remove('/' + openTag)
            htmlText = htmlText.replace('<' + tag + '>', '')
            htmlText = htmlText.replace('</' + openTag + '>', '')

    return tagList, htmlText

def removeTagsConditionally(tagList, htmlText):

    for tag in tagList:

        attributesWithValues = re.findall(r'[^\s\n]+\s*=\s*"[^>\n]+"', tag)

        for attribute in attributesWithValues:

            attributeName = attribute.split('=')[0]
            attributeValue = attribute.split('=')[1][1 : ].replace('"', '')

            if (attributeName == 'style'

            or (attributeName == 'marginheight'
            or  attributeName == 'marginwidth'
            and int(attributeValue) > 20)

            or (attributeName == 'frameborder'
            or  attributeName == 'border'
            and int(attributeValue) > 1)

            or (attributeName == 'size'
            and int(attributeValue) > 40)

            or (attributeName == 'height'
            or  attributeName == 'width'
            and int(attributeValue) > 300)):

                newTag = tag.replace(attribute, '')
                tagList[tagList.index(tag)] = newTag
                htmlText = htmlText.replace(attribute, '')

    return tagList, htmlText

def reformat(htmlText):
    # delete double spaces
    while(htmlText.find('  ') != -1):
        htmlText = htmlText.replace('  ', '', 1)
    # delete double new lines
    while(htmlText.find('\n\n') != -1):
        htmlText = htmlText.replace('\n\n', '\n', 1)
    # delete double new lines
    while(htmlText.find('\n ') != -1):
        htmlText = htmlText.replace('\n ', '\n', 1)

    return htmlText

# function for redecorating the file
# parameter: path to a file
def redecorate(filePath):  

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
            textFile = open(filePath, 'r+')
            # read the file as a string
            htmlText = textFile.read()
            #close the file
            textFile.close()
            
            # check if the file contains a special expression at the beginning of the file
            if(htmlText.find('<!DOCTYPE html>') >= len(htmlText) - len(htmlText.lstrip())):
                
                # extract tags from the file
                tagList = re.findall(r'<[^>\n]+>', htmlText)
                # remove <!DOCTYPE html> from the tag list
                tagList = tagList[1 : ]
                # remove < and > from the tags
                tagList = [tag[1 : -1] for tag in tagList]
            
                if(checkTagMatching(tagList)):
                    
                    # apply processing
                    tagList, htmlText = removeStyleAndScriptTags(tagList, htmlText)
                    tagList, htmlText = removeTagsWithContent(tagList, htmlText)
                    tagList, htmlText = removeStyleLinking(tagList, htmlText)
                    tagList, htmlText = removeTagsWithoutContent(tagList, htmlText)
                    tagList, htmlText = removeTagsConditionally(tagList, htmlText)
                    htmlText = reformat(htmlText)

                    # save the redecorated file
                    with open(filename + '-sans-decor.html', 'w') as outfile:
                        outfile.writelines(htmlText)

def main():

    for i in range(1, len(sys.argv)):

        path = sys.argv[i]

        if(os.path.exists(path)):

            for filePath in os.listdir(path):
                print(filePath)
                redecorate(filePath)
            else:
                continue

if __name__ == "__main__":
    main()