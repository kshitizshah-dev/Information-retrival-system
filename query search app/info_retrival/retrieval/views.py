import os
import re
from collections import defaultdict
from math import log
from django.shortcuts import render

# Preprocessing function
def preprocess(text):
    return re.findall(r'\b\w+\b', text.lower())

# Load documents from a folder
def load_documents(folder_path):
    docs = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                docs[filename] = preprocess(file.read())
    return docs

# Compute term frequencies and document frequencies
def compute_statistics(docs):
    doc_count = len(docs)
    term_doc_freq = defaultdict(int)
    term_freq = defaultdict(lambda: defaultdict(int))

    for doc_id, words in docs.items():
        word_set = set(words)
        for word in words:
            term_freq[doc_id][word] += 1
        for word in word_set:
            term_doc_freq[word] += 1

    return term_freq, term_doc_freq, doc_count

# Compute relevance probabilities using BIM
def compute_relevance_prob(query, term_freq, term_doc_freq, doc_count):
    scores = {}
    for doc_id in term_freq:
        score = 1.0
        for term in query:
            tf = term_freq[doc_id].get(term, 0)
            df = term_doc_freq.get(term, 0)
            p_term_given_relevant = (tf + 1) / (sum(term_freq[doc_id].values()) + len(term_doc_freq))
            p_term_given_not_relevant = (df + 1) / (doc_count - df + len(term_doc_freq))
            score *= (p_term_given_relevant / p_term_given_not_relevant)
        scores[doc_id] = score
    return scores

# View function to handle document retrieval
def retrieve_documents(request):
    if request.method == "POST":
        query = request.POST.get('query', '')
        folder_path = r'D:\code\query search app\books'  # Set the path to your documents folder
        docs = load_documents(folder_path)  # Load documents from folder
        term_freq, term_doc_freq, doc_count = compute_statistics(docs)  # Compute term and doc frequencies

        query_terms = preprocess(query)
        scores = compute_relevance_prob(query_terms, term_freq, term_doc_freq, doc_count)
        ranked_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        return render(request, 'home/result.html', {'query': query, 'ranked_docs': ranked_docs})
    return render(request, 'home/home.html')
