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
        var.assertEqual(len(redecorator.extractTags(htmlText)), 7, "Should be 7")
    
    def test_CheckTagMatching(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'body', '', '', True, 'html', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image1"'], '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'script', '', '', True, 'body', 1)
        htmlTags = redecorator.extractTags(htmlText)
        var.assertEqual(redecorator.checkTagMatching(htmlTags), True, "Should be True")
        htmlText += '</additionalTag>'
        htmlTags = redecorator.extractTags(htmlText)
        var.assertEqual(redecorator.checkTagMatching(htmlTags), False, "Should be False")

    def test_CheckStyleTagRemoval(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'body', '', '', True, 'html', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image1"'], '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'script', '', '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'style', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'style', 1)
        htmlTags = redecorator.extractTags(htmlText)
        htmlTags, htmlText = redecorator.removeStyleAndScriptTags(htmlTags, htmlText)
        var.assertEqual(htmlText.find('<something>'), -1, "Should be -1")
        var.assertEqual(htmlText.find('<style>'), -1, "Should be -1")

    def test_CheckTagRemovalWithContent(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'body', '', '', True, 'html', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image1"'], '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'script', '', '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'figure', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'figure', 1)
        htmlText = TagFactory.addTag(htmlText, 'embed', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'embed', 1)
        htmlText = TagFactory.addTag(htmlText, 'iframe', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'iframe', 1)
        htmlText = TagFactory.addTag(htmlText, 'object', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'object', 1)
        htmlTags = redecorator.extractTags(htmlText)
        htmlTags, htmlText = redecorator.removeTagsWithContent(htmlTags, htmlText)
        var.assertEqual(htmlText.find('<embed>'), -1, "Should be -1")
        var.assertEqual(htmlText.find('<iframe>'), -1, "Should be -1")
        var.assertEqual(htmlText.find('<object>'), -1, "Should be -1")
        var.assertEqual(htmlText.find('<figure>'), -1, "Should be -1")

    def test_CheckTagRemovalWithContent(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'body', '', '', True, 'html', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image1"'], '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'script', '', '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'figure', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'figure', 1)
        htmlText = TagFactory.addTag(htmlText, 'embed', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'embed', 1)
        htmlText = TagFactory.addTag(htmlText, 'iframe', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'iframe', 1)
        htmlText = TagFactory.addTag(htmlText, 'object', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something', '', '', True, 'object', 1)
        htmlTags = redecorator.extractTags(htmlText)
        htmlTags, htmlText = redecorator.removeTagsWithContent(htmlTags, htmlText)
        var.assertEqual(htmlText.find('<embed>'), -1, "Should be -1")
        var.assertEqual(htmlText.find('<iframe>'), -1, "Should be -1")
        var.assertEqual(htmlText.find('<object>'), -1, "Should be -1")
        var.assertEqual(htmlText.find('<figure>'), -1, "Should be -1")

    def test_CheckStyleLinkingRemoval(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText += '\n' + '<link rel="stylesheet" href="https://www.site.com">'
        htmlTags = redecorator.extractTags(htmlText)
        htmlTags, htmlText = redecorator.removeStyleLinking(htmlTags, htmlText)
        var.assertEqual(htmlText.find('<link rel="stylesheet"'), -1, "Should be -1")

    def test_CheckTagRemovalWithContent(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'body', '', '', True, 'html', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image1"'], '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'script', '', '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'big', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something1', '', '', True, 'big', 1)
        htmlText = TagFactory.addTag(htmlText, 'strong', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something2', '', '', True, 'strong', 1)
        htmlText = TagFactory.addTag(htmlText, 'kbd', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something3', '', '', True, 'kbd', 1)
        htmlText = TagFactory.addTag(htmlText, 'mark', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'something4', '', '', True, 'mark', 1)
        htmlTags = redecorator.extractTags(htmlText)
        htmlTags, htmlText = redecorator.removeTagsWithoutContent(htmlTags, htmlText)
        var.assertEqual(htmlText.find('<big>'), -1, "Should be -1")
        var.assertFalse(htmlText.find('<something1>') == -1, "Should not be -1")
        var.assertEqual(htmlText.find('<strong>'), -1, "Should be -1")
        var.assertFalse(htmlText.find('<something2>') == -1, "Should not be -1")
        var.assertEqual(htmlText.find('<kbd>'), -1, "Should be -1")
        var.assertFalse(htmlText.find('<something3>') == -1, "Should not be -1")
        var.assertEqual(htmlText.find('<mark>'), -1, "Should be -1")
        var.assertFalse(htmlText.find('<something4>') == -1, "Should not be -1")
    
    def test_CheckTagsRemovalConditionally(var):
        htmlText = '<!DOCTYPE html>'
        htmlText = TagFactory.addTag(htmlText, 'html', '', '', False, '', 1)
        htmlText = TagFactory.addTag(htmlText, 'body', '', '', True, 'html', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image1"', 'height="450"'], '', True, 'body', 1)
        htmlText = TagFactory.addTag(htmlText, 'img', ['class="image2"', 'height="100"'], '', True, 'body', 1)
        htmlTags = redecorator.extractTags(htmlText)
        htmlTags, htmlText = redecorator.removeTagsConditionally(htmlTags, htmlText)
        var.assertFalse(htmlText.find('class="image1"') == -1, "Should not be -1")
        var.assertFalse(htmlText.find('class="image2"') == -1, "Should not be -1")
        var.assertEqual(htmlText.find('height="450"'), -1, "Should be -1")
        var.assertFalse(htmlText.find('height="200"') == -1, "Should not be -1")

if __name__ == "__main__":
    unittest.main()