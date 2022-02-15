### DRAFT Collection Object
import requests
import pandas as pd

class DataCollection():
  def __init__(self, token, output_columns=["id", "post_date", "author", "content"]):
        self.token = token
        self.output_columns = output_columns
  def make_df(self, input_arr):
    df = pd.DataFrame(self, input_arr, columns=self.output_columns)
    return df
  def help(self, service=None):
    message = "This will be a spot to outline the various functions and required bits for each service. Pass arg 'service=' for help with specific services"
    # Match is not yet implemented in Colab. Sad day.
    '''
    match service:
            case ‘discord’ : message += "Discord requires a BOT token"
    '''
    if service == 'discord':
      message += '\n Discord requires a BOT token'
    elif service == "twitter":
      message += '\n Twitter requires a BEARER token'
    return message

class TwitterCollection(DataCollection):
  # NOTES: Twitter's requests are formatted such that you need to look up the user id first.
  def get_user(self, screen_name):
    headers = {"Authorization": f"Bearer {self.token}"}
    req = requests.get(f'https://api.twitter.com/2/users/by/username/{screen_name}', headers=headers)
    return req
    
  def get_tweets(self, user_id, num):
    #tweets_list = (screen_name=screen_name, count=num)
    #req = requests.get( )
    headers = {"Authorization": f"Bearer {self.token}"}
    req = requests.get(f'https://api.twitter.com/2/users/{user_id}/tweets', headers=headers) 
    return req
  
class DiscordCollection(DataCollection):
  def get_channel_messages(self, channel, before=None, after=None, around=None, count=None):
    headers = {"Authorization": f"Bot {self.token}"}
    count = count if count else 100
    before = f'&before={before}' if before else ""
    after = f'&after={after}' if after else ""
    around = f'&around={around}' if around else ""
    channel_path = f'https://discord.com/api/channels/{channel}/messages?&limit={count}'
    allmessages = []
    try:
        new_messages = requests.get(channel_path, headers=headers).json() 
        allmessages.extend(new_messages)
        print(len(allmessages))
        #save the id of the oldest tweet less one
        oldest = int(allmessages[-1]['id']) - 1
        print(int(len(allmessages)) < count)
        #keep grabbing messages until there are no messages left to grab
        if int(len(allmessages)) < count:
          while len(new_messages) > 0:
              print(len(new_messages))
              print(f"getting messages before {oldest}")
              channel_path = f'https://discord.com/api/channels/{channel}/messages?limit={count}&before={oldest}'
              new_messages = requests.get(channel_path, headers=headers).json() 

              allmessages.extend(new_messages)

              print(f"...{len(allmessages)} messages downloaded so far")

              try:
                  oldest = int(allmessages[-1]['id']) - 1
              except:
                  print("Done")
                  break
          print(len(allmessages))
        return allmessages
    except Exception as e: print(f'Error: {e}')

  def get_user_messages(self, user, before=None, after=None, around=None, count=None):
    # Should return messages from a specific user
    pass

  def make_arr(self, messages):
      message_arr = [{m['id'], m['timestamp'], m['author']['username'], m['content']} for m in messages]
      return message_arr


class KaggleCollection(DataCollection):
  pass

class RedditCollection(DataCollection):
  pass

class SlackCollection(DataCollection):
  pass
