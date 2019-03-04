from django.http import HttpResponse, HttpResponseBadRequest
from .service import services

def search(request):
  results = []

  if len(request.GET) == 0:
    return HttpResponse('A Custom GeoCoding Service Based on Google and HERE\'s'+ 
                        ' GeoCoding Services', content_type='text/plain')

  searchText = request.GET.get('q', '')
  if len(searchText) == 0:
    return HttpResponseBadRequest()

  for service in services:
    try:
      results = service.get(searchText)
      if len(results) > 0:
        return HttpResponse(results, content_type='application/json')
    except Exception as e:
      raise Exception ("Error in service request: %r" %e)  

  return HttpResponse('Some error - either in input address or processing- '+
                      'has happend, please try again')
