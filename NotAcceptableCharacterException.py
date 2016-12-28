class NotAcceptableCharacterException:
    def __init__(self,c, stem, pos):
        raise ValueError("Character '" + c + "' at position " + (pos+1) + " \"" + stem
                         + "\" is not an acceptable letter for Turkish Lemmatizer.")