#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

"""
This is the main file that allows the NIPS paper collection to be searched and information to be retrieved.

Most importantly, this file - GETS RESULTS.
"""

import sys, os
from helpers import constants
from .query_builder import QueryBuilder

# Please don't remove me! I'm important so that all the other imports in this script work as well
import lucene

from java.nio.file import Paths
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher


class Search:

    searcher = None
    analyzer = None
    query_string = ''

    def __init__(self, query_string):
        """
        Initialise prerequisites to search

        :param query_string:
        """

        self.query_string = query_string

        # Create a new searcher  based on the already existing index

        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        store_dir = SimpleFSDirectory(Paths.get(os.path.join(base_dir, constants.INDEX_DIR)))
        self.searcher = IndexSearcher(DirectoryReader.open(store_dir))

        # Create the new analyser (the same one that was used for indexing)

        self.analyzer = constants.ANALYZER()

    def get_results(self, result_type):
        """
        Get results from the index based on the given query string

        :param result_type:
        :return:
        """

        print("Searching for:", self.query_string)

        if result_type == 'papers':
            return self.get_papers()
        else:
            print('Result type is not supported.')
            return []

    def get_papers(self):
        """
        Build a list of papers after performing a search on papers
        :return:
        """

        retrieved_files = []

        qb = QueryBuilder(self.query_string)
        query = qb.build_query()

        score_docs = self.searcher.search(query, 50).scoreDocs
        print("%s total matching documents." % len(score_docs))

        for score_doc in score_docs:
            doc = self.searcher.doc(score_doc.doc)

            authors = []

            for author in doc.getFields('author'):
                authors.append(author.stringValue())

            retrieved_files.append({
                'title': doc.get('paper_title'),
                'year': doc.get('year'),
                'authors': authors,
                'event_type': doc.get('event_type'),
                'pdf_name': doc.get('pdf_name'),
                'abstract': doc.get('abstract'),
            })

        return retrieved_files
