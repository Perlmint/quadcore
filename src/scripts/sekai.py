# -*- coding: utf-8 -*-
from script import *
import random, hashlib

end = [EndScript()]

nice_boat = [
    Conversation(Self(), u"계속 날 피할 때마다 물어봤는데..."),
    Conversation(Self(), u"끝까지 무슨 일이 있는지 말하지 않았어"),
    u"한 걸음 가까이 다가온다.",
    Conversation(Self(), u"그래도 네가 좋으니까, 언젠가 말해줄거라고 믿고 있었어"),
    Conversation(Self(), u"그러고 있었는데 언제부턴가 더이상 피하지 않더라고 그래서 뭔가 있던 걱정이 없어진 줄 알았어"),
    Conversation(Self(), u"안심이되서, 이제는 괜찮다고, 그렇게 생각하고 있었는데 친구들이 네가 다른 여자들하고 있는 것을 봤다고 하더라고"),
    u"더 가까이 다가온다.",
    Conversation(Self(), u"걱정은 되지만 아닐거라고 믿고 그런 이야기들을 무시하려고, 직접 보기 전까지는 믿을 수 없다고 버텨내고 있었는"),
    Conversation(Self(), u"나중에 네가 그 여자애랑 같이 있다는 이야기를 듣고 찾아갔어..."),
    u"어느새 바로 눈 앞에까지 다가왔다.",
    u"푹",
    u"그녀의 손에는 작은 칼이 들려있고 그 반정도는 어느새 내 몸 속에 들어와 있었다.",
    u"그리고 나는 죽었다."
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

default_school = [
    Conversation(Self(), u"주말인데 학교에는 무슨 일로 온거야?"),
    Choice(u"", [
        Selection(u"그러는 너는?", [
            Route("How About You", lambda *a, **kw: loveRoute([50], *a, **kw), [
                [Route("rand", lambda *a, **kw: randomRoute([0.5], *a, **kw), [[
                    Conversation(Self(), u"헤헷~ 비밀이지"),
                    Conversation(Self(), u"ㅋㅋㅋㅋ")] + give_or_take, [
                    Conversation(Self(), u"난누구 여긴 어디?")] + give_or_take
                ])] + give_or_take,
                [Conversation(Self(), u"왠지 학교오면 널 볼 수 있을 것 같아서 히히"),
                Conversation(Self(), u"봐봐 이렇게 만났잖아")]
            ])
        ] + give_or_take),
        Selection(u"그러게...", [
            Conversation(Self(), u"에이 그게 뭐야"),
        ] + give_or_take),
    ]),
] + give_or_take

default = [
    BGM("sekai.ogg"),
    Route("Default Conversation", placeRoute, [default_anywhere, default_school])
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

