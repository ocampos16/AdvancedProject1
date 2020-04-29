import json

# new_files_list = ['tweets_climatechange_06-03-2020', 'tweets_fridaysforfuture_09-03-2020', 'tweets_savetheplanet_09-03-2020']
new_files_list = ['tweets_fridaysforfuture_09-03-2020_test', 'tweets_climatechange_06-03-2020_test', 'tweets_savetheplanet_09-03-2020_test']

new_files_list[0]
# We load the url of the first file.
url = "Results/" + new_files_list[0] + ".json"

# JSON file
f = open (url, "r")

# Reading from file
data = json.loads(f.read())

print()