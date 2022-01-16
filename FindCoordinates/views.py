from django.http import JsonResponse, HttpResponse
import requests
import json
from xml.dom import minidom
import xml.etree.ElementTree as xmldata
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def find_coordinates_view(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode('utf-8'))    
        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
        API_KEY = 'Enter your API key'
        params = {
            'address': post_data['address'],
            'key':API_KEY
        }
        
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        
        result = res['results'][0]
        geodata = dict()
        geodata['coordinates']={
            'lat' : result['geometry']['location']['lat'],
            'lng' : result['geometry']['location']['lng']
            }
        geodata['address'] = result['formatted_address']

        # If the flag is set to json
        if post_data['output_format']=="json":
            return JsonResponse(geodata)

        # If the flag is set to xml
        elif post_data['output_format']=="xml":
            root = xmldata.Element("root")

            m1 = xmldata.Element("address")
            root.append (m1)
            m1.text=geodata['address']

            m2 = xmldata.Element("coordinates")
            c1 = xmldata.SubElement(m2, "lat")
            c1.text = str(geodata['coordinates']['lat'])
            c2 = xmldata.SubElement(m2, "lng")
            c2.text = str(geodata['coordinates']['lng'])
            root.append (m2)

            tree = xmldata.ElementTree(root)
            xmlstr = minidom.parseString(xmldata.tostring(root)).toprettyxml(indent="   ")
            return HttpResponse(xmlstr)

        # If the flag is not in json or xml format    
        else:
            return HttpResponse("Invalid Output Format")

    