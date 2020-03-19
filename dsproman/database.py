from operator import itemgetter

crystal_types = "Sp", "Qz", "LiF", "BaF", "CaF"

Sp_signals  = (250, 400),
Qz_signals  = (250, 346),
LiF_signals = (260, 331), (450, 680), (450, 530)
BaF_signals = (250, 570), (320, 960)
CaF_signals = (410, 580), (600, 770), (400, 770), (450, 630)

signals = dict(
Sp  =  Sp_signals,
Qz  =  Qz_signals,
LiF = LiF_signals,
BaF = BaF_signals,
CaF = CaF_signals,
)

excitations = {key: tuple(map(itemgetter(0), value)) for key, value in signals.items()}
emissions   = {key: tuple(map(itemgetter(1), value)) for key, value in signals.items()}
