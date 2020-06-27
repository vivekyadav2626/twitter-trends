from twitter.models import twitter_available_trends


def get_woeid_from_city_name(city):
    try:
        if city:
            print("[CITY NAME] Requested -> ", city)
            city = city.lower().capitalize()
            print("[CITY NAME] Checking for -> ", city)
            if not city:
                city = 'India'
            output = twitter_available_trends.objects.filter(place=city).values('woeid', 'place', 'country').order_by('woeid')
            print("OUTPUT", output, len(output))
            if len(output) > 0:
                return output[0]['woeid'], output[0]['place'], output[0]['country']
            else:
                return 23424848, "India", "India"
        else:
            return 23424848, "India", "India"
    except Exception as e:
        print("[CITY NAME] Exception Found ->", e)
        return 23424848, "India", "India"
