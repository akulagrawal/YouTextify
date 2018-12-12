from pydub import AudioSegment
import math
import sys
import os
import docx
import json
from download import urlToWav

doc = docx.Document("youtube_list.docx")
idxVid = 1

for para in doc.paragraphs:
	idx = 0
	while para.text[idx] != 'h':
		idx += 1
	url = para.text[idx:]
	videoName = "video" + str(idxVid)
	idxVid += 1
	urlToWav(url,videoName + ".webm", 'wav')

	orig = AudioSegment.from_wav(videoName + ".wav")
	n = len(orig)
	d = 1000000
	m = math.ceil(n/d)
	fullText = ""

	for i in range(0,m):
		print("Slot " + str(i+1) + " of " + str(m))
		if i < m-1:
			temp = orig[i*d:(i+1)*d]
		else:
			temp = orig[i*d:]
		temp.export("dummy.flac", format="flac")

		text = os.system("curl -X POST -u \"apikey:API_KEY\" \
						  --header \"Content-Type: audio/flac\" \
						  --data-binary @/home/akul/Desktop/Fathom/dummy.flac \
						  \"URL/v1/recognize\" \
						  > dummy.json")			# Enter your API_KEY and URL for Speech to Text IBM API
		with open('dummy.json', 'r') as outfile:
			data = json.load(outfile)
			n = len(data['results'])
			s = ""
			for i in range(0,n):
				s += data['results'][i]['alternatives'][0]['transcript'] + " "
			fullText += s

		#sys.stdout.write('\033[F')

		f = open(videoName + ".txt","w")
		f.write(fullText)
		f.close()

if os.path.exists("dummy.wav"):
	os.remove("dummy.wav")