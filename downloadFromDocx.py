import docx
from download import urlToWav


def docxListDownload(DocName):
	doc = docx.Document(DocName)
	idxVid = 1
	for para in doc.paragraphs:
		idx = 0
		while para.text[idx] != 'h':
			idx += 1
		url = para.text[idx:]
		videoName = "video" + str(idxVid)
		idxVid += 1
		urlToWav(url,videoName + ".webm")


docxListDownload('youtube_list.docx')