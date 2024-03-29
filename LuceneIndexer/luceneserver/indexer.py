#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

"""
This file provides the functionality to index a given lists of papers, joined on their authors.
Currently, the indexing process takes over 10 minutes to perform using the standard analyzer.

The standard analyzer, as part of its job, removes predefined common stop words to make search more relevant.
"""

import os
import sys

from ..helpers import constants

# Please don't delete me! I'm important!
import lucene

from java.nio.file import Paths
from org.apache.lucene.document import Document, TextField, Field, IntPoint, StoredField, FieldType, SortedNumericDocValuesField, SortedDocValuesField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, Term, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import BytesRef


class Indexer(object):
    """Indexer class that handles creating an index from the specified input"""

    store = None
    analyzer = None
    writer = None

    dataset_location = None

    def __init__(self):
        """
        Perform some initial set up
        """

        # Create an index store

        store_dir = self.__create_store_dir()
        self.store = SimpleFSDirectory(Paths.get(store_dir))

        # Create an analyser
        # We use the whitespace analyser since we want to preserve punctuation
        # This is especially relevant when taking into account all the question marks present

        self.analyzer = constants.ANALYZER()

        # Create an index writer using both of the above
        # The open mode tells the writer that it should create, not append

        config = IndexWriterConfig(self.analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        self.writer = IndexWriter(self.store, config)

    def index_docs(self, docs):
        """
        Start indexing of documents
        :return:
        """

        for doc in docs:
            self.__write_paper_to_index(docs[doc])

        # Commit the result and close the writer

        self.writer.commit()
        self.writer.close()

    def __create_store_dir(self):
        """
        Create a directory for the inverted index, if it does not already exist
        :return:
        """

        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        store_dir = os.path.join(base_dir, constants.INDEX_DIR)

        if not os.path.exists(store_dir):
            os.mkdir(store_dir)

        return store_dir

    def __write_paper_to_index(self, paper):
        """
        Write a single paper with author information to the index

        :param common.paper.Paper paper:
        :return:
        """

        concat = paper.title + ' ' + paper.event_type + ' ' + paper.pdf_name + ' ' + ' ' + paper.abstract
        concat = concat + ' ' + paper.paper_text + ' ' + str(paper.year)

        document = Document()
        document.add(TextField("paper_id_store", str(paper.id), Field.Store.YES))
        document.add(StoredField("year_store", paper.year))
        document.add(IntPoint("year_int", paper.year))
        document.add(IntPoint("paper_id_int", int(paper.id)))
        document.add(TextField("paper_title", paper.title, Field.Store.YES))
        document.add(TextField("event_type", paper.event_type, Field.Store.YES))
        document.add(TextField("pdf_name", paper.pdf_name, Field.Store.YES))
        document.add(TextField("abstract", paper.abstract, Field.Store.YES))
        document.add(TextField("paper_text", paper.paper_text, Field.Store.YES))

        # Add a sorted fields for sorting purposes

        document.add(SortedDocValuesField("paper_title_sort", BytesRef(paper.title)))
        document.add(SortedNumericDocValuesField("paper_id", paper.id))
        document.add(SortedNumericDocValuesField("year", paper.year))

        for author in paper.authors:

            # Every author that we add to the same field simply concatenates that when searching

            document.add(TextField('author', author.name, Field.Store.YES))
            document.add(IntPoint("author_id_int", int(author.id)))
            document.add(TextField('author_id', str(author.id), Field.Store.YES))
            concat = concat + ' ' + author.name

        # Finally concatenate every field together and then add it as a field called 'content' with term vectors enabled

        field_type = FieldType()
        field_type.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)
        field_type.setStored(True)
        field_type.setStoreTermVectors(True)
        field_type.setTokenized(True)
        field_type.setStoreTermVectorOffsets(True)

        field = Field('content', concat, field_type)

        document.add(field)

        self.writer.addDocument(document)
