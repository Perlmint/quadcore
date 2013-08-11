# -*- coding: utf-8 -*-
from script import *
import random, hashlib

end = [EndScript()]

nice_boat = [
    Conversation(Self(), u"날... 귀엽다고 해 줬지?"),
    Conversation(Self(), u"그런데 다른 여자에게 한눈을 팔다니..."),
    u"한 걸음 가까이 다가온다.",
    Conversation(Self(), u"이런건 치사해!"),
    Conversation(Self(), u"고작 여자라는 이유만으로 남자들의 눈길을 끌지!"),
    u"옷자락을 붙잡혔다.",
    Conversation(Self(), u"나는 안되는거야?"),
    Conversation(Self(), u"나는 너밖에 없는데..."),
    u"푹",
    u"배가 뜨겁다.",
    u"눈 앞이 흐려진다...",
    Conversation(Self(), u"이제, 쭉 함께야......")
] + end

def placeRoute(loveee, heroine, place, self):
    if place.name == "school":
        return 1
    return 0

def loveRoute(ratioList, loveee, heroine, place, self):
    ratio = 0
    index = 0
    seed = heroine.love
    for curRatio in ratioList:
        ratio += curRatio
        if seed < ratio:
            return index
        index += 1
    return index

def randomRoute(ratioList, loveee, heroine, place, self):
    ratio = 0
    index = 0
    seed = random.random()
    for curRatio in ratioList:
        ratio += curRatio
        if seed < ratio:
            return index
        index += 1
    return index

def giveItem(loveee, heroine, place, self):
	items = []
	if len(loveee.player.items) == 0:
		self.scripts = [[Choice(u"아무것도 들고있지 않다. 돈이라도 줄까", [
			Selection(u"돈을 준다.", [Money(lambda x: u"%d원을 줬다." % x)]),
			Selection(u"아무것도 들고있지 않다.", [Route("rand", lambda *a, **kw: randomRoute([0.6, 0.45], *a, **kw), [
				[Conversation(Self(), u"날 놀리는거야?"), Love(-10)],
				[Conversation(Self(), u"에이 뭐야, 장난이었어?")],
				[Conversation(Self(), u"선물은 필요없어. 너의 마음으로 충분해."), Love(10)]])])])]]
		return 0
	for i in range(0,3):
		item = random.choice(loveee.player.items)
		items += [(item.name, [u"%s를 주었다." % item.name, Love((eval("0x" + hashlib.md5("%s%d" % (item.name, item.price)).hexdigest()) % 50) - 25)])]
	self.scripts = [[Give(None, dict(items))]]
	return 0

gift_list = ["식칼", "여명808", "컨디션", "혓개나무 추출물", "이상한 약"]

give_or_take = [
    Choice(u"무엇을 할까", [
        Selection(u"선물을 준다.", [Route("asdf", giveItem, [])] + end),
        Selection(u"뭔가 나한테 줄 것 있지 않아?", [Route("Take", lambda *a, **kw: loveRoute([100], *a, **kw), 
            [[Conversation(Self(), u"네 생각이 나서 샀어. 받아줘.")] + end,
            [Conversation(Self(), u"")] + end])]),
        Selection(u"그냥 헤어진다.", [u"인사를 하고 헤어졌다."] + end),
        Selection(u"도망간다.", [Route("Escape", lambda *a, **kw: loveRoute([10], *a, **kw),
            [[Conversation(Self(), u"어딜가는거야?!")] + end,
            nice_boat])])
    ])
] + end

nice_default = [
    Conversation(Self(), u""),
    EndScript()
]

default_anywhere = [
	BGM("yo.ogg"),
    Route("sibal", lambda *a, **kw: loveRoute([100], *a, **kw),
          [
            [Conversation(Self(), u"안녕."),
            u"(귀여운 아이다...)",
            Choice(u"뭐라고 인사할까?", [
                Selection(u"안녕", []),
                Selection(u"누구신지", [
                    Conversation(Self(), u"너무해, 날 모르는거야?"), Love(-10)]),
                Selection(u"너 정말 귀엽구나", [
                    u"(부끄러워 한다...)", Love(50)])
                   ])
            ],
            [Conversation(Self(), u"안녕, 지금 한가해?"),
                          Choice(u"어떻게 할까...", [
                              Selection(u"같이 놀래?", [
                                  Conversation(Self(), u"그래 좋아. 기뻐!"), Love(50), u"(즐거운 시간을 보냈다.)"]),
                              Selection(u"실례지만 누구신지...", [
                                  Conversation(Self(), u"그런 장난은 싫어."), Love(-50), u"(울면서 뛰어가 버렸다...)"]),
                              Selection(u"걱...걱3거거걱걱걱걱ㄱ걱", [
                                  Conversation(Self(), u"너, 머리 괜찮아?")])
    ])]])]

default = default_anywhere

flag_set = [
    EndScript()
]

gift_recieve = [
    EndScript()
]

gift_give = [
    EndScript()
]

script = default

