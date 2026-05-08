import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# =====================================================
# HUMAN-LIKE SAFETY DATASET
# labels: safe, warning, danger
# =====================================================

data = [
    # SAFE messages
    ("I reached home safely", "safe"),
    ("I am at college with my friends", "safe"),
    ("Everything is fine here", "safe"),
    ("I am going to the library", "safe"),
    ("I am travelling with my family", "safe"),
    ("I am safe, no problem", "safe"),
    ("I just reached the hostel", "safe"),
    ("I am with my classmates", "safe"),
    ("I am waiting near the main gate", "safe"),
    ("I am in a public place and everything is okay", "safe"),
    ("I am going for lunch with my friends", "safe"),
    ("I am on my way home and feeling okay", "safe"),
    ("I am in class right now", "safe"),
    ("Sab thik hai", "safe"),
    ("Main safe hu", "safe"),
    ("Main ghar pahunch gayi hu", "safe"),
    ("Main friends ke saath hu", "safe"),
    ("No issue, I am okay", "safe"),
    ("I am inside the campus", "safe"),
    ("I am at a safe location", "safe"),

    # WARNING messages
    ("I feel uncomfortable here", "warning"),
    ("A stranger is staring at me", "warning"),
    ("Someone is walking behind me", "warning"),
    ("This place feels unsafe", "warning"),
    ("The cab driver changed the route", "warning"),
    ("I am alone and the road is empty", "warning"),
    ("A person is following me from a distance", "warning"),
    ("I feel nervous in this area", "warning"),
    ("The driver is asking personal questions", "warning"),
    ("Someone is making me uncomfortable", "warning"),
    ("I am not sure if this place is safe", "warning"),
    ("It is dark and I am alone", "warning"),
    ("A group of boys are staring at me", "warning"),
    ("Mujhe thoda unsafe feel ho raha hai", "warning"),
    ("Koi mujhe dekh raha hai", "warning"),
    ("Driver route change kar raha hai", "warning"),
    ("Main akeli hu aur road empty hai", "warning"),
    ("Mujhe yaha comfortable feel nahi ho raha", "warning"),
    ("Someone is behaving strangely near me", "warning"),
    ("I think someone is watching me", "warning"),

    # DANGER messages
    ("Someone is following me and I feel unsafe", "danger"),
    ("Please help me, I am in danger", "danger"),
    ("I am being chased", "danger"),
    ("Someone is trying to force me", "danger"),
    ("A man is following me closely", "danger"),
    ("I am scared, please send help", "danger"),
    ("I need urgent help", "danger"),
    ("Someone grabbed my hand", "danger"),
    ("I am trapped and cannot leave", "danger"),
    ("I feel like I am in serious danger", "danger"),
    ("The driver is not stopping the cab", "danger"),
    ("Someone is threatening me", "danger"),
    ("I am being harassed", "danger"),
    ("Help me immediately", "danger"),
    ("Mujhe bachao", "danger"),
    ("Koi mera peecha kar raha hai", "danger"),
    ("Main danger me hu", "danger"),
    ("Please jaldi help bhejo", "danger"),
    ("Mujhe bahut darr lag raha hai", "danger"),
    ("Driver cab nahi rok raha hai", "danger"),
    ("Kisi ne mera haath pakad liya", "danger"),
    ("Koi mujhe zabardasti le ja raha hai", "danger"),
    ("Main phas gayi hu help chahiye", "danger"),
    ("Someone is trying to harm me", "danger"),
    ("I am not safe please call someone", "danger"),
    ("Emergency please help", "danger"),
    ("SOS I need help now", "danger"),
]

df = pd.DataFrame(data, columns=["message", "label"])

X = df["message"]
y = df["label"]


# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# =====================================================
# MODEL PIPELINE
# Word + character ngrams help with spelling mistakes and Hinglish
# =====================================================

model = Pipeline([
    ("features", FeatureUnion([
        ("word_tfidf", TfidfVectorizer(
            lowercase=True,
            analyzer="word",
            ngram_range=(1, 2),
            max_features=6000
        )),
        ("char_tfidf", TfidfVectorizer(
            lowercase=True,
            analyzer="char_wb",
            ngram_range=(3, 5),
            max_features=6000
        ))
    ])),
    ("classifier", LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    ))
])


# =====================================================
# TRAIN MODEL
# =====================================================

model.fit(X_train, y_train)


# =====================================================
# EVALUATE MODEL
# =====================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# =====================================================
# SAVE MODEL
# =====================================================

with open("threat_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nThreat detection model saved successfully as threat_model.pkl")