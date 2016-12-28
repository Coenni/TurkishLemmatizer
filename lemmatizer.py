from Stem import Stem
from Tracer import Tracer
from TurkishAlphabet import TurkishAlphabet
import re
import numpy as np
import copy

'''
Turkish Lemmatizer class. It provides users method to lemmatize given word.
'''
class Lemmatizer:
    turkish_alphabet = TurkishAlphabet()
    stems = np.empty((29, 29, 29), np.chararray)
    candidates = []
    trace=[]
    stem_found = False
    EN_UZUN_KOK_KONTROLU = 0;
    UNSUZ_YUMUSAMA_KONTROLU = 1; # pçtk
    UNLU_DARALMASI_KONTROLU = 2; #bekl - e - mek bekl - i - yor
    UNLU_DUSMESI_KONTROLU = 3; # oğul
    UNSUZ_DUSMESI_KONTROLU = 4; #küçücük, ufacık, yükselmek, alçalmak
    PEKISTIRME_KONTROLU = 5; # sapasağlam -> sağlam
    UNLU_DEGISIMI = 6; #sana -> sen, bana -> ben

    def get_trace(self):
        message = 'Trace:'
        trace_len = len(self.trace)
        for i in range(0, trace_len):
            trace_next = self.trace[i]
            message +='['+str(trace_next.control_name())+'='+str(trace_next.result)+'] <- '
        return message

    def set_stem(self, the_list, next_stem):
        for i in range(0, len(the_list)):
            if the_list[i] == None:
                the_list[i]=next_stem
                break

    def set_stem_all(self, source, destination):
        index = 0
        for i in range(0, len(source)):
            if source[i] == None:
                index = i
                break

        for i in range(0, len(destination)):
            if destination[i] != None:
                source[index+i]=destination[i]
                break

    def add_stem(self, stem):
        stem_len = len(stem)
        for i in range(0, (stem_len-1)):
            letter = stem[i]
            position = self.turkish_alphabet.get_position(letter)
            if position == -1:
                raise Exception('Character not found')
        stem = str(stem).lower()
        first_letter = stem[0]
        second_letter = stem[1]
        first_letter_index = self.turkish_alphabet.get_position(first_letter)
        second_letter_index = self.turkish_alphabet.get_position(second_letter)
        next_stem = Stem(stem, '')
        #self.stems[first_letter_index][second_letter_index].append(s)
        self.set_stem(self.stems[first_letter_index][second_letter_index], next_stem)

    '''
    Finds stem of a given word. This function allows words that contains more than or equal 2 characters. Passing string that has less than
    2 characters will throw {@link StringIndexOutOfBoundsException}. This function returns first found stem as a result. <b>HOWEVER</b>, stem of
    the word may not be the return value. User <code>getAllCandidates()</code> function to retrieve all candidate stems. The correct stem might be
    one of them.
    '''
    def lemmatize(self, word):
        self.trace = []
        self.candidates = []
        if str(word).lower() == 'sana':
            self.trace.append(Tracer(self.UNLU_DEGISIMI, True))
            return 'sen'
        if str(word).lower() == 'bana':
            self.trace.append(Tracer(self.UNLU_DEGISIMI, True))
            return 'ben'

        #validate word
        word_len = len(word)
        for i in range(0, word_len):
            letter = word[i]
            position = self.turkish_alphabet.get_position(letter)
            if position == -1:
                raise Exception('Character not found')
        first_character = word[0]
        second_character = word[1]
        first_pos = self.turkish_alphabet.get_position(first_character)
        second_pos = self.turkish_alphabet.get_position(second_character)
        list_stem = copy.copy(self.stems[first_pos][second_pos])

        candidate = ''

        #unsuz yumusama kontrolu
        if second_character =='d':
            second_pos = self.turkish_alphabet.get_position('t')
        elif second_character=='c':
            second_pos = self.turkish_alphabet.get_position('ç')
        elif second_character=='g':
            second_pos = self.turkish_alphabet.get_position('k')
        elif second_character=='ğ':
            second_pos = self.turkish_alphabet.get_position('k')
        elif second_character == 'b':
            second_pos = self.turkish_alphabet.get_position('p')

        self.set_stem_all(list_stem, self.stems[first_pos][second_pos])
        '''
        ÜNSÜZ YUMUŞAMA KONTROLÜ  p,ç,t,k -> b,c,d,ğ,g
        '''
        candidate = self.find_longest_matched_stem(list_stem, word,Lemmatizer.UNSUZ_YUMUSAMA_KONTROLU)
        if len(candidate)>0:
            self.trace.append(Tracer(Lemmatizer.UNSUZ_YUMUSAMA_KONTROLU, True))
            self.candidates.append(candidate)
        else:
            self.trace.append(Tracer(Lemmatizer.UNSUZ_YUMUSAMA_KONTROLU, False))

        # unlu daralmasi kontrolu
        '''
        ÜNLÜ DARALMASI KONTROLÜ  a ve e ile biten sözcüklerin -yor eki aldığında a ve e'nin i,ı,u,ü dönüşmesi
        '''
        candidate = self.find_longest_matched_stem(list_stem, word, Lemmatizer.UNLU_DARALMASI_KONTROLU)
        if len(candidate) > 0:
            self.trace.append(Tracer(Lemmatizer.UNLU_DARALMASI_KONTROLU, True))
            self.candidates.append(candidate)
        else:
            self.trace.append(Tracer(Lemmatizer.UNLU_DARALMASI_KONTROLU, False))

        #unlu dusmesi kontrolu
        '''
        ÜNLÜ DÜŞMESİ KONTROLÜ  İkinci hecesinde dar ünlü bulunan sözcükler ünlüyle başlayan ek aldığında ünlü düşmesi görülür. sabır -> sabrım
        '''
        candidate = self.find_longest_matched_stem(list_stem, word, Lemmatizer.UNLU_DUSMESI_KONTROLU)
        if len(candidate)>0:
            self.trace.append(Tracer(Lemmatizer.UNLU_DUSMESI_KONTROLU, True))
            self.candidates.append(candidate)
        else:
            self.trace.append(Tracer(Lemmatizer.UNLU_DUSMESI_KONTROLU, False))

        #unsuz dusmesi
        '''
        Kimi sözcüklerde türetme ve birleştirme sırasında "ünsüz düşmesi" görülür.  küçük-cük →  küçücük
        '''
        candidate = self.find_longest_matched_stem(list_stem, word, Lemmatizer.UNSUZ_DUSMESI_KONTROLU)
        if len(candidate) > 0:
            self.trace.append(Tracer(Lemmatizer.UNSUZ_DUSMESI_KONTROLU, True))
            self.candidates.append(candidate)
        else:
            self.trace.append(Tracer(Lemmatizer.UNSUZ_DUSMESI_KONTROLU, False))

        #pekistirme kontrolu
        '''
        PEKİŞTİRME KONTROLU  Türkçede bazı kelimeler önüne ek alarak pekiştirilirler.  kırmızı -> kıpkırmızı
        '''
        candidate = self.find_longest_matched_stem(list_stem, word, Lemmatizer.PEKISTIRME_KONTROLU)
        if len(candidate) > 0:
            self.trace.append(Tracer(Lemmatizer.PEKISTIRME_KONTROLU, True))
            self.candidates.append(candidate)
        else:
            self.trace.append(Tracer(Lemmatizer.PEKISTIRME_KONTROLU, False))

        all_candidates = self.get_all_candidates()
        longest = ''
        all_candidates_len = len(all_candidates)
        for i in range(0, all_candidates_len):
            if len(all_candidates[i])>len(longest):
                longest = all_candidates[i]
        if all_candidates_len < 1:
            self.stem_found = False
        else:
            self.stem_found = True

        #en uzun kok kontrolu
        # First check if there is a longest matched stem in word
        candidate = self.find_longest_matched_stem(list_stem, word, Lemmatizer.EN_UZUN_KOK_KONTROLU)
        if len(candidate) > 0:
            self.trace.append(Tracer(Lemmatizer.EN_UZUN_KOK_KONTROLU, True))
            self.candidates.append(candidate)
            return candidate
        else:
            self.trace.append(Tracer(Lemmatizer.EN_UZUN_KOK_KONTROLU, False))

        return word if len(longest) < 1 else longest

    '''
    Finds longest matched  stem of < code > word < / code > in given < code > stemList < / code > by considering
    given < code > control < / code > variable.
     < b > Control objects < / b > < br / >
     < ol >
     < li > EN_UZUN_KOK_KONTROLU < / li >
     < li > UNSUZ_YUMUSAMA_KONTROLU < / li >
     < li > UNLU_DARALMASI_KONTROLU < / li >
     < li > UNLU_DUSMESI_KONTROLU < / li >
     < li > UNSUZ_DUSMESI_KONTROLU < / li >
     < li > PEKISTIRME_KONTROLU < / li >
     < / ol >
    '''

    def find_longest_matched_stem(self, stem_list, word, control):
        longest = ''
        for i in range(0, len(stem_list)):
            stem = stem_list[i]
            if stem == None:
                break
            if control == Lemmatizer.EN_UZUN_KOK_KONTROLU:
                pattern = re.compile(stem.get_pattern())
                match_obj = pattern.match(word)
                if match_obj and match_obj.start() == 0:
                    if len(longest) < len(stem.get_stem()):
                        longest = stem.get_stem()
            elif control == Lemmatizer.UNSUZ_YUMUSAMA_KONTROLU:
                #if stem ends with k softening conversion can be either g or ğ
                if stem.stem[-1] == 'k':
                    pattern1 = re.compile(stem.get_softened_conversion()[0])
                    m1 = pattern1.match(word)
                    if m1:
                        if len(longest) < len(stem.get_stem()):
                            longest = stem.get_stem()
                    pattern2 = re.compile(stem.get_softened_conversion()[1])
                    m2 = pattern2.match(word)
                    if m2:
                        if len(longest) < len(stem.get_stem()):
                            longest = stem.get_stem()
                #otherwise get softened version
                else:
                    pattern = re.compile(stem.get_softened_conversion()[0])
                    m1 = pattern.match(word)
                    if m1:
                        if len(longest) < len(stem.get_stem()):
                            longest = stem.get_stem()
            elif control == Lemmatizer.UNLU_DARALMASI_KONTROLU:
                s = stem.get_stem()
                if str(s)[-1] == 'e' or str(s)[-1] == 'a':
                    daralmis = stem.get_daralmis_halleri()
                    for i in range(0, len(stem.get_daralmis_halleri())):
                        pattern = re.compile(daralmis[i])
                        match_obj = pattern.match(word)
                        if match_obj and match_obj.start() == 0:
                            if len(longest) < len(stem.get_stem()):
                                longest = stem.get_stem()
            elif control == Lemmatizer.UNLU_DUSMESI_KONTROLU:
                if len(stem.get_stem()) > 3:
                    ltc = str(stem.get_stem())[-3:]
                    if ltc.find('i')>0 or ltc.find('ı') > 0 or ltc.find('u')>0 or ltc.find('ü')>0: #TODO
                        pattern = re.compile(stem.get_unlu_dusmus_hali())
                        match_obj = pattern.match(word)
                        if match_obj and match_obj.start() == 0:
                            if len(longest) < len(stem.get_stem()):
                                longest = stem.get_stem()
            elif control == Lemmatizer.UNSUZ_DUSMESI_KONTROLU:
                pattern = re.compile(stem.get_unsuz_dusmeli_hali())
                match_obj = pattern.match(word)
                if match_obj and match_obj.start() == 0:
                   if len(longest) < len(stem.get_stem()):
                       longest = stem.get_stem()
            elif control == Lemmatizer.PEKISTIRME_KONTROLU:
                pattern = re.compile(stem.get_pattern())
                match_obj = pattern.search(word)#not match but search match controls from beginning
                if match_obj and match_obj.end() == len(stem.get_stem())+match_obj.start():
                   if len(longest) < len(stem.get_stem()):
                       longest = stem.get_stem()
        return longest

    # returns unique candidate word list
    def get_all_candidates(self):
        return list(set(self.candidates))