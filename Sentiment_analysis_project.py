import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer ,SnowballStemmer

# Load the dataset
data = pd.read_csv("Womens Clothing E-Commerce Reviews.csv")

# List of columns to remove
columns_to_remove = ['number of reviews','Title','Clothing ID', 'Age', 'Division Name', 'Department Name', 'Class Name']

# Drop the specified columns
data.drop(columns_to_remove, axis=1, inplace=True)

# Preprocessing the Review Text column
def preprocess_text(text):
    # Check if text is a string
    if isinstance(text, str):
        # Convert text to lowercase
        text = text.lower()

        # # Remove special characters and digits
        # text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize the text
        tokens = word_tokenize(text)
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        stemmer1 = PorterStemmer()  # Initialize Porter stemmer
        stemmed_tokens1 = [stemmer1.stem(word) for word in filtered_tokens]  # Stem tokens

        stemmer2 = SnowballStemmer(language='english')  # Initialize Porter stemmer
        stemmed_tokens2 = [stemmer2.stem(word) for word in filtered_tokens]  # Stem tokens
        # Join tokens back into text
        processed_text = ' '.join(stemmed_tokens2)
        return processed_text
    else:
        return ""  # Return an empty string if text is not a string

# Apply preprocessing to the Review Text column
data['Review Text'] = data['Review Text'].apply(preprocess_text)

# Print the modified dataset
print(data.head())

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Define features (X) and target (y)
X = data['Review Text']
y = data['Rating'].apply(lambda x: 1 if x > 3 else 0)  # Convert ratings to binary sentiment labels

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data to TF-IDF features
tfidf_vectorizer = TfidfVectorizer(max_features=2000)  # You can adjust the max_features parameter as needed
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", int(accuracy * 100), '%')

# Example of testing new text reviews with the trained model

# Define a function for preprocessing new text reviews
def preprocess_new_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # Stem tokens using the Snowball stemmer
    stemmer = SnowballStemmer(language='english')
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    # Join tokens back into text
    processed_text = ' '.join(stemmed_tokens)
    return processed_text

# Example of new text reviews
new_reviews = [
    "This dress is amazing, I love it!",
    "The quality of this product is very poor.",
    "the fit is bad",
    "i dont like it",
    "not worth it",
    "not hight quality",
    "not how i imagined"
]

# Preprocess the new text reviews
preprocessed_reviews = [preprocess_new_text(review) for review in new_reviews]

# Convert preprocessed text to TF-IDF features
X_new_tfidf = tfidf_vectorizer.transform(preprocessed_reviews)

# Use the trained model to predict the sentiment of the new reviews
predictions = model.predict(X_new_tfidf)

# Print the predictions
for review, prediction in zip(new_reviews, predictions):
    sentiment = "Positive" if prediction == 1 else "Negative"
    print("Review:", review)
    print("Predicted Sentiment:", sentiment)
    print()


# import pandas as pd
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import SnowballStemmer
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.svm import SVC
# from sklearn.metrics import accuracy_score

# # Load the dataset
# data = pd.read_csv("Womens Clothing E-Commerce Reviews.csv")

# # List of columns to remove
# columns_to_remove = ['number of reviews', 'Title', 'Clothing ID', 'Age', 'Division Name', 'Department Name', 'Class Name']

# # Drop the specified columns
# data.drop(columns_to_remove, axis=1, inplace=True)

# # Preprocessing the Review Text column
# def preprocess_text(text):
#     # Check if text is a string
#     if isinstance(text, str):
#         # Convert text to lowercase
#         text = text.lower()
#         # Tokenize the text
#         tokens = word_tokenize(text)
#         # Remove stopwords
#         stop_words = set(stopwords.words('english'))
#         filtered_tokens = [word for word in tokens if word not in stop_words]
#         # Stem tokens using the Snowball stemmer
#         stemmer = SnowballStemmer(language='english')
#         stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
#         # Join tokens back into text
#         processed_text = ' '.join(stemmed_tokens)
#         return processed_text
#     else:
#         return ""  # Return an empty string if text is not a string or NaN

# # Apply preprocessing to the Review Text column
# data['Review Text'] = data['Review Text'].apply(preprocess_text)

# # Drop rows with empty strings in the 'Review Text' column
# data = data[data['Review Text'] != ""]

# # Define features (X) and target (y)
# X = data['Review Text']
# y = data['Rating'].apply(lambda x: 1 if x > 3 else 0)  # Convert ratings to binary sentiment labels

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Convert text data to TF-IDF features
# tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust the max_features parameter as needed
# X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
# X_test_tfidf = tfidf_vectorizer.transform(X_test)

# # Define models and parameter grids for grid search
# models = [
#     {
#         'name': 'Logistic Regression',
#         'model': LogisticRegression(),
#         'params': {'C': [0.001, 0.01, 0.1, 1, 10, 100]}
#     },
#     {
#         'name': 'Decision Tree',
#         'model': DecisionTreeClassifier(),
#         'params': {'max_depth': [None, 5, 10, 20]}
#     },
#     {
#         'name': 'Random Forest',
#         'model': RandomForestClassifier(),
#         'params': {'n_estimators': [50, 100, 200]}
#     },
#     {
#         'name': 'SVM',
#         'model': SVC(),
#         'params': {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf']}
#     }
# ]

# # Perform grid search for each model
# for model_info in models:
#     print(f"Training {model_info['name']}...")
#     grid_search = GridSearchCV(model_info['model'], model_info['params'], cv=5, scoring='accuracy')
#     grid_search.fit(X_train_tfidf, y_train)
#     best_model = grid_search.best_estimator_
#     best_params = grid_search.best_params_
#     print(f"Best parameters: {best_params}")
#     # Evaluate the best model on the test set
#     y_pred = best_model.predict(X_test_tfidf)
#     accuracy = accuracy_score(y_test, y_pred)
#     print(f"Accuracy on test set: {accuracy * 100:.2f}%")
#     print()