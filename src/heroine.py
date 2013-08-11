# -*- coding: utf-8 -*-
import sys
sys.path.append("scripts")

import sekai
import ahri
import sion
import yo
import phermacy

class Heroine:
    def __init__(self, name, engname, global_scr, local_scr, theme):
        self.name    = name
        self.engname = engname
        self.global_scr    = global_scr
        self.local_scr    = local_scr
        self.theme      = theme
        self.love = 0

        self.status = "none"
    def setWorld(self, world):
        self.world = world

scripts = {
    "sekai" : sekai.script,
    "ahri" : ahri.script,
    'sion' : sion.script,
    "yo" : yo.script,
    "phermacy" : phermacy.script
}

heroineCharacters = {
    "sekai" : Heroine(u"사이온지 세카이", "sekai", [scripts["sekai"]], {
        u"town" : None,
    }, None),
    "ahri" : Heroine(u"아리", "ahri", [scripts["ahri"]], {
        u"town" : None,
    }, None),
    "sion" : Heroine(u"은로리", "sion", [scripts["sion"]], {
    }, None),
    "yo" : Heroine(u"Yo자아이", "yo", [scripts["yo"]], {
        u"town" : None,
    }, None),
    "phermacy" : Heroine(u"약사", "phermacy", [scripts["phermacy"]], {
        u"phermacy" : [phermacy.default_phermacy],
    }, None)
}

sekai.heroine = heroineCharacters["sekai"]
ahri.heroine = heroineCharacters["ahri"]
yo.heroine = heroineCharacters["yo"]
sion.heroine = heroineCharacters["sion"]
phermacy.heroine = heroineCharacters["phermacy"]

heroines = dict([
    ("sekai", heroineCharacters["sekai"]),
    ("ahri", heroineCharacters["ahri"]),
    ("sion", heroineCharacters["sion"]),
    ("yo", heroineCharacters["yo"]),
    ("phermacy", heroineCharacters["phermacy"]),
    ])
