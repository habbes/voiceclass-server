import os, random, string, errno, classes, hashlib
from pyAudioAnalysis import audioTrainTest as trainer

DEFAULT_DATA_DIR = os.environ['DATA_DIR']


def wav_filename(name):
    return name + '.wav'


def file_hash(data):
    return ''.join(random.sample(string.ascii_lowercase + string.digits, 20))
    # return hashlib.sha256(data).hexdigest()  #this causes errors in training classifier


def makedir(path):
    try:
        os.makedirs(path)
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
        self.classifier_type = 'knn'    # using svm brings an error
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
        file_id = file_hash(audio)
        file_path = os.path.join(self.class_dir_dict[class_name], wav_filename(file_id))
        with open(file_path, 'wb') as f:
            f.write(audio)

        return file_id, file_path

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
        file_id, path = self.save_unclassified(audio)
        detected = trainer.fileClassification(
            inputFile=path,
            modelName=self.classifier_path,
            modelType=self.classifier_type,
        )
        res = {
            'id': file_id,
            'class': detected[2][0],
            'probability': detected[1][0]
        }
        return res

    def unclassified_path(self, file_id):
        return os.path.join(self.temp_dir, wav_filename(file_id))

    def save_unclassified(self, audio):
        file_id = file_hash(audio)
        path = self.unclassified_path(file_id)
        with open(path, 'wb') as f:
            f.write(audio)
        return file_id, path

    def classify_unclassified(self, file_id, class_name):
        path = self.unclassified_path(file_id)
        with open(path, 'rb') as f:
            audio = f.read()
            return self.classify_audio(audio, class_name)

