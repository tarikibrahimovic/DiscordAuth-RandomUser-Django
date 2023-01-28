
from rest_framework.decorators import api_view
import requests
from django.shortcuts import redirect, render
from django.conf import settings
from oauth2_provider.models import AccessToken

def discord_callback(request):
    code = request.GET.get('code')
    data = {
        'client_id': settings.DISCORD_CLIENT_ID,
        'client_secret': settings.DISCORD_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.DISCORD_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    r = requests.post(
        'https://discord.com/api/oauth2/authorize?client_id=1064894318659248280&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2FrandomUser&response_type=token', data=data)

    token_data = r.json()
    access_token = token_data['access_token']
    token, created = AccessToken.objects.get_or_create()
    return redirect('http://127.0.0.1:8000/api/randomUser', token=token.key)


def getAPIData(request):

    codeFromUrl = request.GET.get('code')
    print(codeFromUrl)
    headers = {
        "Authorization": "Bearer " + codeFromUrl
    }

    verify = requests.get(
        "https://discord.com/api/users/@me", headers=headers)

    if codeFromUrl or verify.status_code == 200:
        response = requests.get("https://randomuser.me/api/")
        return render(request, 'hello.html', {'response': response.json()['results'][0]})
    else:
        return redirect('http://127.0.0.1:8000')


@api_view(['GET'])
def authorize(request):
    return redirect('https://discord.com/api/oauth2/authorize?client_id=1064894318659248280&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fapi%2FrandomUser&response_type=code&scope=identify')
