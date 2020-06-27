import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

from twitter.access import get_twitter_api_access
from twitter.models import twitter_available_trends, twitter_trends_place


@api_view(['GET'])
def insert_trends_in_bulk(request):
    try:
        search_by_woeid = twitter_available_trends.objects.filter(country='India').values('woeid').order_by('woeid')
        api = get_twitter_api_access()
        starttime = datetime.datetime.now()
        final_list = []
        for city in search_by_woeid:
            woeidtrend = api.trends_place(city['woeid'])
            created_at = woeidtrend[0]['created_at']
            as_of = woeidtrend[0]['as_of']
            for record in woeidtrend[0]['trends'][:10]:
                record['created_at'] = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                record['as_of'] = datetime.datetime.strptime(as_of, "%Y-%m-%dT%H:%M:%SZ")
                record['woeid'] = city['woeid']
                final_list.append(record)
        bulk_insert_trends(final_list)
        showtime = datetime.datetime.now()
        print("[API] TOTAL TIME TAKEN TO BULK INSERT IS ->", showtime-starttime)
        final_result = {"message": "Success", "count": len(final_list), "timetaken": showtime-starttime}
        return Response(final_result)
    except Exception as e:
        print("[API] BULK INSERT ERROR -> ", e)
        final_result = {"message": "Error", "error": str(e)}
        return Response(final_result)


def bulk_insert_trends(final_list):
    dump_list = []
    for record in final_list:
        bulk = twitter_trends_place(
            trend_name=record['name'],
            trend_url=record['url'],
            trend_query=record['query'],
            trend_count=record['tweet_volume'],
            trend_woeid=record['woeid'],
            trend_created_at=record['created_at'],
            trend_as_of=record['as_of']
            )
        dump_list.append(bulk)

    twitter_trends_place.objects.bulk_create(dump_list)
    print("[API] BULK INSERT DONE -> ", len(dump_list))


@api_view(['GET'])
def delete_trends_in_bulk(request):
    try:
        total_count = twitter_trends_place.objects.count()
        if total_count > 5000:
            starttime = datetime.datetime.now()
            delete_count = total_count - 5000
            output = twitter_trends_place.objects.filter(id__in=twitter_trends_place.objects.all().order_by('id').values_list('id')[:delete_count]).delete()
            result = True
            showtime = datetime.datetime.now()
            print("[API] BULK DELETE DONE -> ", result, output)
            final_result = {"message": "Success", "count": output[0], "timetaken": showtime-starttime}
            return Response(final_result)
        else:
            result = False
            print("[API] BULK DELETE DONE -> ", result)
            final_result = {"message": "No change", "count": total_count}
            return Response(final_result)
    except Exception as e:
        print("[API] BULK DELETE ERROR -> ", e)
        final_result = {"message": "Error", "error": str(e)}
        return Response(final_result)
