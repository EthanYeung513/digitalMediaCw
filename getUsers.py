import praw
import csv

credentials = praw.Reddit(
    user_agent="",
    client_id="",
    client_secret=""
)


subredditName = "nottheonion"
subreddit = credentials.subreddit(subredditName)

UsersAndTheirCount = {}


for post in subreddit.new(limit=100000000):
    author = post.author
    if author:
        if author.name in UsersAndTheirCount:
            UsersAndTheirCount[author.name] += 1
        else:
            UsersAndTheirCount[author.name] = 1

filterByMinPosts = 2
activeUsers = {}
for currentUser, count in UsersAndTheirCount.items():
    if count >= filterByMinPosts:
        activeUsers[currentUser] = count

with open( subredditName + "_users.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Username", "NumOfPosts"])
    for currentUser, count in activeUsers.items():
        writer.writerow([currentUser, count])
