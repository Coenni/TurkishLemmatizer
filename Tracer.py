class Tracer:
    control = 1
    result = False
    names =['EN_UZUN_KOK_KONTROLU',
            'UNSUZ_YUMUSAMA_KONTROLU',
            'UNLU_DARALMASI_KONTROLU',
            'UNLU_DUSMESI_KONTROLU',
            'UNSUZ_DUSMESI_KONTROLU',
            'PEKISTIRME_KONTROLU',
            'UNLU_DEGISIMI'
            ]

    def __init__(self, control, result):
        self.control=control
        self.result=result

    def control_name(self):
        return self.names[self.control]