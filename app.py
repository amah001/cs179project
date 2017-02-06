import tweepy
import time, sys, json
import os, errno

#opens keys
file = open("key.txt", "r")
key_lines = file.readlines()
file.close()

# accesses keys
access_token=key_lines[0].rstrip()
access_token_secret=key_lines[1].rstrip()
consumer_key=key_lines[2].rstrip()
consumer_secret=key_lines[3].rstrip()

hundredMB=1024 * 1000 * 100

# modified version of the basic StreamListener from Tweepy
class JSONStream(tweepy.StreamListener):
    def __init__(self, timeLimit):
        self.timeStart = time.time()
        self.timeLimit = 60 * timeLimit
        super(JSONStream, self).__init__()

    def on_status(self, status):
        global f, fileCount
        if (time.time() - self.timeStart) < self.timeLimit:
            if f.tell() > hundredMB:
                f.close()
                fileCount += 1
                outputPath = "data/tweets_" + str(fileCount) + ".json"
                f = open(outputPath, 'a')
            f.write(json.dumps(status._json) + '\n')
        else:
            f.close()
            return False

    def on_error(self, status_code):
        sys.stderr.write("[Error] - Unable to process tweets, " + str(status_code) + '\n')
        f.close()
        return False

# create directory for data files
try:
    os.makedirs("data")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

# setup output files
fileCount = 0
outputPath = "data/tweets_" + str(fileCount) + ".json"
f = open(outputPath, 'a')

# parse command line arguments
if (len(sys.argv) != 2):
    sys.stderr.write("[Error]: Too few arguments\n")
    sys.stderr.write("Usage: app.py <Time Limit (minutes)>\n")
    sys.exit(1)

TIME_LIMIT = int(sys.argv[1])


# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# gather current trends in the US
#rawTrends = api.trends_place(id=2442047)
#trends = list()
#sys.stderr.write("Currently trending topics:\n")
#for trend in rawTrends[0]["trends"]:
#    trends.append(trend["name"])
#    sys.stderr.write("\t> " + trend["name"] + "\n")

# bounding box
box = [-125.0011, 24.9493, -66.9326, 49.5904]

# gather tweets until time runs out
jsonstream = JSONStream(timeLimit=TIME_LIMIT)
stream = tweepy.Stream(auth=api.auth, listener=jsonstream)

print("Collecting tweets for " + str(TIME_LIMIT) + " minutes...")
stream.filter(locations=box)
print("Done!")
