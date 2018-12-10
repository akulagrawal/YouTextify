import speech_recognition as sr
from pydub import AudioSegment
import math
import sys
import os
import docx
from download import urlToWav

doc = docx.Document("youtube_list (copy).docx")
idxVid = 1

for para in doc.paragraphs:
	idx = 0
	while para.text[idx] != 'h':
		idx += 1
	url = para.text[idx:]
	videoName = "video" + str(idxVid)
	idxVid += 1
	urlToWav(url,videoName + ".webm")

	orig = AudioSegment.from_wav(videoName + ".wav")
	n = len(orig)
	d = 10000
	m = math.ceil(n/d)
	fullText = ""

	print("0.00%")

	for i in range(0,m):
		temp = orig[i*d:(i+1)*d]
		temp.export("dummy.wav", format="wav")

		# transcribe audio file                                                         
		AUDIO_FILE = "dummy.wav"

		# use the audio file as the audio source                                        
		r = sr.Recognizer()
		with sr.AudioFile(AUDIO_FILE) as source:
			audio = r.record(source)  # read the entire audio file

		try:
			fullText += r.recognize_google(audio)
			fullText += " "
		except:
			fullText += ""
		
		sys.stdout.write('\033[F')
		print(str("{0:.2f}".format(((i+1)/m)*100)) + "%")

	f = open(videoName + ".txt","w")
	f.write(fullText)
	f.close()

if os.path.exists("dummy.wav"):
	os.remove("dummy.wav")