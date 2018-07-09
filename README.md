# youtube_stats
Get 3 custom video statistics ((commentCount / viewCount), (likeCount / viewCount), (likeCount / dislikeCount)) for a list of Youtube channels and returns best x videos according to these stats.

Works with python3.

Usage:

1. create a project, enable Youtube data API v3 for it, and get API key from here : https://console.developers.google.com/apis/credentials?project=_
2. Create a list of Youtube channel ids 
3. Fill in youtube-stats.py with these details and change the published_before and published_after variables
4. Run python3 youtube-stats.py
