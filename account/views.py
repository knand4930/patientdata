import json

import requests
from django.core import signing
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class BrowserCookiesAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        print( request.data)
        return Response(status=status.HTTP_200_OK)



def browser_cookies(request):
    resp = requests.get("http://google.com")
    cookies_data = resp.cookies._cookies
    print(cookies_data, "cookies_data")


    cookies = request.COOKIES
    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    ip_address = request.META.get('REMOTE_ADDR', 'unknown')
    language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'unknown')
    encoding = request.META.get('HTTP_ACCEPT_ENCODING', 'unknown')
    referer = request.META.get('HTTP_REFERER', 'unknown')
    connection = request.META.get('HTTP_CONNECTION', 'unknown')
    try:
        signed_email = request.COOKIES.get("user_email_signed")
        email = signing.loads(signed_email) if signed_email else "unknown"
    except signing.BadSignature:
        email = "tampered or invalid"

    context = {
        "cookies": cookies,
        "user_agent": user_agent,
        "ip_address": ip_address,
        "language": language,
        "encoding": encoding,
        "referer": referer,
        "connection": connection,
        "email": email,
    }

    # print(context, "get contenct")

    return render(request, "home.html", context)





from .browser_utils import (list_extensions, get_user_profile, get_autofill,
                            get_downloads, get_saved_passwords, get_bookmarks,
                            get_browsing_history)  # Assume these are in a separate module

def browser_data(request):
    context = {
        "extensions": list_extensions(),
        "profile": get_user_profile(),
        "autofill": get_autofill(),
        "downloads": get_downloads(),
        "passwords": get_saved_passwords(),
        "bookmarks": get_bookmarks(),
        "history": get_browsing_history(limit=10),
    }
    print(context, "get all data !!")

    return render(request, "browser_data.html", context)



def collect_browser_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Received frontend browser info:", data)
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)