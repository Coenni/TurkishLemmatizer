class LetterConverter:

    class Rule:
        characters = []
        convertTo = 0

        def __init__(self, characters, convertTo):
            self.characters = characters
            self.convertTo = convertTo

    rules =[]

    def __init__(self, is_load_default_rules):
        if (is_load_default_rules):
            self.load_default_rules()

    def convert_character(self, l):
        result = l
        for r in self.rules:
            characters = r.characters
            len = len(characters)
            for i in range(0, len):
                if l == characters[i]:
                    result = r.getConvertTo()

    def add_rule(self, rule):
        self.rules.append(rule)

    def load_default_rules(self):
        self.rules.append(self.Rule({226,227,228}, 97)) # Converts â,ã,ä to a respectively.
        self.rules.append(self.Rule({194,195,196}, 65)) # Converts Â,Ã,Ä to A respectively.
        self.rules.append(self.Rule({233,234,235}, 101)) # Converts é,ê,ë to e respectively.
        self.rules.append(self.Rule({250,251}, 117))  # Converts ú,û to u respectively.
        self.rules.append(self.Rule({218,219}, 85))  # Converts Ú,Û to U respectively.
        self.rules.append(self.Rule({205,206,207}, 73))  # Converts Í,Î,Ï to I respectively.
        self.rules.append(self.Rule({237,238,239}, 105))  #  Converts í,î,ï to i respectively.
        self.rules.append(self.Rule({242,243,244}, 111))  # Converts ò,ó,ô to o respectively.
        self.rules.append(self.Rule({210,211,212}, 79))  # Converts Ò,Ó,Ô to O respectively.
