import base64
import os
import json
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
from django.http import JsonResponse
from dotenv import load_dotenv
from io import BytesIO
from jsonschema import validate, ValidationError
from .models import VisitsLog


load_dotenv()
API_KEY = os.getenv("API_KEY")


def validate_api_key(request):
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return JsonResponse({"error": "Incorrect API key provided"}, status=401)
    return None


def parse_body(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Malformed JSON body"}, status=400)


def validate_body(body, schema):
    try:
        validate(instance=body, schema=schema)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    return None

# MATPLOTLIB GRAPHS
def get_yesterdays_visits():
    yesterday = date.today() - timedelta(2) # 2 days ago temporarily
    return VisitsLog.objects.filter(timestamp__date=yesterday)


def set_hours():
    return {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
    11: 0,
    12: 0,
    13: 0,
    14: 0,
    15: 0,
    16: 0,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
    21: 0,
    22: 0,
    23: 0
}

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()
    plt.close()
    return graph


def plot_visits(visits):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.set_xlabel("Time")
    ax.set_ylabel("Visits")
    ax.set_xlim([0, 24])
    ax.set_xticks(list(range(1, 25)))
    ax.set_yticks(list(range(1, visits.count())))
    hours = set_hours()
    for visit in visits:
        hours[visit.timestamp.hour] += 1

    plt.bar(hours.keys(), hours.values())
    graph = get_graph()
    return graph
