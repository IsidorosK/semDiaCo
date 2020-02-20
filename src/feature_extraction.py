import os, readchar, sklearn.cluster, re
from pyAudioAnalysis.audioFeatureExtraction import mtFeatureExtractionToFile,mtFeatureExtraction
from pyAudioAnalysis.audioBasicIO import readAudioFile, stereo2mono
from pyAudioAnalysis.audioSegmentation import flags2segs, mtFileClassification, speakerDiarization, evaluateSpeakerDiarization
from pyAudioAnalysis.audioTrainTest import normalizeFeatures, featureAndTrain
import utilities


class FeatureExtractor:

    @staticmethod
    def extract_mid_features(input_file):
        class_names = [os.path.basename(input_file)]
        features = []
        fs, x = readAudioFile(input_file)
        x = stereo2mono(x)
        mt_size, mt_step, st_win, st_step = 1, 0.4, 0.025, 0.010
        [mt_feats, st_feats, _] = mtFeatureExtraction(x, fs, mt_size * fs, mt_step * fs,
                                                      round(st_win * fs), round(st_step * fs))

        mtFeatureExtractionToFile(input_file, mt_size, mt_step, st_win, st_step, input_file, False, True, True)
        return mt_feats, st_feats, _

    @staticmethod
    def call_feature_and_train():
        mt = 1.0
        st = 0.025
        dir_path = ["sub_audio/","../audio/silence"]
        featureAndTrain(dir_path, mt, mt, st, st, "knn", "diarization")

    @staticmethod
    def get_classification():
        au = "../audio/Adam_Driver_and_Michael_Shannon.wav"
        gt = "annotated_data/Adam_Driver_and_Michael_Shannon.segments"
        #    au = "../data/musical_genres_small/hiphop/run_dmc_peter_riper.wav"
        mtFileClassification(au, "diarization", "knn", True, gt)


if __name__ == '__main__':
    feature_object = FeatureExtractor()
    audio_path = os.listdir('../audio/')
    pattern = re.compile(r'[A-Za-z].*\.wav$')
    for wav in audio_path:
        if re.match(pattern, wav):
            feature_object.extract_mid_features('../audio/' + wav)
