class browserDetection(object):
    # Check if client browser is Chrome
    def process_request(self, request):
        browser = request.META.get('HTTP_USER_AGENT') # Get client browser
        if (('Chrome' in browser) or ('CriOS' in browser)):
            request.chrome = True
        else:
            request.chrome = False
        return