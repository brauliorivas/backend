from datetime import datetime
from collections import Counter

from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
import requests
import json

from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    print('Endpoint ', url)
    print('Response ', response_dict)

    total_responses = len(response_dict.keys())

    responses = response_dict.values()

    sorted_responses = sorted(responses, key=lambda item: datetime.strptime(item["saved"].replace("\xa0", " ").replace("a.m.", "AM").replace("p.m.", "PM").replace("a. m.", "AM").replace("p. m.", "PM"), "%d/%m/%Y, %I:%M:%S %p"))

    first_response = sorted_responses[0]
    last_response = sorted_responses[-1]

    dates = [
    datetime.strptime(
        item["saved"]
        .replace("\xa0", " ")
        .replace("a.m.", "AM")
        .replace("p.m.", "PM")
        .replace("a. m.", "AM")
        .replace("p. m.", "PM"),
        "%d/%m/%Y, %I:%M:%S %p"
    ).date()
    for item in responses
    ]

    most_common_day, most_common_count = Counter(dates).most_common(1)[0]

    data = {
            'title': 'Landing-Dashboard',
            'total_responses': total_responses,
            'responses': responses,
            'first_response': first_response['saved'],
            'last_response': last_response['saved'],
            'most_common_day': most_common_day
    }

    return render(request, 'main/index.html', data)

