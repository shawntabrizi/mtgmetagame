from bs4 import BeautifulSoup
import urllib
import html
import re

def getAllMetagameDecks ():
    metagameURL = "https://www.mtggoldfish.com/metagame/modern/full"
    htmlFile = urllib.request.urlopen(metagameURL)
    rawHTML = htmlFile.read()
    soup = BeautifulSoup(rawHTML, "html.parser")

    decks = soup.findAll('div', attrs={'class':'archetype-tile'})

    deckURLs = []

    htmloutput = ""

    htmloutput += "<!DOCTYPE html><html><head><title>Deck Lists</title>" + "\n"
    htmloutput += "<style>"
    htmloutput += """
                    @page {
                      size: 5.5in 8.5in;
                    }

                    div {
                        width: 250px;
                        max-width: 250px;
                        display:inline-block;
                        float: left;
                        margin-left: 10px;
                    }

                    h1 {
                        margin-bottom: 0;
                        margin-top: 0;
                        font-family: Arial, Helvetica, sans-serif;
                        font-size: 20px;
                    }
                    h2 {
                        margin-bottom: 0;
                        margin-top: 0;
                        font-size: 14px;
                    }

                    p {
                        margin-bottom: 0;
                        margin-top: 0;
                        font-family: Arial, Helvetica, sans-serif;
                        font-size: 10px;
                    }"""
    htmloutput += "</style>"
    htmloutput += "</head><body>" + "\n"

    for deck in decks:
        deckList = deck.find('a', attrs={'class':'card-image-tile-link-overlay'})
        deckListURL = deckList['href']
        deckURLs.append(deckListURL)

    for deckURL in deckURLs:
        deckURL = urllib.parse.urljoin('https://www.mtggoldfish.com', deckURL)
        deckHTML = urllib.request.urlopen(deckURL)
        rawDeckHTML = deckHTML.read()
        deckSoup = BeautifulSoup(rawDeckHTML, "html.parser")

        htmloutput += "<div>" + "\n"

        deckName = deckSoup.find('h2', attrs={'class':'deck-view-title'}).contents[0].strip()
        deckStats = deckSoup.find('p', attrs={'class':None}).text
        deckPercent = re.search('([0-9]*\.?[0-9]+)[%]', deckStats).group(1)
        deckPercent = round(float(deckPercent))

        #print(deckName, deckPercent)

        htmloutput += "<h1>" + deckName + ", " + str(deckPercent) + "%</h1>" + "\n"

        archetypeDetails = deckSoup.find('div', attrs={'class':'archetype-details'})

        archtypeBreakdownSections = archetypeDetails.findAll('div', attrs={'class':'archetype-breakdown-section'})
        for section in archtypeBreakdownSections:
            sectionTitle = section.find('h4').text
            #print(sectionTitle)

            htmloutput += "<h2>" + sectionTitle + "</h2>" + "\n"

            featuredCards = section.findAll('div', attrs={'class':'archetype-breakdown-featured-card'})
            for card in featuredCards:
                cardImage = card.find('img', attrs={'class':'price-card-image-image'})
                cardName = cardImage.get('alt','')

                cardInfo = card.find('p', attrs={'class':'archetype-breakdown-featured-card-text'}).text
                cardQuant = re.search('(\d+)[x]',cardInfo).group(1)
                cardFreq = re.search('(\d+)[%]',cardInfo).group(1)
                #print(cardName, cardQuant, cardFreq)

                if(cardFreq == '100'):
                    htmloutput += "<p><b>" + cardQuant + " " + cardName + "</b> " + cardFreq + "%</p>" + "\n"
                else:
                    htmloutput += "<p>" + cardQuant + " " + cardName + " " + cardFreq + "%</p>" + "\n"


            cardTable = section.find('table')
            cardTableRows = cardTable.findAll('tr')
            for row in cardTableRows:
                cardQuant = row.find('td', attrs={'class':'deck-col-qty'}).text.strip()
                cardFreq = row.find('td', attrs={'class':'deck-col-frequency'}).text.strip()
                if(row.find('a')):
                    cardName = row.find('a').text.strip()
                else:
                    cardName = row.find('td', attrs={'class': None}).text
                
                cardName = re.search('([^(]+)',cardName).group(1).strip()
                cardQuant = re.search('(\d+)[x]',cardQuant).group(1)
                cardFreq = re.search('(\d+)[%]',cardFreq).group(1)
                
                #print(cardName, cardQuant, cardFreq)
                
                if(cardFreq == '100'):
                    htmloutput += "<p><b>" + cardQuant + " " + cardName + "</b> " + cardFreq + "%</p>" + "\n"
                else:
                    htmloutput += "<p>" + cardQuant + " " + cardName + " " + cardFreq + "%</p>" + "\n"
        htmloutput += "</div>" + "\n"
    
    htmloutput += "</body></html>"
    
    f = open('decks.html', 'w')
    f.write(htmloutput)
    f.close()
