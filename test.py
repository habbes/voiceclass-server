from classifier import Classifier
import classes

f = open('data/test-sounds/male-ok.wav', 'rb')
audio = f.read()
f.close()

classifier = Classifier()
classifier.classify_audio(audio, classes.MALE_ADULT)