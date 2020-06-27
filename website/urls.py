from django.conf.urls import url
from django.contrib import admin

from twitter.fetch_and_delete_trends import delete_trends_in_bulk, insert_trends_in_bulk
from twitter.views import twitter_view_trends

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^insert/', insert_trends_in_bulk),
    url(r'^delete/', delete_trends_in_bulk),
    url(r'$', twitter_view_trends)
]
