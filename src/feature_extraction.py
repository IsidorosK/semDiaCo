import os, readchar, sklearn.cluster
from pyAudioAnalysis.audioFeatureExtraction import mtFeatureExtractionToFile,mtFeatureExtraction
from pyAudioAnalysis.audioBasicIO import readAudioFile, stereo2mono
from pyAudioAnalysis.audioSegmentation import flags2segs,speakerDiarization,evaluateSpeakerDiarization
from pyAudioAnalysis.audioTrainTest import normalizeFeatures,featureAndTrain
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

        mtFeatureExtractionToFile(input_file, mt_size, mt_step, st_win, st_step, 'testing', False, True, True)

        (mt_feats_norm, MEAN, STD) = normalizeFeatures([mt_feats.T])
        mt_feats_norm = mt_feats_norm[0].T
        features.append(mt_feats_norm)
        # utilities.plot_feature_histograms(features, _, class_names)

        # perform clustering (k = 2)
        n_clusters = 2
        k_means = sklearn.cluster.KMeans(n_clusters=n_clusters)
        k_means.fit(mt_feats_norm.T)
        # print(k_means)
        cls = k_means.labels_
        segs, c = flags2segs(cls, mt_step)  # convert flags to segment limits
        print(segs)
        for sp in range(n_clusters):  # play each cluster's segment
            for i in range(len(c)):
                if c[i] == sp and segs[i, 1] - segs[i, 0] > 1:
                    # play long segments of current speaker
                    print(c[i], segs[i, 0], segs[i, 1])
                    cmd = "avconv -i {} -ss {} -t {} lebron2.wav " \
                          "-loglevel panic -y".format(input_file, segs[i, 0] + 1,
                                                      segs[i, 1] - segs[i, 0] - 1)
                    os.system(cmd)
                    os.system("play lebron2.wav -q")
                    readchar.readchar()

    @staticmethod
    def call_feature_and_train():
        # mt_size, mt_step, st_win, st_step = 1, 0.4, 0.025, 0.010
        mt = 1.0
        st = 0.025
        dir_path = ["../audio/"]
        featureAndTrain(dir_path, mt, mt, st, st, "knn", "diarization")


if __name__ == '__main__':
    feature_object = FeatureExtractor()
    # x = os.listdir('../audio/')
    # for i in x:
    #     print(i)
    # feature_object.extract_mid_features('../audio/Beanie_Feldstein_and_Florence_Pugh.wav')
    feature_object.call_feature_and_train()