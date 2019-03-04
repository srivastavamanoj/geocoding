'''
*** GeoCoding Service Using Google and HERE's Geocoding API ****
1. A custom Geocoding Service is created using Google and HERE Geocoding Services. 
   This API does a free-form address lookup and produces lattitude and longitude 
   of the address. 
2. For the sake of brevity other geocoding services such as specific viewport, 
   intersection address, etc are not implemented.
3. It uses GoogleService primarily, and HERE as a backup service.
4. Code creates an abstract baseclass "BaseService" and we derive GoogleService and 
   HereService from it which implement url fetching () and output json file parsing.
5. You need to create your own API_KEY in case of Google Service and API_ID and 
   API_CODE in case HERE Service.  
'''

from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen, URLError
import json

class BaseService(object):
  def create_search_url(self, searchtext):
    raise NotImplementedError

  def get_output_lnglat(self, response):
    raise NotImplementedError

  def get(self, searchText):
    searchUrl = self.create_search_url(searchText)

    try:
      response = urlopen(searchUrl, timeout=3)
    except URLError as e:
      raise Exception("Error in urlopen: %r" % e)

    try:
      outputJson = json.loads(response.read())
    except ValueError as e:
      raise LoadError(e)

    lnglat = self.get_output_lnglat(outputJson)
    return lnglat 

class GoogleService(BaseService):
  def __init__(self, apiKey):
    self.baseurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
    self.apiKey = apiKey
    self.errorMsgs = {
      'ZERO_RESULTS'    : 'Geocode was successful but returned no results; possibly request address is non-existent',
      'OVER_DAILY_LIMIT': 'Any of the following may have occured'
                          '-- Missing or invalid API key'
                          '-- Billing is not been enabled on your account.'
                          '-- Self-imposed usage cap has been exceeded. '
                          '-- Provided method of payment is no longer valid',
       'OVER_QUERY_LIMIT': 'You are over your quota',
       'REQUEST_DENIED'  : 'Your request was denied',
       'INVALID_REQUEST' : 'Wrong query - address, components or latlng - is missing.',
       'UNKNOWN_ERROR'   : 'Unknown server error, please try again',
    }

  def create_search_url(self, searchText):
    searchParams= {
      'address': searchText,
      'sensor': 'false',
      'key': self.apiKey,
    }
    searchUrl = self.baseurl + urlencode(searchParams, quote_via=quote_plus)
    print ('search url: ', searchUrl)
    return searchUrl 

  def get_output_lnglat(self, response):
    out = []
    if response['status']=='OK':
      for result in response['results']:
        out.append({'lat': result['geometry']['location']['lat']})
        out.append({'lng': result['geometry']['location']['lng']})
      return out 
    else:
      raise Exception('Google Geocoding Service: %s' % self.errorMsgs[response['status']])

class HereService(BaseService):
  def __init__(self, appId, appCode):
    self.baseurl = 'https://geocoder.api.here.com/6.2/geocode.json?'
    self.appId = appId
    self.appCode = appCode

  def create_search_url(self, searchText):
    searchParams = {
      'searchtext': searchText,
      'app_id': self.appId,
      'app_code': self.appCode,
    }
    searchUrl = self.baseurl + urlencode(searchParams, quote_via=quote_plus)
    print ('search url: ', searchUrl)
    return searchUrl 

  def get_output_lnglat(self, response):
    out = []
    try:
      for view in response['Response']['View']: 
        for result in view['Result']:
          out.append({'lat': result['Location']['DisplayPosition']['Latitude']})
          out.append({'lng': result['Location']['DisplayPosition']['Longitude']})
      return out     
    except KeyError:
      raise Exception('HERE Geocoding Service: could not parse lattitude/longitude in output json file')

services=[
  GoogleService(apiKey ='AIzaSyCMr0liqqd4vKfYwOEVmHJ8oVSMt1anaYA'),
  HereService(appId='22QyFApiUkAJVvQLfhRN',appCode='9MyblSWINxPZ7BPNwmxS4A'),
]
