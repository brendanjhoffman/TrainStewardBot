import praw
import time
import re
from mt_commenter import mt_commenter

class mt_redditor:
    """
    This class initializes the Reddit API and replies to comments
    """

    def __init__(self, username, password, client_id, client_secret):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.subreddit = "MonsterTrain"
        self.reddit = self.init_reddit()
        self.done_comments = []

    def init_reddit(self):
        """
        This function initializes the Reddit API
        """
        try:
            return praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                password=self.password,
                user_agent='MonsterTrain item Bot by u/BrendanH117',
                username=self.username
            )
        except Exception as e:
            print(e)
            return None
    
    def reply_to_comment(self, comment, items):
        """
        This function replies to a comment with the item's data
        """
        reply = ""
        for item_name in items:
            item_commenter = mt_commenter(item_name)
            reply += item_commenter.get_comment()
            reply += "\n\n"
        reply += "------------------------------------------------------  \n"
        reply += "^^Questions? ^^Ping ^^user ^^BrendanH117 ^^- ^^Call ^^items ^^with ^^[[ITEMNAME]]"
        comment.reply(reply)

    def get_new_comments(self):
        """
        This function returns an array of new comments
        """
        comments = self.reddit.subreddit(self.subreddit).comments(limit=250)
        new_comments = []
        for comment in comments:
            if comment.author != self.reddit.user.me() and comment.id not in self.done_comments:
                new_comments.append(comment)
        return new_comments

    def run(self):
        """
        This function runs the bot and checks for new comments
        """
        
        # Load the list of comments already replied to
        try:
            with open('done_comments.txt', 'r') as done_comments_file:
                self.done_comments = done_comments_file.read().split('\n')
        except FileNotFoundError:
            pass

        while True:
            new_comments = self.get_new_comments()
            for comment in new_comments:
                print("Reading Comment ID: {} from User: {}".format(comment.id, comment.author))
                try:
                    regex = '\[\[(.*?)\]\]'
                    body = comment.body.replace('\\', '')
                    items = re.findall(regex, body)
                    if len(items) > 0:
                        self.reply_to_comment(comment, items)
                        self.done_comments.append(comment.id)
                        print("Success: Added items {}".format(items))
                    else:
                        print("No item name found")
                except Exception as e:
                    print("!!!Failed - Reason: {}!!!".format(e))
                time.sleep(10)
            
            # Write the done comments to a file
            with open('done_comments.txt', 'w') as done_comments_file:
                for comment in self.done_comments:
                    done_comments_file.write(comment + '\n')
            
            time.sleep(60)

if __name__ == '__main__':
    """
    Read the config file and run the bot
    """
    try:
        with open('.env', 'r') as config_file:
            config = config_file.read().split('\n')
            username = config[0].split('=')[1]
            password = config[1].split('=')[1]
            client_id = config[2].split('=')[1]
            client_secret = config[3].split('=')[1]
    except FileNotFoundError:
        print("Config file not found. Please create a .env file with the following format:")
        print("username=<username>\npassword=<password>\nclient_id=<client_id>\nclient_secret=<client_secret>")
        exit()
    
    try:
        mt_redditor = mt_redditor(username, password, client_id, client_secret)
        if mt_redditor.reddit is None:
            print("Error initializing Reddit API")
            exit()
        mt_redditor.run()
    except Exception as e:
        print(e)
        exit()
    except KeyboardInterrupt:
        print("\nExiting...")