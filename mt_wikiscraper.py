from bs4 import BeautifulSoup
import requests
import json

class mt_wiki_reader:
    """
    This class handles reading, parsing, and saving cards from the MonsterTrain wiki.
    """
    def __init__(self):
        self.cards_url = 'https://monster-train.fandom.com/wiki/Cards'
        self.cards_file = 'saved_cards.json'
        self.cards_list = []
        self.update_cards()

    def update_cards(self):
        """
        This function updates the saved_cards.json file with the latest cards from the wiki using BeautifulSoup.
        """
        # Get the cards from the wiki
        cards_page = requests.get(self.cards_url)
        cards_soup = BeautifulSoup(cards_page.text, 'html.parser')

        cards_table = cards_soup.find('table', {'class': 'wikitable sortable floatheader'})
        cards_rows = cards_table.find_all('tr')
        for card in cards_rows:
            card_fields = ["Card", "Description", "Clan", "Type", "Rarity", "Cost", "CP", "ATK", "HP"]
            card_data = card.find_all('td')
            card = {}
            for data, field in zip(card_data, card_fields):
                for img in data.find_all('img'):
                    accepted_text = ['Attack', 'Health', 'Capacity', 'Ember']
                    if img['alt'] in accepted_text:
                        img.replace_with(img.get('alt'))
                card.update({field: data.text.strip()})
            self.cards_list.append(card)
            #print(card)

        # Save the cards to a json file
        with open(self.cards_file, 'w', encoding='utf-8') as cards_file:
            cards_file.write(json.dumps(self.cards_list))

mt = mt_wiki_reader()