import hotshot, hotshot.stats
import os, sys
import logging
import cStringIO
from django.conf import settings

def pre_hotshot():
    tmpfile = os.tempnam()
    prof = hotshot.Profile(tmpfile)
    return tmpfile, prof


def post_hotshot(tmpfile, prof):
    prof.close()
    
    out = cStringIO.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    
    pstats = hotshot.stats.load(tmpfile)
    #stats.strip_dirs()
    pstats.sort_stats('time', 'calls')
    pstats.print_stats()
    
    sys.stdout = old_out
    os.remove(tmpfile)
            
    return out.getvalue()

class ProfileMiddleware(object):
    def process_request(self, request):
        if settings.DEBUG and request.has_key('prof'):
            self.tmpfile,  self.prof = pre_hotshot()

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and request.has_key('prof'):
            return self.prof.runcall(callback, request, *callback_args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and request.has_key('prof'):
            stats_str = post_hotshot(self.tmpfile, self.prof)
            #from django.utils.html import escape
            #if response and response.content and stats_str:
            #    response.content = "<pre>" + stats_str + "</pre>"
            #logging.debug(escape(stats_str))
            x = file('/tmp/profile.txt', 'w')
            x.write( stats_str )
            #print stats_str
        return response

def hotshot_viewer(view_func):
    def _check_viewer(request, *args, **kwargs):
        if not request.session.get('supervisor'):
            return view_func(request, *args, **kwargs)
        tmpfile, prof = pre_hotshot()
        
        result = prof.runcall(view_func, request, *args, **kwargs)

        stats_str = post_hotshot(tmpfile, prof)
        logging.debug(stats_str)        
        return result
        
    return _check_viewer