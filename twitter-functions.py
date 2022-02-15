def validate_twitter(consumer_key, consumer_secret, access_key, access_secret):
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_key, access_secret)

  api = tweepy.API(auth)

  return api

def sort_tweets_by_time_chunk(input_df, column_name='Date', time_chunk="week"):
    for x in range(52):
      df = input_df[input_df[column_name].dt.isocalendar().week == x]
      print(df.count)
      # Only make folders and files for weeks where there were tweets
      if not df.empty:
        if not os.path.exists(f'week-{x}'):
          os.makedirs(f'week-{x}')
        df.to_csv(f'week-{x}/{screen_name}.csv')

# get an arbitrary # of tweets
def get_tweets(screen_name, num, api):
    new_tweets = api.user_timeline(screen_name=screen_name, count=num)
    
    return new_tweets


def get_all_tweets(screen_name, api):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name,
                                       count=200,
                                       max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f"...{len(alltweets)} tweets downloaded so far")

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text]
                 for tweet in alltweets]
                 
    # Transposed in the repl.it
    tweets_df = pd.DataFrame(outtweets,
                             columns=["Tweet_id", "Date", "Tweet_Text"])
    
    # TODO: incorporate this start to error handling
    # except BaseException as e:
    #       print('failed on_status', str(e))
    #       time.sleep(3)

  # For each week in the year, create dir if ! exists, filter df, write to csv, and save to folder
  # See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.weekofyear.html  
    '''
    for x in range(52):
      df = tweets_df[tweets_df['Date'].dt.isocalendar().week == x]
      print(df.count)
      # Only make folders and files for weeks where there were tweets
      if not df.empty:
        if not os.path.exists(f'week-{x}'):
          os.makedirs(f'week-{x}')
        df.to_csv(f'week-{x}/{screen_name}.csv')
    '''
    return tweets_df

    
# If using datetime object, can use this function to get the week for an individual tweet
# Note that every python data type handles this slightly differently! Check the type!
def make_chunks(data, tuple_position=1):
  # 0 = year, 1 = week, 2 = day
  weeks = []
  for x in data:
    chunk = x.created_at.isocalendar()[tuple_position]
    weeks.append(chunk)
  return weeks

# #tweets
# tweets = pd.read_csv('bored_tweets.csv')

# #remove links
# no_links = tweets[~tweets.text.str.contains("http")]
# no_links.head()

# # only tweets
# just_tweets = no_links.text

# # make everything a string
# text = str(just_tweets)


#api = validate_twitter(consumer_key, consumer_secret, access_key, access_secret)
#test = get_all_tweets('BoredElonMusk', api)
#print(test)