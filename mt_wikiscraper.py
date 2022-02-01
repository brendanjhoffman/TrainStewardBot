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
        self.artifacts_url = 'https://monster-train.fandom.com/wiki/Artifacts'
        self.artifacts_file = 'saved_artifacts.json'
        self.artifacts_list = []

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
                    accepted_text = ['Attack', 'Health', 'Capacity', 'Ember', 'X Cost', 'Echo', 'Echo Slot', 'Gold']
                    if img['alt'] in accepted_text:
                        img.replace_with(img.get('alt'))

                # Clean description card text
                cardText = data.text.strip()
                if field == "Description":
                    cardText = re.sub(r'(?<=\d)(?=[^\d\sx%])|(?<=[^\d\s+-])(?=\d)', ' ', cardText)
                    cardText = cardText.replace(" .", ".")
                    cardText = cardText.replace(".", ". ")
                    cardText = cardText.replace("  ", " ")
                    cardText = cardText.strip()

                # Add the field to the card dictionary
                card.update({field: cardText})

            # Add the card to the list of cards
            # The next line removes the first "card", which is a result of the table header
            if(card != {}):
                print("Adding card: " + card['Card'])
                self.cards_list.append(card)
                
        # Save the cards to a json file
        with open(self.cards_file, 'w', encoding='utf-8') as cards_file:
            cards_file.write(json.dumps(self.cards_list, indent = 4))
    
    def update_artifacts(self):
        """
        This function updates the saved_artifacts.json file with the latest artifacts from the wiki using BeautifulSoup.
        """

        # Scrape data from the wiki using BeautifulSoup
        artifacts_page = requests.get(self.artifacts_url)
        artifacts_soup = BeautifulSoup(artifacts_page.text, 'html.parser')

        # Find the table of artifacts, then the rows of the table
        artifacts_table = artifacts_soup.find_all('table', {'class': 'wikitable sortable floatheader'})[1] # Index 1 is the main table of artifacts, index 0 is the divine artifacts
        artifacts_rows = artifacts_table.find_all('tr')

        # Iterate through the rows of the table
        for artifact in artifacts_rows:
            artifact_fields = ["Artifact", "Description", "Clan/Type", "Source", "DLC"]
            artifact_data = artifact.find_all('td')
            artifact = {}

            # Iterate through the fields (wiki columns) of the artifact
            for data, field in zip(artifact_data, artifact_fields):

                # If the field is an image, then replace it with the image's alt text
                # The accepted_text array lists the alt text of the images that are accepted in order to not print/save unit images (e.g. "Hornbreaker_Prince.png") 
                for img in data.find_all('img'):
                    accepted_text = ['Attack', 'Health', 'Capacity', 'Ember', 'X Cost', 'Echo', 'Echo Slot', 'Gold']
                    if img['alt'] in accepted_text:
                        img.replace_with(img.get('alt'))

                # Clean description card text
                cardText = data.text.strip()
                if field == "Description":
                    cardText = re.sub(r'(?<=\d)(?=[^\d\sx%])|(?<=[^\d\s+-])(?=\d)', ' ', cardText)
                    cardText = cardText.replace(" .", ".")
                    cardText = cardText.replace(".", ". ")
                    cardText = cardText.replace("  ", " ")
                    cardText = cardText.strip()
        
                # Add the field to the artifact dictionary
                artifact.update({field: cardText})
            # Add the artifact to the list of artifacts
            # The next line removes the first "artifact", which is a result of the table header
            if(artifact != {}):

                # Add an empty string for Source and DLC since they are not present on Divine cards
                if "Source" not in artifact:
                    artifact.update({"Source": ""})
                    artifact.update({"DLC": ""})

                print("Adding artifact: " + artifact['Artifact'])
                self.artifacts_list.append(artifact)

        # Save the artifacts to a json file
        with open(self.artifacts_file, 'w', encoding='utf-8') as artifacts_file:
            artifacts_file.write(json.dumps(self.artifacts_list, indent = 4))

if __name__ == '__main__':
    reader = mt_wiki_reader()
    reader.update_cards()
    reader.update_artifacts()