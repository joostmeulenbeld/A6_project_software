import urllib, urllib2, cookielib

username = 'mithun.martin.215'
password = 'GroupA6_GroupA6'

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = urllib.urlencode({'username' : username, 'j_password' : password})
opener.open('https://www.space-track.org', login_data)
resp = opener.open('https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/2014-01-01--2014-01-02/NORAD_CAT_ID/39428/orderby/TLE_LINE1%20ASC/format/tle')
print resp.read()