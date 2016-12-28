class TurkishAlphabet:
    ALPHABET = [97, 98, 99, 231, 100, 101, 102, 103, 287, 104, 305, 105, 106,
                107, 108, 109, 110, 111, 246, 112, 114, 115, 351, 116, 117, 252, 118, 121, 122]

    def display(self):
        for ascii in self.ALPHABET:
            print('ascii ' + ascii + chr(ascii))

    def get_letter(self,pos):
        return chr(self.ALPHABET[pos])

    def get_position(self, character):
        pos = -1
        alphpabet_len = len(self.ALPHABET)
        for i in range(0, alphpabet_len):
            if ord(character) == self.ALPHABET[i]:
                pos = i
        return pos
