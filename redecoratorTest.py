import unittest
import redecorator

class TagFactory():

    def addTag(htmlText,
               tag, 
               attributes, 
               content, 
               isInside, 
               tagBefore, 
               whichOne):

        newTag = ('\n' + '<' + tag)

        for attribute in attributes:
            newTag += (' ' + attribute)

        newTag += ('>')
        
        if(not set(redecorator.voidElements).intersection(set([tag]))):
            newTag += (content)
            newTag += ('</' + tag + '>')
        
        start = len(htmlText)

        if len(tagBefore) != 0:

            start = htmlText.find('</' + tagBefore + '>') + len('</' + tagBefore + '>')
            while start >= 0 and whichOne > 1:
                start = htmlText.find('</' + tagBefore + '>', start + len('</' + tagBefore + '>'))
                whichOne -= 1

            if isInside:
                start -= len('</' + tagBefore + '>')

        if isInside:
            newTag += '\n'

        htmlText = htmlText[ : start] + newTag + htmlText[start : ]

        return htmlText
            

class Testclass(unittest.TestCase):
    
    def test_CheckTagExtracting(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'body', '', '', True, 'html', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image1"'], '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'script', '', '', True, 'body', 1)
        print(htmlText)
        var.assertEqual(len(redecorator.extractTags(htmlText)), 7, "Should be 7")
    
    def test_CheckTagExtracting(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'body', '', '', True, 'html', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image1"'], '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'script', '', '', True, 'body', 1)
        print(htmlText)
        var.assertEqual(len(redecorator.extractTags(htmlText)), 7, "Should be 7")

if __name__ == "__main__":
    unittest.main()