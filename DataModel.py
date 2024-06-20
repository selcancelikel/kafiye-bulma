import random
import nltk
from datasets import load_dataset
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

class BlueDisambiguation:
    def __init__(self):
        # Gerekli NLTK veri setlerini indirin
        nltk.download('brown')
        nltk.download('punkt')
        
        # Veri setlerini hazirla
        self.dataset = self.prepare_dataset()

    def prepare_dataset(self):
        # NLTK'dan cümleler alma
        nltk_sentences = nltk.corpus.brown.sents()
        nltk_sentences = [' '.join(sentence) for sentence in nltk_sentences if len(sentence) > 5]

        # HuggingFace'den cümleler alma
        dataset = load_dataset("ag_news", split='train')
        hf_sentences = [item['text'] for item in dataset]

        # Birleþtirilen cümleler
        all_sentences = nltk_sentences + hf_sentences
        random.shuffle(all_sentences)

        # "blue" kelimesini içeren cümleleri seçme
        color_sentences = [sentence for sentence in all_sentences if "blue" in sentence.lower()]
        emotion_sentences = [sentence.replace("happy", "blue") for sentence in all_sentences if "happy" in sentence.lower()]

        # Veri seti oluþturma
        color_labelled = [(sentence, "color") for sentence in color_sentences]
        emotion_labelled = [(sentence, "emotion") for sentence in emotion_sentences]
        combined_dataset = color_labelled[:500] + emotion_labelled[:500]
        random.shuffle(combined_dataset)

        # Veri setini DataFrame'e çevirme
        df = pd.DataFrame(combined_dataset, columns=['sentence', 'label'])

        return df

    def train_model(self):
        # Veriyi eðitim ve test setlerine ayýrma
        X_train, X_test, y_train, y_test = train_test_split(self.dataset['sentence'], self.dataset['label'], test_size=0.2, random_state=42)

        # Model pipeline'ý oluþturma
        self.model = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())
        ])

        # Modeli eðitme
        self.model.fit(X_train, y_train)

        # Test seti üzerinde tahmin yapma
        y_pred = self.model.predict(X_test)

        # Sonuçlarý deðerlendirme
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

    def predict(self, sentences):
        predictions = self.model.predict(sentences)
        for sentence, prediction in zip(sentences, predictions):
            print(f"Sentence: {sentence} -> Prediction: {prediction}")

    def get_dataset(self):
        return self.dataset

# Sýnýfý kullanma örneði
blue_disambiguation = BlueDisambiguation()
blue_disambiguation.train_model()

# Örnek cümleler üzerinde tahmin yapma
sample_sentences = [
    "The sky is blue and clear.",
    "He felt blue after the argument.",
    "She wore a blue hat.",
    "Listening to the news made him blue."
]
blue_disambiguation.predict(sample_sentences)

# Veri setinin ilk 10 satýrýný görüntüleme
df_full = blue_disambiguation.get_dataset()
print(df_full.head(10))
print("Dataset size:", len(df_full))
