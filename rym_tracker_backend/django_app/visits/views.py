from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import VisitsLog
from .schemas import RECORD_VISIT_SCHEMA
from .utils import plot_visits, validate_api_key, parse_body, validate_body, get_yesterdays_visits


@method_decorator(csrf_exempt, name='dispatch')
class RecordVisitView(View):
    def get(self, request):
        template = loader.get_template("visits/summary.html")
        visits = get_yesterdays_visits()
        context = {
            "name": "Myles",
            "visits": visits,
            "graph": plot_visits(visits)
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


# [
# { "is_unique": True, "timestamp": "2025-05-06 10:43:29.281973+00:00" },
# { "is_unique": True, "timestamp": "2025-05-06 12:54:37.316145+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 12:54:39.431561+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 12:54:54.901279+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 12:55:07.134670+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 12:55:30.931281+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 12:55:45.661750+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 12:56:19.416202+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.670907+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.787063+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.825267+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.824918+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.863683+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.863463+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.937526+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.906652+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.940945+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.906966+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.906426+00:00" },
# { "is_unique": False, "timestamp": "2025-05-06 13:03:40.852509+00:00" }
# ]

# hours = {
#     0: 0,
#     1: 0,
#     2: 0,
#     3: 0,
#     4: 0,
#     5: 0,
#     6: 0,
#     7: 0,
#     8: 0,
#     9: 0,
#     10: 0,
#     11: 0,
#     12: 0,
#     13: 0,
#     14: 0,
#     15: 0,
#     16: 0,
#     17: 0,
#     18: 0,
#     19: 0,
#     20: 0,
#     21: 0,
#     22: 0,
#     23: 0
# }
