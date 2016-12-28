import re

class Stem:
    stem = ''
    stem_type = 'N/A'

    def __init__(self, stem, type_input):
        self.stem = stem
        self.stem_type = type_input

    def get_stem(self):
        return self.stem

    def get_pattern(self):
        return re.compile(self.stem)

    def get_softened_conversion(self):
        stem_modified = []
        last_letter = str(self.stem)[-1]

        if last_letter == 'p':
            stem_modified.append(str(self.stem)[:-1]+'b')
        elif last_letter == 'ç':
            stem_modified.append(str(self.stem)[:-1] + 'c')
        elif last_letter == 't':
            stem_modified.append( str(self.stem)[:-1] + 'd')
        elif last_letter == 'k':
            stem_modified.append( str(self.stem)[:-1] + 'g')
            stem_modified.append( str(self.stem)[:-1] + 'ğ')
        else:
            stem_modified.append(self.stem)
        return stem_modified


    def get_daralmis_halleri(self):
        daralmis = []
        daralmis.append(self.stem[0:-1]+'ı')
        daralmis.append(self.stem[0:-1] + 'i')
        daralmis.append(self.stem[0:-1] + 'u')
        daralmis.append(self.stem[0:-1] + 'ü')
        return daralmis

    def get_unlu_dusmus_hali(self):
        sb = ''
        characters = self.stem
        for i in range(0, len(characters)):
            if i >= len(characters)-3:
                if characters[i] == 'ı':
                    pass
                elif characters[i] == 'i':
                    pass
                elif characters[i] == 'ü':
                    pass
                elif characters[i] == 'u':
                    pass
                else:
                    sb+= characters[i]
            else:
                sb += characters[i]
        return sb

    def get_unsuz_dusmeli_hali(self):
        return str(self.stem)[:-1]

