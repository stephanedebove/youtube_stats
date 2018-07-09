# for python3

import urllib.request 
import datetime
import json
import sys
import os

channel_ids=['',''] # List of channel ids you want the stats for
number_of_output_videos=3 # select the top x videos for each stat

api_key='' #create a project, enable Youtube data API v3 for it, and get API key from here : https://console.developers.google.com/apis/credentials?project=_
published_before='2017-08-01T00:00:00Z' # retrieve videos published before this date only. RFC 3339 formatted date-time value (1970-01-01T00:00:00Z). Leave blank for last month
published_after='2017-07-01T00:00:00Z'  # retrieve videos published after this date only. RFC 3339 formatted date-time value (1970-01-01T00:00:00Z). Leave blank for last month

jours_back=-30 # select videos in the last x days. useless if published_after is set

if published_before == '':
	d = datetime.datetime.utcnow() # get time now in UTC
	published_before = d.isoformat("T") + "Z" #transform time in RFC3339

if published_after == '':
	d = datetime.datetime.utcnow() # get time now in UTC
	d = d + datetime.timedelta(days=jours_back) # get time 30 days ago
	published_after = d.isoformat("T") + "Z" #transform time in RFC3339

video_list=[] #list of videos with the requested criteria

for channel_id in channel_ids:
	request='https://www.googleapis.com/youtube/v3/search?part=snippet&channelId='+channel_id+'&type=video&key='+api_key+'&publishedAfter='+published_after+'&publishedBefore='+published_before+'&maxResults=50&order=date' # request to get all videos from this channel published between required dates

	contents = urllib.request.urlopen(request).read() #execute request
	json_data = json.loads(contents) # read json

	for index, video in enumerate(json_data['items']): #for each retrieved video on this channel, we keep only the desired information
		video_list.append( {
			'channelTitle' : video['snippet']['channelTitle'],
			'title' : video['snippet']['title'],
			'videoId' : video['id']['videoId'],
			'publishedAt' : video['snippet']['publishedAt']
		})



all_ids = [key['videoId'] for key in video_list] # keep only ids

all_ids_50_chunks = [all_ids[i:i + 50] for i in range(0, len(all_ids), 50)] # create chunks of 50 ids as it's the limit for the next API request

index=0
for chunk in all_ids_50_chunks:
	string_chunk = ",".join(chunk) # transform list to string

	contents = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/videos?id='+string_chunk+'&key='+api_key+'&part=statistics').read()
	json_data = json.loads(contents)

	for video in json_data['items']: #for each retrieved video we keep only the desired stats
		video_list[index]['viewCount'] = video['statistics']['viewCount']
		video_list[index]['likeCount'] = video['statistics']['likeCount']
		video_list[index]['dislikeCount'] = video['statistics']['dislikeCount']
		if 'commentCount' in video['statistics'] and int(video['statistics']['viewCount']) > 0: # check if video has comments (they can be disabled)
			video_list[index]['commentViewRatio'] = int(video['statistics']['commentCount'])/ int(video['statistics']['viewCount'])
		else:
			video_list[index]['commentViewRatio'] = -1
		if int(video['statistics']['dislikeCount']) > 0: #to avoid division by 0
			video_list[index]['likeDislikeRatio'] = int(video['statistics']['likeCount'])/ int(video['statistics']['dislikeCount'])
		else:
			video_list[index]['likeDislikeRatio'] = -1
		if int(video['statistics']['viewCount']) > 0: #sometimes equals to 0 when video was a live broadcast
			video_list[index]['likeViewPerc'] = 100*int(video['statistics']['likeCount'])/ int(video['statistics']['viewCount'])
		else:
			video_list[index]['likeViewPerc'] = -1

		index += 1



def sort_and_print(stat,texte):
	keep_only = [key[stat] for key in video_list] # keep only the stat we want
	sorted_by = sorted(range(len(keep_only)), key=lambda k: keep_only[k], reverse=True) #sort list from big to small, then returns the index (position) in the original (unsorted) list

	print('\n<strong>Les ' + str(number_of_output_videos) + ' vidéos avec ' + texte + ' sont (sur ' + str(len(video_list)) +' vidéos) :</strong> \n')

	for x in range(number_of_output_videos):

		print(str(video_list[sorted_by[x]][stat]) + ' : <a href="https://www.youtube.com/watch?v=' + video_list[sorted_by[x]]['videoId'] + '">"'+video_list[sorted_by[x]]['title'] + '"</a> par ' + video_list[sorted_by[x]]['channelTitle']) # with html tags to publish directly on the website


number_of_output_videos = min(number_of_output_videos,len(video_list)) # in case there are less retrieved videos than the requested number
sort_and_print('likeViewPerc','le plus grand pourcentage de gens qui ont liké')
sort_and_print('likeDislikeRatio','le plus grand ratio (nb likes / nb dislikes)')
sort_and_print('commentViewRatio','le plus grand ratio (nb commentaires / nb vues)')
	
		





