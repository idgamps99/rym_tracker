import os
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from jsonschema import validate, ValidationError
from .models import VisitsLog
from .schemas import RECORD_VISIT_SCHEMA
from .utils import plot_visits, validate_api_key


load_dotenv()
API_KEY = os.getenv("API_KEY")


@method_decorator(csrf_exempt, name='dispatch')
class RecordVisitView(View):
    def get(self, request):
        template = loader.get_template("visits/summary.html")
        visits = VisitsLog.objects.all()
        context = {
            "name": "Myles",
            "visits": visits,
            "graph": plot_visits
        }
        return HttpResponse(template.render(context))


    def post(self, request):
        validate_api_key(request)
        api_key = request.headers.get("x-api-key")
        if api_key != API_KEY:
            return JsonResponse({"error": "Incorrect API key provided"}, status=401)

        try:
            parsed_body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Malformed JSON body"}, status=400)

        try:
            validate(instance=parsed_body, schema=RECORD_VISIT_SCHEMA)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

        timestamp = timezone.now()
        VisitsLog.objects.create(is_unique=parsed_body["isUnique"], timestamp=timestamp)
        print("hell yeah motherfucker")
        return HttpResponse("Visit recorded", status=201)
