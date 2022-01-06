import json

class mt_commenter:
    """
    This class handles fetching card data, formatting the Reddit comment, and posting the comment with the API
    """
    def __init__(self, card_name):
        self.comment = ""
        self.cards_file = "saved_cards.json"
        self.card_name = card_name
        self.card_data = self.get_card()
        self.format_comment()

    def get_card(self):
        """
        This function searches the saved_cards.json file for the card with the given name.
        """
        with open(self.cards_file, 'r') as cards_file:
            cards = json.load(cards_file)
            for card in cards:
                if card['Card'] == self.card_name:
                    return card
            return None

    def format_comment(self):
        """
        This function formats the comment to be posted to Reddit.
        """
        if self.card_data is None:
            self.comment = "Card not found."
        else:
            self.comment = "**{}**\n\n".format(self.card_data['Card'])
            self.comment += "**Clan:** {}\n".format(self.card_data['Clan'])
            self.comment += "**Type:** {}\n".format(self.card_data['Type'])
            self.comment += "**Rarity:** {}\n".format(self.card_data['Rarity'])
            self.comment += "**Cost:** {}\n".format(self.card_data['Cost'])
            self.comment += "**CP:** {}\n".format(self.card_data['CP'])
            self.comment += "**ATK:** {}\n".format(self.card_data['ATK'])
            self.comment += "**HP:** {}\n".format(self.card_data['HP'])
            self.comment += "**Description:** {}\n".format(self.card_data['Description'])