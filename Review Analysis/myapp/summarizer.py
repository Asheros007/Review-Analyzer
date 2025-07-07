import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

def summarize_text(text, num_sentences=3):
    if not text:
        return "No text to summarize."

    # Tokenize into sentences
    sentences = sent_tokenize(text)

    # Tokenize into words and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]

    # Calculate word frequencies
    freq = Counter(words)

    # Score sentences
    sentence_scores = {}
    for sent in sentences:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freq:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + freq[word]

    # Sort sentences by score
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Return top N
    summary = ' '.join(ranked_sentences[:num_sentences])
    return summary
