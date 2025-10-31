from collections import defaultdict
import re

class WordGraph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(int))
        self.groups = 5 

    def add_sentence(self, sentence: str):
        words = re.findall(r'\b\w+\b', sentence.lower())
        if len(words) < 2:
            return
        
        for n in range(2, self.groups + 1):
            if len(words) < n:
                continue
            for i in range(len(words) - n + 1):
                key = tuple(words[i:i + n - 1])
                next_word = words[i + n - 1]
                self.graph[key][next_word] += 1

    def train(self, data):
        for sentence in data:
            self.add_sentence(sentence)

    def predict_next(self, *context):
        
        lowercase_context = []
        for word in context:
            lowercase_word = word.lower()
            lowercase_context.append(lowercase_word)

        context = lowercase_context


        context_length = len(context)
        if context_length < self.groups:
            max_context_length = context_length
        else:
            max_context_length = self.groups


        for k in range(max_context_length, 0, -1):
            key = tuple(context[-k:])
            if key in self.graph:
                next_words = self.graph[key]
                candidates = list(next_words.items())
                
                # sort
                def obtener_frecuencia(par):
                    frecuencia = par[1]
                    return frecuencia

                candidates.sort(key=obtener_frecuencia)
                candidates.reverse()

                return candidates
        return []
