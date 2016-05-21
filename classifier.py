
import os, random, string, errno, classes

DEFAULT_DATA_DIR = os.environ['DATA_DIR']


def random_filename():
    '''

    Returns: random string with .csv extension

    '''
    return ''.join(random.sample(string.ascii_lowercase + string.digits, 20)) + '.wav'


class Classifier(object):
    def __init__(self, data_dir=DEFAULT_DATA_DIR, class_names=classes.CLASSES):
        self.data_dir = data_dir
        self.class_names = class_names
        self.init_dirs()

    def class_dir(self, class_name):
        return os.path.join(self.data_dir, 'classes', class_name)

    def init_dirs(self):
        for class_name in self.class_names:
            path = self.class_dir(class_name)
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise IOError('Could not create directory: ' + path)

    def classify_audio(self, audio, class_name):
        filename = random_filename()
        file_path = os.path.join(self.class_dir(class_name), filename)
        file = open(file_path, 'wb')
        file.write(audio)
        file.close()
        return filename, file_path
