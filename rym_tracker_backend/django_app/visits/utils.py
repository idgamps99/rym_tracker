import os
import base64
from django.http import JsonResponse
import matplotlib.pyplot as plt
from io import BytesIO
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")


def validate_api_key(request):
    api_key = request.headers.get("x-api-key")
    if api_key != API_KEY:
        return JsonResponse({"error": "Incorrect API key provided"}, status=401)





# MATPLOTLIB GRAPHS
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


def plot_visits():
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.set_xlabel("Time")
    ax.set_ylabel("Visits")
    ax.set_xlim([0, 24])
    ax.set_xticks(list(range(1, 25)))
    ax.set_yticks(list(range(1, 10)))
    graph = get_graph()
    return graph
