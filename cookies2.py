import httplib,base64

username = "mithun.martin.215"
password = "GroupA6_GroupA6"
auth = base64.encodestring("%s:%s" % (username, password))
headers = {"Authorization" : "Basic %s" % auth, "User-agent" : "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2"}
conn = httplib.HTTPSConnection("www.space-track.org")
conn.request("GET", "https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/2014-01-01--2014-01-02/NORAD_CAT_ID/39428/orderby/TLE_LINE1%20ASC/format/tle", headers=headers)
response = conn.getresponse()
data = response.read()
print response.status, response.reason
conn.close()