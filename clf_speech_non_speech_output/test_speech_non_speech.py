"""
@details: Speech Non-speech discrimination and segmentation (using a trained
speech - non segment classifier)
Important: Need to run speech_non_speech.py first to extract speech non_speech model (stored
in svm_speech_non_speech)
"""
from pyAudioAnalysis.audioSegmentation import mtFileClassification

if __name__ == '__main__':
    au = "/media/vlachos/4e757fbf-09d9-4276-a1f4-af671280a9bb/NCSR-UOP/Multimodal Information Processing and Analysis/audio/speech_non_speech_test.wav"
    gt = "/media/vlachos/4e757fbf-09d9-4276-a1f4-af671280a9bb/NCSR-UOP/Multimodal Information Processing and Analysis/audio/speech_non_speech_test.txt"
    mtFileClassification(au, "svm_speech_non_speech", "svm_rbf", True, gt)
