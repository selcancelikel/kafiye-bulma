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
        # NLTK'dan c�mleler alma
        nltk_sentences = nltk.corpus.brown.sents()
        nltk_sentences = [' '.join(sentence) for sentence in nltk_sentences if len(sentence) > 5]

        # HuggingFace'den c�mleler alma
        dataset = load_dataset("ag_news", split='train')
        hf_sentences = [item['text'] for item in dataset]

        # Birle�tirilen c�mleler
        all_sentences = nltk_sentences + hf_sentences
        random.shuffle(all_sentences)

        # "blue" kelimesini i�eren c�mleleri se�me
        color_sentences = [sentence for sentence in all_sentences if "blue" in sentence.lower()]
        emotion_sentences = [sentence.replace("happy", "blue") for sentence in all_sentences if "happy" in sentence.lower()]

        # Veri seti olu�turma
        color_labelled = [(sentence, "color") for sentence in color_sentences]
        emotion_labelled = [(sentence, "emotion") for sentence in emotion_sentences]
        combined_dataset = color_labelled[:500] + emotion_labelled[:500]
        random.shuffle(combined_dataset)

        # Veri setini DataFrame'e �evirme
        df = pd.DataFrame(combined_dataset, columns=['sentence', 'label'])

        return df

    def train_model(self):
        # Veriyi e�itim ve test setlerine ay�rma
        X_train, X_test, y_train, y_test = train_test_split(self.dataset['sentence'], self.dataset['label'], test_size=0.2, random_state=42)

        # Model pipeline'� olu�turma
        self.model = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())
        ])

        # Modeli e�itme
        self.model.fit(X_train, y_train)

        # Test seti �zerinde tahmin yapma
        y_pred = self.model.predict(X_test)

        # Sonu�lar� de�erlendirme
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

    def predict(self, sentences):
        predictions = self.model.predict(sentences)
        for sentence, prediction in zip(sentences, predictions):
            print(f"Sentence: {sentence} -> Prediction: {prediction}")

    def get_dataset(self):
        return self.dataset

# S�n�f� kullanma �rne�i
blue_disambiguation = BlueDisambiguation()
blue_disambiguation.train_model()

# �rnek c�mleler �zerinde tahmin yapma
sample_sentences = [
    "The sky is blue and clear.",
    "He felt blue after the argument.",
    "She wore a blue hat.",
    "Listening to the news made him blue."
]
blue_disambiguation.predict(sample_sentences)

# Veri setinin ilk 10 sat�r�n� g�r�nt�leme
df_full = blue_disambiguation.get_dataset()
print(df_full.head(10))
print("Dataset size:", len(df_full))
