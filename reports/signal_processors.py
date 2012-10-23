from geopy import geocoders

g = geocoders.Google('AIzaSyAZoNPSlRTETltbmJvgYYqol0SLAVBgKs')

def save_point_for_location(sender, **kwargs):
    instance = kwargs['instance']
    if instance.geometry == None:
        location_found = True
        try:
            (place, point) = g.geocode(instance.location)
        except:
            location_found = False
            print "location not found for instance %s" % instance.id
        if location_found:
            instance.geometry = "POINT (%s %s)" % (point[1], point[0])
            instance.save()
        print "saving point for location on %s" % instance.name
