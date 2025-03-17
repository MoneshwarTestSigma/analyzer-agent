from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from collections import Counter, OrderedDict
from sumy.nlp.tokenizers import Tokenizer
import re

def abbreviate_frequent_words(text, threshold=6):
    words = re.findall(r'\b\w+\b', text) 
    word_counts = Counter(words) 

    replacements = {word: word[:3] + "." for word, count in word_counts.items() if count >= threshold}

    print(replacements)
    
    # Apply replacements
    for word, abbr in replacements.items():
        text = re.sub(r'\b' + re.escape(word) + r'\b', abbr, text)

    return text
def summarize_text(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)

    # Remove redundancy
    unique_sentences = list(OrderedDict.fromkeys(str(sentence) for sentence in summary))
    summarized_text = " ".join(unique_sentences)

    # Abbreviate frequent words
    return abbreviate_frequent_words(summarized_text)
