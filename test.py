from classifier import Classifier
import classes

def audio(name):
    f = open('data/test-sounds/' + name + '.wav', 'rb')
    content = f.read()
    f.close()
    return content

me = audio('me');
maleOk = audio('male-ok')
maleGoodbye = audio('male-goodbye')
maleNotScare = audio('male-notscare')
femaleActUnprod = audio('female-activity_unproductive')


classifier = Classifier()
classifier.classify_audio(maleGoodbye, classes.MALE_ADULT)
classifier.classify_audio(maleNotScare, classes.MALE_ADULT)
classifier.classify_audio(femaleActUnprod, classes.FEMALE_ADULT)
classifier.train()
print classifier.detect_class(me)