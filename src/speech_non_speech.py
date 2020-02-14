"""
details: Train a speech-non speech classifier, don't forget to change paths
"""
from audioTrainTest import featureAndTrain

if __name__ == '__main__':
    mt = 1.0
    st = 0.05
    dir_paths = ["/media/vlachos/4e757fbf-09d9-4276-a1f4-af671280a9bb/NCSR-UOP/Multimodal Information Processing and Analysis/audio/speech_music/speech/",
"/media/vlachos/4e757fbf-09d9-4276-a1f4-af671280a9bb/NCSR-UOP/Multimodal Information Processing and Analysis/audio/speech_music/non_speech"]
    featureAndTrain(dir_paths, mt, mt, st, st, "svm_rbf", "svm_speech_non_speech")
