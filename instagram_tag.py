import urllib2
import json
import datetime
import pandas as pd
from pandas import DataFrame


client_id = "INSERT CLIENT ID HERE"
tag = "nofilter"
count = 100
iterations = 1500 	# will output about 50,000 entries, change if needed
df = DataFrame()

url = 'https://api.instagram.com/v1/tags/%s/media/recent/?client_id=%s&count=%s' % (tag, client_id, count)

for i in xrange(iterations):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	data = json.loads(response.read())
	df = df.append(data["data"],ignore_index=True)
	if 'next_url' not in data["pagination"].keys():
		break
	url = data["pagination"]["next_url"]

df["caption"] = df["caption"].apply(lambda x: '' if x is None else x["text"].replace(',',''))
df["comments"] = df["comments"].apply(lambda x: x["count"])
df["created_time"] = df["created_time"].apply(lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'))
df["likes"] = df["likes"].apply(lambda x: x["count"])

ordered_df = df[["caption","likes","comments","created_time","filter","type","link"]]
ordered_df.to_csv(str(tag) + "_instagram.csv",encoding='utf-8', index=False)