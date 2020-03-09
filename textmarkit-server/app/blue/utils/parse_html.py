'''
    Version - 1.0
    Date - 06/02/2020
    
    Script function -
    This script consists of functions required to parse the html file.
'''

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.handletag, self.addspan, self.addanchor, self.heading1, self.heading2  = False, False, False, False, False

        self.file_content = []

    def handle_starttag(self, tag, attrs):
        if tag not in ['p', 'div', 'span', 'a', 'i', 'h1','h2', 'h3', 'h4', 'h5', 'h6']:
            print(tag, " not handled")
            return
        elif tag == 'span':
            self.addspan  = True
            self.include = False
        elif tag in ['p', 'div']:
            self.handletag = True
        elif tag == 'h1':
            self.heading1 = True
        elif tag == 'h2':
            self.heading2 = True
    
    def handle_endtag(self, tag):
        if tag in ['p', 'div']:
            if self.handletag:
                self.handletag = False
                self.addspan = False
            else:
                print("p tag not handled.")
        elif tag == 'span':
            self.include = True
        elif tag == 'h1':
            self.heading1 = False
            self.addspan = False
        elif tag == 'h2':
            self.heading2 = False
            self.addspan = False
        # else:
            # print("Encounterd an end tag.", tag)

    def handle_data(self, data):
        # print("Encountered some data: ", data)
        data = ' '.join(data.split()) 
        
        if len(data)<1:
            return

        if self.addspan and self.handletag:
            if self.include:
                text = ""
                if len(self.file_content)!=0:
                    text = self.file_content.pop()
                text = text +" "+str(data)
                self.file_content.append(text)
        elif self.handletag:
            self.file_content.append(data)
        elif self.heading2 and self.include:
            self.file_content.append("h2-"+str(data))
        elif self.heading1 and self.include:
            self.file_content.append("h1-"+str(data))
            

def parse_html(text):
    '''
        Function to parse the html file.
    '''
    try:
        text = " ".join(text.split("\n"))
        text = " ".join(" ".join(text.split("<i>")).split("</i>"))
        parser = MyHTMLParser()
        parser.feed(text)
        return parser.file_content
    except Exception as e:
        print("Exception occured here.")
        print("Error: ", e)
    finally:
        parser.close()