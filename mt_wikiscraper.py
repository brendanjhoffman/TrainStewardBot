from bs4 import BeautifulSoup
import requests
import json
import re

class mt_wiki_reader:
    """
    This class handles reading, parsing, and saving cards from the MonsterTrain Fandom wiki.
    """
    def __init__(self):
        self.cards_url = 'https://monster-train.fandom.com/wiki/Cards'
        self.cards_file = 'saved_cards.json'
        self.cards_list = []

    def update_cards(self):
        """
        This function updates the saved_cards.json file with the latest cards from the wiki using BeautifulSoup.
        """

        # Scrape data from the wiki using BeautifulSoup
        cards_page = requests.get(self.cards_url)
        cards_soup = BeautifulSoup(cards_page.text, 'html.parser')

        # Find the table of cards, then the rows of the table
        cards_table = cards_soup.find('table', {'class': 'wikitable sortable floatheader'})
        cards_rows = cards_table.find_all('tr')

        # Iterate through the rows of the table
        for card in cards_rows:
            card_fields = ["Card", "Description", "Clan", "Type", "Rarity", "Cost", "CP", "ATK", "HP"]
            card_data = card.find_all('td')
            card = {}

            # Iterate through the fields (wiki columns) of the card
            for data, field in zip(card_data, card_fields):
                # If the field is an image, then replace it with the image's alt text
                # The accepted_text array lists the alt text of the images that are accepted in order to not print/save unit images (e.g. "Hornbreaker_Prince.png") 
                for img in data.find_all('img'):
                    accepted_text = ['Attack', 'Health', 'Capacity', 'Ember']
                    if img['alt'] in accepted_text:
                        img.replace_with(img.get('alt'))

                # Clean description card text
                cardText = data.text.strip()
                if field == "Description":
                    numbersInDescription = re.findall("\d+", cardText)
                    for number in numbersInDescription:
                        cardText = cardText.replace(number, number + " ")

                    cardText = cardText.replace(" .", ".")
                    cardText = cardText.replace(".", ". ")
                    cardText = cardText.replace("  ", " ")
                    cardText = cardText.strip()

                # Add the field to the card dictionary
                card.update({field: cardText})

            # Add the card to the list of cards
            # The next line removes the first "card", which is a result of the table header
            if(card != {}):
                self.cards_list.append(card)
                
        # Save the cards to a json file
        with open(self.cards_file, 'w', encoding='utf-8') as cards_file:
            cards_file.write(json.dumps(self.cards_list, indent = 4))

if __name__ == '__main__':
    reader = mt_wiki_reader()
    reader.update_cards()