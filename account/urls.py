from django.urls import path

from account.views import BrowserCookiesAPIView, browser_cookies, collect_browser_info, browser_data

urlpatterns =[
    path("browser/cookies/", BrowserCookiesAPIView.as_view(), name="BrowserCookiesAPIView"),
    path("cookies/", browser_cookies, name="browser_cookies"),
    path("browser/data/", browser_data, name="browser_data"),
    path("browser/info/", collect_browser_info, name="collect_browser_info"),
]