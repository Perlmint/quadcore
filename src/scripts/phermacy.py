# -*- coding: utf-8 -*-
from script import *
import random, hashlib

end = [EndScript()]

nice_boat = [
    Conversation(Self(), u"..."),
    u"...",
    Conversation(Self(), u"..."),
    u"이, 일단 설명을...",
    Conversation(Self(), u"뭐, 대충 예상은 했지만 말야"),
    u"....",
    Conversation(Self(), u"이런 식으로 한방 먹이다니, 너도 꽤 S에 소질이 있구나?"),
    u".....",
    Conversation(Self(), u"가볼게. 약이 필요하면 언제든지 찾아와."),
    u"......",
    Conversation(Self(), u"잘, 지어줄테니까."),
    u"약사는 반대로 돌아 걸어갔다.",
    u"나는 그 자리에서 한발짝도 쫓아갈 수 없었다.",
] + end

def placeRoute(loveee, heroine, place, self):
	if place.name == "phermacy":
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
				[Conversation(Self(), u"뭐야, 장난하는거야? 잘했어요? 잘못했어요?"), Love(-10)],
				[Conversation(Self(), u"에이 뭐야, 장난이었어?")],
				[Conversation(Self(), u"선물은 무슨 마음만이라도 고마워"), Love(10)]])])])]]
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
			[[Conversation(Self(), u"")] + end,
			[Conversation(Self(), u"")] + end])]),
		Selection(u"그냥 헤어진다.", [u"인사를 하고 헤어졌다."] + end),
		Selection(u"도망간다.", [Route("Escape", lambda *a, **kw: loveRoute([10], *a, **kw),
			[[Conversation(Self(), u"야! 어디가")] + end,
			nice_boat])])
	])
] + end

nice_default = [
	Conversation(Self(), u""),
	EndScript()
]

default_anywhere = [
	Route("WTF", lambda *a, **kw: loveRoute([50], *a, **kw), [[
		Conversation(Self(), u"좋은아침~!"),
        	Conversation(Self(), u"어디 가는 거야?")] + give_or_take,
		nice_default])]

default_phermacy = [
        Route("normal", lambda *a, **kw: loveRoute([50], *a, **kw),
              [[Conversation(Self(), u"뭐야, 필요한거라도?"),
                Choice(u"그러니까...",
                [
                    Selection(u"아뇨별로",
                    [
		                Conversation(Self(), u"...싱겁기는. 비타민이나 챙겨가."),
                        u"나는 약사가 내준 비타민을 들고 약국을 나왔다.",
                        Love(10)
        			]),
                    Selection(u"머리가 아파요",
                    [
                        Conversation(Self(), u"흠, 대놓고 머리가 아프다면서 오는건 신종 작업수단인가?"),
                        u"...아니, 저.. 진짜 머리가 아픈데..",
                        Conversation(Self(), u"(笑) 나을 수 있는지는 장담 못하지만 약이라도 지어줄게."),
                        u"잠시 후 들고 나온 약을 들고 약국을 나왔다.",
                        Love(10)
                    ]),
                    Selection(u"내 마음이 아파요.",
                    [
                        Conversation(Self(), u"..."),
                        u"...",
                        Conversation(Self(), u"..."),
                        u" ...가볼게요.",
                        u"나는 약국을 나왔다.",
                        Love(-20)
                    ])
		])] + give_or_take,
		[Conversation(Self(), u"또 왔네, 필요한거라도?"),
        Choice(u"",
        [
            Selection(u"아뇨, 별로.",
            [
                Conversation(Self(), u"그렇게 심심하면 환각제라도 지어줄까? 마침 새로 들어온게..."),
                u"약사가 그래도 되는겁니까?!",
                Conversation(Self(), u"어머, 치료의 일환으로 환각제를 쓰기도 하는거 몰라? 비밀로 해줄테니까, 이거 받아가."),
                u"필요없어요!",
                u"나는 재빨리 약국을 나왔다.",
                Love(10)
            ]),
            Selection(u"머리가 아파요",
            [
                Conversation(Self(), u"머리가 자주 아픈것같다? 혹시 밤잠을 설치며 생각할 누군가라도 있는거야?"),
                Choice(u"",
                [
                    Selection(u"무슨소리에요?!",
                    [
                        Conversation(Self(), u"(웃음) 후후, 어딘가 찔리나본데"),
                        u"나는 약을 들고 재빨리 약국을 나왔다.",
                        Love(20)
                    ]),
                    Selection(u"무슨소리에요?!",
                    [
                        Conversation(Self(), u"(웃음) 후후, 어딘가 찔리나본데"),
                        u"나는 약을 들고 재빨리 약국을 나왔다.",
                        Love(10)
                    ])
                ])
            ]),
            Selection(u"내 마음이 아파요",
            [
                Conversation(Self(), u"..."),
                u"...",
                Conversation(Self(), u"..."),
                u"....가볼게요.",
                Conversation(Self(), u"..."),
                u"나는 약국을 나왔다.",
                Love(10)
            ])
        ])
    ] + give_or_take])
]

default = [
    Route("Default Conversation", placeRoute, [default_anywhere, default_phermacy])
]

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