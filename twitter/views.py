import datetime

from django.core.paginator import Paginator
from django.shortcuts import render

from twitter.get_info import get_woeid_from_city_name
from twitter.models import twitter_trends_place


def twitter_view_trends(request):
    city_name = request.GET.get('city', None)
    woeid, place, country = get_woeid_from_city_name(city_name)
    print("[MAIN PAGE] LOADING FOR ID ->", woeid, "Place -> ", place, "Country -> ", country)
    search_by_woeid = twitter_trends_place.objects.filter(trend_woeid=woeid).values().order_by('-trend_as_of')
    paginator = Paginator(search_by_woeid, 10)

    tables_final = []
    top_time_list = []
    for page_no in paginator.page_range:
        tables_final_min = []
        for page_obj in paginator.get_page(page_no):
            tables_final_min.append(page_obj)
        if paginator.count > 0:
            top_time_list.append(tables_final_min[0]['trend_created_at'] + datetime.timedelta(hours=5, minutes=30))
        tables_final.append(tables_final_min)

    timenow = datetime.datetime.now()
    final_time = [timenow-now for now in top_time_list]
    all_india_trends_list = ["India", "Thane", "Jaipur", "Patna", "Lucknow", "Nagpur", "Kolkata",  "Hyderabad",
                             "Ahmedabad", "Indore", "Bangalore", "Srinagar", "Surat", "Kanpur", "Mumbai", "Ranchi",
                             "Rajkot", "Delhi", "Chennai", "Amritsar", "Pune", "Bhopal"]
    all_india_trends_list.sort()
    return render(request, "twitter.html", {"trends": tables_final, 'showtime': final_time,
                                                    "all_trend_tables": paginator, "city": place,
                                                    "all_india_trends_list": all_india_trends_list
                                                    })
