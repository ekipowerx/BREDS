#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "David S. Batista"
__email__ = "dsbatista@inesc-id.pt"

import uuid


class Pattern(object):

    def __init__(self, t=None):
        self.id = uuid.uuid4()
        self.positive = 0
        self.negative = 0
        self.unknown = 0
        self.confidence = 0
        self.tuples = set()
        self.bet_uniques_vectors = set()
        self.bet_uniques_words = set()
        if tuple is not None:
            self.tuples.add(t)

    def __eq__(self, other):
        return self.tuples == other.tuples

    def __cmp__(self, other):
        if other.confidence > self.confidence:
            return -1
        elif other.confidence < self.confidence:
            return 1
        else:
            return 0

    def update_confidence(self, config):
        if self.positive > 0:
            self.confidence = (float(self.positive) / float(self.positive +
                                                            self.unknown * config.wUnk +
                                                            self.negative * config.wNeg))
        elif self.positive == 0:
            self.confidence = 0

    def add_tuple(self, t):
        self.tuples.add(t)

    # put all tuples with BET vectors into a set so that comparision with repeated vectors is eliminated
    def merge_all_tuples_bet(self):
        self.bet_uniques_vectors = set()
        self.bet_uniques_words = set()
        for t in self.tuples:
            # transform numpy array into a tuple so it can be hashed and added into a set
            self.bet_uniques_vectors.add(tuple(t.bet_vector))
            self.bet_uniques_words.add(t.bet_words)

    def update_selectivity(self, t, config):
        matched_both = False
        matched_e1 = False
        for s in config.positive_seed_tuples:
            if s.e1 == t.e1 or s.e1.strip() == t.e1.strip():
                matched_e1 = True
                if s.e2 == t.e2.strip() or s.e2.strip() == t.e2.strip():
                    self.positive += 1
                    matched_both = True
                    break

        if matched_e1 is True and matched_both is False:
            #print t.e1, '\t', t.e2, "->", t.bet_words
            self.negative += 1

        if matched_both is False:
            for n in config.negative_seed_tuples:
                if n.e1 == t.e1 or n.e1.strip() == t.e1.strip():
                    if n.e2 == t.e2.strip() or n.e2.strip() == t.e2.strip():
                        self.negative += 1
                        matched_both = True
                        break

        if matched_both is False:
            self.unknown += 1