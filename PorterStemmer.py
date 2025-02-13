
from nltk.stem import PorterStemmer

class Stemmer:

    def __init__(self):
        self.vowels = 'aeiou'

    # utility function to check whether the word contains a vowel or not
    def isvowel(self, ch):
        ch = ch.lower()

        for c in ch:
            if c not in self.vowels:
                return False
        return True
        
    
    # utility function to check whether the word contains a consonant or not
    def isconsonant(self, ch):
        return not self.isvowel(ch)
    


    def encode(self, word):
        return ['C' if self.isconsonant(ch) else 'V' for ch in self.group(word)]

    # group consonants or vowels that are together into a single unit
    # CCC -> C
    def group(self, word):
        groups = []
        preceeding = None
        for idx, ch in enumerate(word):
            if not preceeding:
                preceeding = ch
                continue
            
            if self._compare(preceeding, ch):
                preceeding += ch
            else:
                groups.append(preceeding)
                preceeding = ch

            if idx == len(word) - 1:
                    groups.append(preceeding)
        return groups
    
    def m_count(self, word):
        encoded = self.encode(word)
        return "".join(encoded).count('VC')

    def _compare(self, ch1, ch2):
        if self.isconsonant(ch1) and self.isconsonant(ch2):
            return True
        elif self.isvowel(ch1) and self.isvowel(ch2):
            return True
        else:
            return False
        
    # check if word ends with any letter in lt
    def _chk_LT(self, stem, lt):
        for letter in lt:
            if stem.endswith(letter):
                return True
        return False

    def _chk_v(self, stem):
        for letter in stem:
            if letter in self.vowels:
                return True
            
        return False
    
    # double consonants
    def _chk_d(self, stem):
        if self.isconsonant(stem[-1]) and self.isconsonant(stem[-2]):
            return True
        return False
    
    # check if it ends in CVC
    def _chk_o(self, stem):
        if len(stem) < 3:
            return False
        
        if self.isconsonant(stem[-3]) and self.isvowel(stem[-2]) and self.isconsonant(stem[-1]):
            return True
        else:
            return False
        

    def _step_1(self, word):
        # plurals and past participles
        stem = word
        stepb2 = False

        # step 1a
        if stem.endswith('sses'):
            stem = stem[:-2]
        elif stem.endswith('ies'):
            stem = stem[:-2]
        elif not stem.endswith('ss') and stem.endswith('s'):
            stem = stem[:-1]

        #step 1b

        if len(stem) > 4:
            if stem.endswith('eed') and self.m_count(stem) > 0:
                stem = stem[:-1]
            elif stem.endswith('ed'):
                stem = stem[:-2]
                if not self._chk_v(stem):
                    stem = word
                else:
                    stepb2 = True

            elif stem.endswith("ing"):
                stem = stem[:-3]
                if not self._chk_v(stem):
                    stem = word
                else:
                    stepb2 = True
            

        if stepb2:
            if stem.endswith('at') or stem.endswith('bl') or stem.endswith('iz'):
                stem += 'e'
            elif self._chk_d(stem) and not self._chk_LT(stem, 'lsz'):
                stem = stem[:-1]
            elif self.m_count(stem) == 1 and self._chk_o(stem):
                stem += 'e'

        # step 1c
        if self._chk_v(stem) and stem.endswith('y'):
            stem = stem[:-1] + 'i'

        return stem

    def _step_2(self, stem):
        pair_tests = [('ational','ate'), ('tional','tion'), ('enci','ence'), ('anci','ance'), ('izer', 'ize'),
                      ('abli','able'), ('alli','al'), ('entli', 'ent'), ('eli', 'e'), ('ousli', 'ous'), ('ization', 'ize'),
                      ('ation', 'ate'), ('ator', 'ate'), ('alism', 'al'), ('iveness', 'ive'), ('fulness', 'ful'),
                      ('ousness', 'ous'), ('aliti','al'), ('ivit', 'ive'), ('biliti','ble')]
        if self.m_count(stem) > 0:
            for term, subs in pair_tests:
                if stem.endswith(term):
                    return stem[:-len(term)] + subs
        return stem
    
    def _step_3(self, stem):
        pair_tests = [('icate','ic'),('ative',''),('alize','al'),('iciti','ic'),('ical','ic'),('ful',''),('ness','')]
        if self.m_count(stem) > 0:
            for term, subs in pair_tests:
                if stem.endswith(term):
                    return stem[:-len(term)]+subs
        return stem
    

    def _step_4(self, stem):
        """
        Remove suffixes
        """
        suffixes_1 = ['al','ance','ence','er','ic','able','ible','ant','ement','ment','ent']
        special_case = 'ion'
        suffixes_2 = ['ou','ism','ate','iti','ous','ive','ize']
        if self.m_count(stem) > 1:
            for suffix in suffixes_1:
                if stem.endswith(suffix):
                    return stem[:-len(suffix)]
            if stem.endswith(special_case):
                temp = stem[:-len(special_case)]
                if self._chk_LT(temp, 'st'):
                    return temp
            for suffix in suffixes_2:
                if stem.endswith(suffix):
                    return stem[:-len(suffix)]
        return stem
    
    def _step_5(self, stem):
        temp = stem
        #Step 5a
        if self.m_count(temp)>1 and temp.endswith('e'):
            temp = temp[:-1]
        elif self.m_count(temp) == 1 and (not self._chk_o(temp)) and temp.endswith('e') and len(temp) > 4:
            temp = temp[:-1]
        #Step 5b
        if self.m_count(temp) > 1 and self._chk_d(temp) and self._chk_LT(temp, 'l'):
            temp = temp[:-1]
        return temp
    

    def stem(self, word):
        stem = word.lower().strip()
        stem = self._step_1(stem)
        stem = self._step_2(stem)
        stem = self._step_3(stem)
        stem = self._step_4(stem)
        stem = self._step_5(stem)

        return stem
    

stemmer = Stemmer()

print(stemmer.stem('cunning'))
