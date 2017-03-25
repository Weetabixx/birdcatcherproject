class browserDetection(object):
    # Check if client browser is Chrome
    def process_request(self, request):
        print "checking browser"
        browser = request.META.get('HTTP_USER_AGENT') # Get client browser
        print browser
        if (('Chrome' in browser) or ('CriOS' in browser)):
            request.chrome = True
            print 'chrome detected'
        else:
            request.chrome = False
        return