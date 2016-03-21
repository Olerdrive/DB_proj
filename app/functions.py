import urlparse
from flask import request


def get_json(request):
    return urlparse.parse_qs(urlparse.urlparse(request.url).query)


def get_related(request):
    try:
        related = request["related"]
    except Exception:
        related = []
    return related


def get_optional(request, values):
    return dict([(i, request[i]) for i in set(values) if i in request])


def check(params, required_params):
    for item in required_params:
        if item not in params:
            raise Exception("missing " + item)
        if params[item] is not None:
            try:
                params[item] = params[item]
            except Exception:
                continue
    return