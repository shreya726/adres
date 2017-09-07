import copy


class SublexicalScore:
    def __init__(self, target, response):
        self.target = target.lower()
        self.response = response.lower()
        self.errors = 0
        self.overlap = False

    # Measuring overlap in word
    def overlap_word(self):
        letters = 0
        response = copy.copy(self.response)
        for t in self.target:
            if t in response:
                letters += 1
                response = self.remove(response, t)
        return float(letters) / float(len(self.target)) >= 0.5

    def score(self):
        if "don't know" in self.response: return 0
        if "not sure" in self.response: return 0
        if ';' in self.response:
            '''If multiple responses entered, take the last one afer semicolon as the whole response.
            '''
            self.response = self.response.split(';')[-1]
        if len(self.response) > 1:
            while self.response[0] == " " and len(self.response) > 1:
                self.response = self.response[1:]
            while self.response[-1] == " " and len(self.response) > 1:
                self.response = self.response[:-1]
        if self.response == self.target:
            return 9
        if self.response == "" or self.response == "-":
            return 0
        if self.addition():
            return 7

        self.overlap = self.overlap_word()
        if not self.overlap:
            if len(self.response) == len(self.target):
                return 2
            else:
                return 1

        if self.deletion():
            return 4
        if self.transposition():
            return 6
        if self.substitution():
            return 5
        else:
            return 3

    # Remove a certain letter from a word
    def remove(self, word, letter):
        for i in range(len(word)):
            if word[i] == letter:
                return word[:i] + word[i + 1:]
        return word

    # Check number of additions
    def addition(self):
        diff = len(self.response) - len(self.target)
        if diff > 1:
            self.errors += diff
            return False
        if diff == 1:
            self.errors += 1
            return all([t not in self.response for t in self.target])
        return False

    # Check number of transpositions.
    def transposition(self):
        last_index = -1
        if len(self.target) == len(self.response):
            for i in range(0, len(self.response)):
                if self.response[i] != self.target[i]:
                    if last_index == -1:
                        last_index = i
                    else:
                        if self.response[last_index] == self.target[i]:
                            last_index = -1
                            self.errors += 1
                            continue
                        else:
                            return False
            return True
        else:
            return False

    # Check number of substitutions.
    def substitution(self):
        if len(self.response) == len(self.target):
            s = 0
            for i in range(0, len(self.response)):
                if self.response[i] != self.target[i]:
                    s += 1
                    self.errors += 1
            return s == 1
        return False

    def deletion(self):
        diff = len(self.target) - len(self.response)
        if diff > 0:
            self.errors += 1
        if diff == 1:
            return all([r in self.target for r in self.response])
        return False
