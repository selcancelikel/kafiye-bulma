from typing import List
from jpype import JClass, getDefaultJVMPath, shutdownJVM, startJVM
import unicodedata
5
# Zemberek kütüphanesinin yolu
ZEMBEREK_PATH = r'C:\Users\celik\Downloads\zemberek-full.jar'
class ZemberekAnalyzer:
    def __init__(self, zemberek_path: str = ZEMBEREK_PATH):
        self.start_jvm(zemberek_path)
        TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
        self.morphology = TurkishMorphology.createWithDefaults()
        
    def start_jvm(self, zemberek_path: str):
        startJVM(getDefaultJVMPath(), '-ea', f'-Djava.class.path={zemberek_path}')

    def stop_jvm(self):
        shutdownJVM()

    def analyze_word(self, word: str) -> List[str]:
        analysis = self.morphology.analyzeAndDisambiguate(word).bestAnalysis()
        return [(str(a.getLemmas()[0]), str(a.formatLong())) for a in analysis]

def remove_turkish_characters(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
