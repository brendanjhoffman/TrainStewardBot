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
                if card['Card'].lower() == self.card_name.lower():
                    return card
            return None

    def format_comment(self):
        """
        This function formats the comment to be posted to Reddit.
        """
        if self.card_data is None:
            self.comment = "Card not found.\n\n"
        else:
            self.comment = "**{}**\n\n".format(self.card_data['Card'])
            self.comment += "**Clan:** {}  \n".format(self.card_data['Clan'])
            self.comment += "**Type:** {}  \n".format(self.card_data['Type'])
            self.comment += "**Rarity:** {}  \n".format(self.card_data['Rarity'])
            self.comment += "**Cost:** {}  \n".format(self.card_data['Cost'])

            if self.card_data['Type'] != "Spell":
                self.comment += "**CP:** {} || **ATK:** {} || **HP:** {}  \n".format(self.card_data['CP'], self.card_data['ATK'], self.card_data['HP'])
            self.comment += "**Description:** {}\n\n".format(self.card_data['Description'])
        self.comment += "------------------------------------------------------  \n"
        self.comment += "^^Questions? ^^Visit ^^/r/TrainStewardBot ^^- ^^Call ^^cards ^^with ^^[[CARDNAME]]"

    
    def get_comment(self):
        """
        This function returns the formatted comment.
        """
        return self.comment
    
if __name__ == '__main__':
    card_name = "Most Blessed Sword"
    card_commenter = mt_commenter(card_name)
    print(card_commenter.get_comment())