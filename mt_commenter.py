import json

class mt_commenter:
    """
    This class handles fetching item data, formatting the Reddit comment, and posting the comment with the API
    """
    def __init__(self, item_name):
        self.comment = ""
        self.cards_file = "saved_cards.json"
        self.artifacts_file = "saved_artifacts.json"
        self.item_name = item_name
        self.item_type = ""
        self.item_data = self.get_item()
        self.format_comment()

    def get_item(self):
        """
        This function searches the saved_cards.json file for the card with the given name.
        """
        with open(self.cards_file, 'r') as cards_file:
            cards = json.load(cards_file)
            for card in cards:
                if card['Card'].lower() == self.item_name.lower():
                    self.item_type = "Card"
                    return card
        with open(self.artifacts_file, 'r') as artifacts_file:
            artifacts = json.load(artifacts_file)
            for artifact in artifacts:
                if artifact['Artifact'].lower() == self.item_name.lower():
                    self.item_type = "Artifact"
                    return artifact
            return None

    def format_comment(self):
        """
        This function formats the comment to be posted to Reddit.
        """

        # Append the card name to the base url to get it's wiki entry
        baseurl = "https://monster-train.fandom.com/wiki/"

        if self.item_data is None:
            self.comment = "Item not found.\n\n"
        elif self.item_type == "Card":
            self.comment = "**[{}]({})**\n\n".format(self.item_data['Card'], baseurl + self.item_data['Card'].replace(" ", "_"))
            self.comment += "**Clan:** {}  \n".format(self.item_data['Clan'])
            self.comment += "**Type:** {}  \n".format(self.item_data['Type'])
            self.comment += "**Rarity:** {}  \n".format(self.item_data['Rarity'])
            self.comment += "**Cost:** {}  \n".format(self.item_data['Cost'])

            if self.item_data['Type'] != "Spell":
                self.comment += "**CP:** {} || **ATK:** {} || **HP:** {}  \n".format(self.item_data['CP'], self.item_data['ATK'], self.item_data['HP'])
            self.comment += "**Description:** {}\n\n".format(self.item_data['Description'])
        elif self.item_type == "Artifact":
            self.comment = "**[{}]({})**\n\n".format(self.item_data['Artifact'], baseurl + self.item_data['Artifact'].replace(" ", "_"))
            self.comment += "**Clan/Type:** {}  \n".format(self.item_data['Clan/Type'])
            self.comment += "**Source:** {}  \n".format(self.item_data['Source'])
            self.comment += "**DLC:** {}  \n".format(self.item_data['DLC'])
            self.comment += "**Description:** {}\n\n".format(self.item_data['Description'])
    
    def get_comment(self):
        """
        This function returns the formatted comment.
        """
        return self.comment
    
if __name__ == '__main__':
    item_name = "Capricious Reflection"
    item_commenter = mt_commenter(item_name)
    print(item_commenter.get_comment())