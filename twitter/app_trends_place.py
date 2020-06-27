import datetime

from twitter.models import twitter_trends_place


def save_trends_place_to_database(record):
    b = twitter_trends_place(trend_name=record['name'],
                                 trend_url=record['url'],
                                 trend_query=record['query'],
                                 trend_count=record['tweet_volume'],
                                 trend_woeid=record['woeid'],
                                 trend_created_at=record['created_at'],
                                 trend_as_of=record['as_of']
                                 )
    b.save()
    print("DONE", record)


# To get trends for specific place
def get_trends_place(api, woeid):
    woeidtrend = api.trends_place(woeid)
    created_at = woeidtrend[0]['created_at']
    as_of = woeidtrend[0]['as_of']
    for record in woeidtrend[0]['trends'][:10]:
        record['created_at'] = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        record['as_of'] = datetime.datetime.strptime(as_of, "%Y-%m-%dT%H:%M:%SZ")
        record['woeid'] = woeid
        save_trends_place_to_database(record)
