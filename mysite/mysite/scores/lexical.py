import enchant

import mysite.scores.semantic as sm

usDict = enchant.Dict('en_US')
ukDict = enchant.Dict('en_UK')

class LexicalScore:

    def __init__(self, target, response, last3 = [], targets=[]):
        self.target = target.lower()

        self.last3 = last3
        self.targets = targets

        if len(response) > 1:
            # Makes all of the response other than the first letter lower-case.
            response = response[0] + response[1:].lower()

        if ';' in response:
            # If multiple responses entered, take the last one afer
            # semicolon as the whole response.
            response = response.split(';')[-1]


        # Taking out spaces at the beginning and end of string
        if len(response) > 1:
            while response[0] == " " and len(response) > 1:
                response = response[1:]
            while response[-1] == " " and len(response) > 1:
                response = response[:-1]
        self.response = response.lower()
        self.perseveration = self.response in self.last3
        self.is_word = self.check_is_word()

    def perseveration_non_word(self):
        if self.perseveration:
            return True
        overlap_letters = 0
        i = 0
        for word in self.last3:
            word_length = len(word)
            while (i < len(self.response)) and len(word) > 0:
                for j in range(0, len(word)):
                    if self.response[i] == word[j]:
                        overlap_letters += 1
                        word = word[j + 1:]
                        break
                i += 1
            if float(overlap_letters) / float(word_length) >= 0.5:
                return True
        return False

    def check_is_word(self):
        # add all targets
        if self.response in self.targets:
            return True
        if len(self.response) < 2:
            # Single letters are not counted as words.
            return False
        try:
            return usDict.check(self.response) or ukDict.check(self.response)
        except:
            return False

    def score(self):
        if "don't know" in self.response or "not sure" in self.response:
            return 0

        if self.response == self.target:
            # Target
            return 9

        if self.response == '' or self.response == ' ':
            # No response
            return 0

        elif not self.is_word:
            if self.target in self.response.split():
                # If target is in the description,
                # treat as accurate response of 9.
                return 9
            elif sm.related_description(self.target, self.response):
                # Related description
                return 5
            elif sm.description(self.response, self.target):
                # Unrelated description
                return 2
            # Perseveration of a nonword - not incorporating overlap stuff
            elif self.perseveration_non_word():
                return 1
            else:
                # Non-word
                return 3
        elif sm.morphological_error(self.target, self.response):
            # Morphological errors
            return 8
        else:
            # Perseveration of a word
            if self.perseveration:
                return 4
            # unrelated word
            return 6