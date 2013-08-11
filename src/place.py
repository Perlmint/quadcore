# -*- coding: utf-8 -*-

class Place:
    def __init__(self, name, background):
        self.name = name
        self.background = background

places = dict([
    ('test.tmx', Place("town", "gakuen.png")),
    ('inner_chatzip.tmx', Place("chatzip", "gakuen.png")),
    ('inner_hobar.tmx', Place("hobar", "gakuen.png")),
    ('inner_phermacy.tmx', Place("phermacy", "gakuen.png")),
    ('inner_school.tmx', Place("school", "gakuen.png")),
    ('inner_shop.tmx', Place("shop", "gakuen.png")),
    ('inner_tonari.tmx', Place("tonari", "gakuen.png")),
    ('inner_zoo.tmx', Place("zoo", "gakuen.png")),
])

