import os
import json
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import VisitsLog
from .schemas import RECORD_VISIT_SCHEMA
from .utils import plot_visits, validate_api_key, parse_body, validate_body


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
        invalid_key = validate_api_key(request)
        if invalid_key:
            return invalid_key

        parsed_body, parse_err = parse_body(request)
        if parse_err:
            return parse_err

        validate_err = validate_body(parsed_body, RECORD_VISIT_SCHEMA)
        if validate_err:
            return validate_err

        VisitsLog.objects.create(
            is_unique=parsed_body["isUnique"],
            timestamp=timezone.now()
            )
        print("hell yeah motherfucker")
        return HttpResponse("Visit recorded", status=201)
