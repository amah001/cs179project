#! twitter/bin/python3

import tweepy
import time, sys, json

# this information should probably be encrypted
access_token = "240097377-zXq4uXzgKnrSYy80JC5OU6hAhhOv9375kYFaQn6G"
access_token_secret = "ik4cVFmbLZcJc78tK8W22oQrciPF7RSxgOMkAZRd1yFXG"
consumer_key = "mqmJvvCHbgr39xmVsIeaJScrG"
consumer_secret = "r2deGcivhRDxVpalFw0JNc4rtYTwemLjhGhRR5TiYXOAnpS8eA"

# modified version of the basic StreamListener from Tweepy
class JSONStream(tweepy.StreamListener):
    def __init__(self, timeLimit, outputFileName):
        self.timeStart = time.time()
        self.timeLimit = 60 * timeLimit
        self.outputFile = open(outputFileName, 'a')
        super(JSONStream, self).__init__()

    def on_status(self, status):
        if (time.time() - self.timeStart) < self.timeLimit:
            self.outputFile.write(json.dumps(status._json) + '\n')
        else:
            self.outputFile.close()
            return False

if __name__ == "__main__":
    # parse command line arguments
    if (len(sys.argv) != 3):
        sys.stderr.write("[Error]: Too few arguments\n")
        sys.stderr.write("Usage: app.py <Time Limit (minutes)> <Output File>\n")
        sys.exit(1)

    TIME_LIMIT = int(sys.argv[1])
    FILENAME = str(sys.argv[2])

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
    jsonstream = JSONStream(outputFileName=FILENAME, timeLimit=TIME_LIMIT)
    stream = tweepy.Stream(auth=api.auth, listener=jsonstream)
    sys.stderr.write("\nCollecting tweets for " + str(TIME_LIMIT) + " minutes... ")
    stream.filter(locations=box)
    sys.stderr.write("Done!\n")
