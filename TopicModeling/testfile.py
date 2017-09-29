import os

from gensim import corpora, models
from gensim.models import AuthorTopicModel

from common.database import DataBase

base_dir = os.path.join(os.path.dirname(__file__), 'corpora')

dictionary_file = os.path.join(base_dir, 'documents.dict')
corpus_file = os.path.join(base_dir, 'corpus.mm')

# Create dictionary (word to id)
if os.path.exists(dictionary_file):
    dictionary = corpora.Dictionary.load(dictionary_file)
else:

    # Read documents

    db = DataBase('../dataset/database.sqlite')
    authors = db.get_all_authors()

    papers = db.get_all()

    documents = []

    for id, paper in papers.items():
        documents.append(paper.paper_text)

    # Tokenize and remove stopwords

    # remove common words and tokenize (I don't know if we have to do this by hand? There are a lot of words)
    stoplist = set('for a of the and to in '.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    # remove words that appear only once
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    # Save tokens that occur more than once
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    # Create dictionary
    dictionary = corpora.Dictionary(texts)
    dictionary.save(os.path.join(os.path.dirname(__file__), 'corpora', 'documents.dict'))

# Create corpus (wordid to count)
if os.path.exists(corpus_file):
    corpus = corpora.MmCorpus(corpus_file)
else:
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(corpus_file, corpus)

# Create model
model = models.LdaModel(corpus, id2word=dictionary, num_topics=5)

# Print the topics
i = 0
for topic in model.show_topics(num_topics=5, formatted=False):
    i = i + 1
    print("Topic #" + str(i) + ":")
    for word in topic[1]:
        print('{} ({})'.format(word[0], word[1]))
    print("")

