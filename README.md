# TrainStewardBot
A card fetcher bot for Monster Train.

## Usage
In the r/MonsterTrain subreddit, use [[CARDNAME]] to retrieve data from the bot. If running this bot for yourself or as a template for another, you'll need an .env file with your Reddit Client ID, Secret, Username, and Password.

## How It Works
This repo contains four components: saved_cards.json, mt_wikiscraper, mt_commenter and mt_redditor.

##### saved_cards.json
This is a JSON file that the bot reads from. This should be updated regularly using mt_wikiscraper.

##### mt_wikiscraper.py
This scrapes and parses https://monster-train.fandom.com/wiki/Cards for data. Cards get saved to saved_cards.json.

##### mt_commenter.py
This formats the reply comment given a card name.
Initialize by using `comment = mt_commenter("Hornbreaker Prince")`
Then retrieve the comment with `formatted_comment = comment.get_comment()`

##### mt_redditor.py
This initializes praw, reads the latest 250 comments every minute, and replies to any comments that meets the following
`comment.replace('\\', '').split('[[')[1].split(']]')[0]`
This is the main file to run
