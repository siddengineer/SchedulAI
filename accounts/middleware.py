class OrgMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.org = request.user  # user IS the org
        else:
            request.org = None
        return self.get_response(request)