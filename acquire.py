import urllib2

url = 'https://www.space-track.org'
url2 = 'https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/2014-01-01--2014-01-02/NORAD_CAT_ID/39428/orderby/TLE_LINE1%20ASC/format/tle'
username = 'mithun.martin.215'
password = 'GroupA6_GroupA6'
p = urllib2.HTTPPasswordMgrWithDefaultRealm()

p.add_password(None, url2, username, password)

handler = urllib2.HTTPBasicAuthHandler(p)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

#response = urllib2.urlopen('%s/%s' %(url,url2))

page = urllib2.urlopen(url).read()

