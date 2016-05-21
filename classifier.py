import os, random, string, errno, classes
from pyAudioAnalysis import audioTrainTest as trainer

DEFAULT_DATA_DIR = os.environ['DATA_DIR']


def random_filename():
    '''

    Returns: random string with .csv extension

    '''
    return ''.join(random.sample(string.ascii_lowercase + string.digits, 20)) + '.wav'

def makedir(dir):
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e


class Classifier(object):
    def __init__(self, data_dir=DEFAULT_DATA_DIR, class_names=classes.CLASSES):
        self.data_dir = data_dir
        self.class_names = class_names
        self.class_dir_dict = {}
        self.class_dir_list = []
        self.temp_dir = ''
        self.classifier_dir = ''
        self.classifier_path = ''
        self.classifier_type = 'knn'    #using svm brings an error
        self.classifier_name = 'VoiceGenderAgeClassifier'
        self.init_dirs()

    def class_dir(self, class_name):
        return os.path.join(self.data_dir, 'classes', class_name)

    def init_dirs(self):
        # create dirs for different classes
        for class_name in self.class_names:
            path = self.class_dir(class_name)
            self.class_dir_dict[class_name] = path
            self.class_dir_list.append(path)
            makedir(path)

        # create dir for classifier
        self.classifier_path = os.path.join(self.data_dir, 'classifier', self.classifier_name)
        makedir(os.path.dirname(self.classifier_path))

        # create temp dir for unclassified audio
        self.temp_dir = os.path.join(self.data_dir, 'unclassified')
        makedir(self.temp_dir)

    def classify_audio(self, audio, class_name):
        filename = random_filename()
        file_path = os.path.join(self.class_dir_dict[class_name], filename)
        file = open(file_path, 'wb')
        file.write(audio)
        file.close()
        return filename, file_path

    def train(self):
        trainer.featureAndTrain(
            listOfDirs=self.class_dir_list,
            mtWin=1.0,
            mtStep=1.0,
            stWin=trainer.shortTermWindow,
            stStep=trainer.shortTermStep,
            classifierType=self.classifier_type,
            modelName=self.classifier_path
        )

    def detect_class(self, audio):
        filename, path = self.save_unclassified(audio)
        res = trainer.fileClassification(
            inputFile=path,
            modelName=self.classifier_path,
            modelType=self.classifier_type
        )
        return filename, res

    def save_unclassified(self, audio):
        filename = random_filename()
        path = os.path.join(self.temp_dir, filename)
        file = open(path, 'wb')
        file.write(audio)
        file.close()
        return filename, path

