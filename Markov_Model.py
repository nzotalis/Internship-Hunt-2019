############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Nicholas Zotalis"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string
import random
import math

############################################################
# Section 1: Markov Models
############################################################

def tokenize_helper(word):
    if word == '':
        return []
    else:
        for i in range(len(word)):
            if word[i] in string.punctuation:
                if i != 0:
                    return [word[:i], word[i]] + tokenize_helper(word[i + 1:])
                else:
                    return [word[i]] + tokenize_helper(word[i + 1:])
        return [word]

def tokenize(text):
    text = text.split()
    tokenized = []
    for t in text:
        tokenized += tokenize_helper(t)

    return tokenized

def ngrams(n, tokens):
    tokens = ['<START>'] * (n - 1) + tokens + ['<END>']
    ngrams = []

    for i in range(len(tokens) - n + 1):
        if n == 1:
            context = ()
        else:
            context = tuple([tokens[j] for j in range(i, i + n - 1)])
        ngrams.append((context, tokens[i + n - 1]))

    return ngrams
            
class NgramModel(object):

    def __init__(self, n):
        self.order = n
        self.ngrams = {}
        self.context_occurences = {}

    def update(self, sentence):
        for n in ngrams(self.order, tokenize(sentence)):
            try:
                self.ngrams[n] += 1.0
            except KeyError:
                self.ngrams[n] = 1.0

            try:
                self.context_occurences[n[0]] += 1.0
            except KeyError:
                self.context_occurences[n[0]] = 1.0

    def prob(self, context, token):
        try:
            return self.ngrams[(context, token)] / self.context_occurences[context]
        except KeyError:
            return 0.0

    def random_token(self, context):
        context_tokens = sorted([s[1] for s in self.ngrams if s[0] == context])
        r = random.random()
        sumprobs = {}
        sumprobs[0] = 0
        for i in range(len(context_tokens)):
            sumprobs[i + 1] = self.prob(context, context_tokens[i]) + sumprobs[i]
        
        for i in range(len(context_tokens)):
            if sumprobs[i] <= r and r < sumprobs[i + 1]:
                return context_tokens[i]

    def random_text(self, token_count):
        s = ''
        if self.order != 1:
            context = tuple(['<START>'] * (self.order - 1))
            start_context = context
        else:
            context = ()
            start_context = context
            
        for i in range(token_count):
            new = self.random_token(context)
            s += new + ' '
            
            if new == '<END>':
                context = start_context
            elif self.order != 1:
                context = tuple(list(context[1 : len(context)]) + [new])
            
        return s.strip()

    def perplexity(self, sentence):
        p = 0
        ngram_list = ngrams(self.order, tokenize(sentence))
        for ngram in ngram_list:
            p += math.log(1.0) - math.log(self.prob(ngram[0], ngram[1]))
            
        return math.exp(p) ** (1.0 / len(ngram_list))

def create_ngram_model(n, path):
    with open(path, 'r') as f:
        lines = f.readlines()

    m = NgramModel(n)
    for line in lines:
        m.update(line)
    return m

############################################################

m = create_ngram_model(3, "frankenstein.txt")
for i in range(5):
    print(m.random_text(36))
    print('\n')

