class browserDetection(object):
    
    # Check if client browser is Chrome
    def process_request(self, request):
        
        # Get client browser
        browser = request.META.get('HTTP_USER_AGENT')
        if (('Chrome' in browser) or ('CriOS' in browser)):
            request.chrome = True
        else:
            request.chrome = False
        return