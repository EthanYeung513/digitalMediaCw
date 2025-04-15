import praw
import json
from praw.models import MoreComments
import csv


numPostsForSubreddit = 60 
numCommentsForPost = 70 

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent= ""
)


subreddits = ["politics", "worldnews", "nottheonion", "TrueReddit", "geopolitics", "stupidpol"]


def getDataFromSubreddits():
    data = []
    
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            
            for post in subreddit.top(limit=numPostsForSubreddit):
                post_data = {
                    'subreddit': subreddit_name,
                    'postTitle': post.title,
                    'postText': post.selftext,
                    'comments': []
                }
                
                comments = post.comments.list()
                for comment in comments[:numCommentsForPost]:
                    if isinstance(comment, MoreComments):
                        continue
                    
                    post_data['comments'].append({
                        'commentText': comment.body,
                    })  
                data.append(post_data)
            
        except Exception as e:
            print("error for subreddit: " + subreddit_name + str(e))
            continue
    
    return data

def saveToFile(data,csvFile):
    with open(csvFile, 'w', newline='') as csvFile:
        fieldnames = [
            'subreddit', 'postTitle', 'postText','comments'
        ]
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        for post in data:
            post['postText'] 
            listOfComments = []
            for comment in post['comments']:
                commentText = comment['commentText']
                listOfComments.append(commentText)
            post['comments'] = json.dumps(listOfComments)
            
            writer.writerow({
                'subreddit': post['subreddit'],
                'postTitle': post['postTitle'],
                'postText': post['postText'],
                'comments': post['comments']
            })

        

allPostData = getDataFromSubreddits()
saveToFile(allPostData, "PostForAnalysisDataset.csv")
