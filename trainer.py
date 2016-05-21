
import os, random, string, errno, classes
from pyAudioAnalysis import audioTrainTest as at

DATA_DIR = os.environ['DATA_DIR']

def init_class_dirs():
    '''
    creates audio classes directories
    Returns:

    '''
    for classname in classes.CLASSES:
        path = os.path.join(DATA_DIR, 'classes', classname)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise IOError('Could not create directory: ' + path)



def random_filename():
    '''

    Returns: random string with .csv extension

    '''
    return ''.join(random.sample(string.ascii_lowercase + string.digits, 15)) + '.wav'

def classify_audio(clip, classname):
    '''

    Args:
        clip: content of the audio clip in WAV format
        audio_class: name of the class as found in the classes module

    Returns:

    '''
    filename = random_filename()
    file = open(os.path.join(DATA_DIR, classname, filename), 'wb')
    file.write(clip)
    file.close()


def train_classifier():
    pass


