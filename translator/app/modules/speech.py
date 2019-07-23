import speech_recognition as sr

def rec():
	r = sr.Recognizer()

	with sr.Microphone() as source:
		audio = r.listen(source)

		try:
			text = r.recognize_google(audio)
			return(text)
		except:
			return("Sorry, couldn't recognize your voice. Please try again.")