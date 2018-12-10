from __future__ import unicode_literals
import youtube_dl


def urlToWav(url, name):

	ydl_opts = {
		'format': 'bestaudio/best',
    	'postprocessors': [{
        	'key': 'FFmpegExtractAudio',
        	'preferredcodec': 'wav',
        	'preferredquality': '192',
    	}],
    	'outtmpl' : name,
    	'keepvideo' : True
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])