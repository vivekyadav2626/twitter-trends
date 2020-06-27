from twitter.access import get_twitter_api_access
from twitter.models import twitter_available_trends


def save_trends_available_to_database(record):
    b = twitter_available_trends(place=record['name'],
                                 placetype_code=record['placeType']['code'],
                                 placetype_name=record['placeType']['name'],
                                 parentid=record['parentid'],
                                 country=record['country'],
                                 woeid=record['woeid'],
                                 countrycode=record['countryCode'])
    b.save()
    print("DONE", record)


# To get all available trends provided by twitter and save to database.
def get_trends_available(api):
    all_trends = api.trends_available()
    for record in all_trends:
        save_trends_available_to_database(record)
    return True


if __name__ == '__main__':
    api = get_twitter_api_access()
    get_trends_available(api)
