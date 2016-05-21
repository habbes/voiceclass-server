
import os, random, string, errno, classes

DATA_DIR = os.environ['DATA_DIR']

def init_class_dirs():
    '''
    creates audio classes directories
    Returns:

    '''
    for classname in classes.CLASSES:
        path = class_dir(classname)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise IOError('Could not create directory: ' + path)


def class_dir(classname):
    '''

    Args:
        classname:

    Returns: the path of the directory for the specified class

    '''
    return os.path.join(DATA_DIR, 'classes', classname)

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
    file = open(os.path.join(class_dir(classname), filename), 'wb')
    file.write(clip)
    file.close()


def train_classifier():
    pass


