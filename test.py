import trainer
import classes

trainer.init_class_dirs()

f = open('data/test-sounds/male-ok.wav', 'rb')
audio = f.read()
f.close()

trainer.classify_audio(audio, classes.MALE_ADULT)