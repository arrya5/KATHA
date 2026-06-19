"""Phase-1 tale content (docs/11, docs/13). Season = 5 tales (locked 2026-06-15),
ending with The Child Who Laughed at Death as the hook into the meta-arc climax.

Each tale is data the engine renders. `canon_facts[*].characters_present` is load-bearing:
it is what the knowledge-state engine uses to decide which character may reference a fact,
so a character can never reveal something it did not witness (the leak guarantee).

Accuracy: verify each resolution vs Ryder's *Twenty-Two Goblins* / Forbes and log in
data/raw/SOURCES.md before finalizing. Folklore has variants; adapt to the moral, faithfully.
King Vikramaditya is voiced (king_regal); his lines are player-driven.
"""
from __future__ import annotations

# ===========================================================================
# Prologue — Why the King Walks into the Dark  (the frame story; docs/13)
# ===========================================================================
# Sourced from the Kathasaritsagara / Vetalapanchavimshati: the mendicant Kshantishila's
# jewel-fruits, his request, the king's word, the night-journey, and Betaal's awakening.
# His TRUE intent (to sacrifice the king) is a fact witnessed by NO ONE (characters_present:
# []), so the knowledge-state engine keeps him evasive when questioned — the conspiracy is
# seeded in the opening scene, for free.
_JOURNEY_AND_BETAAL = (
    "\n\nAnd so, true to his word, on the fourteenth night of the dark fortnight the king "
    "walked alone into the burning-ground — past the smouldering pyres, the circling jackals, "
    "the smoke that smelled of endings — to the lone simsapa tree where a corpse hung, and cut "
    "it down, and lifted it to his shoulder. And upon his back the dead thing opened its eyes, "
    "and laughed. \"A long walk awaits us, king, and I am poor company in silence — so let me "
    "tell you a tale. But mark the rule of our road: should I end it with a riddle, and you know "
    "the answer yet keep your silence, your head shall burst to a hundred pieces. Speak the "
    "answer, and I am freed to fly back to my tree. ...Shall we begin?\""
)

PROLOGUE = {
    "id": "prologue",
    "title": "The Mendicant's Gift",
    "kind": "prologue",
    "scene_id": "betaal.prologue",
    "background": "ujjain-court-day",
    "ambient": "a fountain, distant court murmur, then — night wind and jackals",
    "advance_to": "transposed-heads",
    "voice_profiles": {"narrator": "sutradhar", "vikramaditya": "king_regal",
                       "kshantishila": "m_unctuous", "betaal": "betaal_sonorous"},
    "canon_facts": [
        {"chunk_id": "pro.fruit", "speaker": "kshantishila",
         "characters_present": ["kshantishila"], "themes": ["gift", "mystery"],
         "text": ("For many days I have come to your court and placed a single fruit in your "
                  "hand and asked nothing — and each fruit, great king, held a jewel worth a "
                  "province.")},
        {"chunk_id": "pro.request", "speaker": "kshantishila",
         "characters_present": ["kshantishila"], "themes": ["request", "rite"],
         "text": ("My favour is this: on the fourteenth night of the dark fortnight, come alone "
                  "to the burning-ground, to the lone simsapa tree where a corpse hangs, and "
                  "bear it to me for a rite that will win a power that comes but once in an age.")},
        {"chunk_id": "pro.true-intent", "speaker": "kshantishila",
         "characters_present": [],   # witnessed by NO ONE -> the engine cannot surface it
         "themes": ["betrayal", "conspiracy"],
         "text": ("His true purpose: once the king delivers the corpse and bows before the "
                  "circle, the mendicant means to strike off his head and offer him, and so "
                  "master the vetala and rule unchallenged.")},
    ],
    "beats": [
        ("In the city of Ujjain reigned Vikramaditya, a king whose justice was sung from the "
         "mountains to the sea. For many days a mendicant — Kshantishila, a yogi of grave and "
         "patient bearing — came to his court, spoke no request, but placed in the king's hand "
         "a single ripe fruit, bowed, and departed. And each day, courteous, the king passed "
         "the fruit to his treasurer and thought no more of it."),
        ("One morning a palace monkey snatched the fruit from the king's hand and bit it — and "
         "it broke upon the marble, and from its heart rolled a jewel of impossible water, worth "
         "a province. The king bade his treasury opened: every fruit the yogi had given held "
         "such a gem. Vikramaditya marvelled. \"What manner of man gives a kingdom's ransom, day "
         "upon day, and asks nothing in return?\""),
        ("Summoned before the throne, Kshantishila bowed low. \"Great king, I have laboured long "
         "for a power that comes but once in an age — and it will come to me only if a king, by "
         "his own hand, brings me a certain corpse. On the fourteenth night of this dark "
         "fortnight, come alone to the great burning-ground, to the lone simsapa tree where a "
         "body hangs, and bear it to me. That is all I ask — for all I have given.\""),
    ],
    "mini_agents": {
        "kshantishila": {
            "bible": "A yogi of studied calm and pious words; warm surface, cold depths.",
            "answer_intro": "Kshantishila folds his hands, his voice smooth as oil.",
            "unknown": ("The mendicant's smile does not reach his eyes. \"A holy rite, great "
                        "king — no more. Sacred things are not for idle telling. You have all "
                        "but given your word; let that be enough between us.\""),
        },
    },
    # Prologue "choices" are the king's STANCE toward the mendicant (sets mendicant_suspicion).
    "choices": [
        {"id": "A", "label": "A king's word is his bond — I accept, and think no ill."},
        {"id": "B", "label": "I accept — but I will watch this too-generous holy man."},
        {"id": "C", "label": "First, ask him plainly what the rite is for."},
    ],
    "stance_reactions": {
        "A": {"suspicion": "low", "expression": "intense",
              "line": ("\"A king's word is his bond,\" said Vikramaditya, \"and I will think no "
                       "ill of a generous man.\"" + _JOURNEY_AND_BETAAL)},
        "B": {"suspicion": "high", "expression": "intense",
              "line": ("\"I accept,\" said the king, \"but a gift without a reason is a debt in "
                       "disguise. I shall keep this holy man in the corner of my eye.\"" + _JOURNEY_AND_BETAAL)},
        "C": {"suspicion": "medium", "expression": "intense",
              "line": ("\"First tell me plainly,\" said the king, \"to what end this rite?\" The "
                       "yogi only smiled and spoke of holy things not meant for the telling — and "
                       "the king, his word already half-given, let it pass." + _JOURNEY_AND_BETAAL)},
    },
}


# ===========================================================================
# Tale 1 — The Transposed Heads  (identity)
# ===========================================================================
TRANSPOSED_HEADS = {
    "id": "transposed-heads",
    "title": "The Transposed Heads",
    "scene_id": "betaal.tale.transposed-heads",
    "background": "cremation-ground-night",
    "ambient": "low wind, a far owl, the tick of cooling embers",
    "voice_profiles": {"betaal": "betaal_sonorous", "vikramaditya": "king_regal",
                       "madanasundari": "f_grave", "dhavala": "m_measured"},
    "canon_facts": [
        {"chunk_id": "th.journey", "speaker": "narrator",
         "characters_present": ["madanasundari", "dhavala", "brother"],
         "themes": ["devotion", "journey"],
         "text": ("Madanasundari journeyed with her husband Dhavala and her young brother "
                  "to a temple of the Goddess upon a hill.")},
        {"chunk_id": "th.deaths-order", "speaker": "narrator",
         "characters_present": ["dhavala", "brother"],
         "themes": ["identity", "fate", "death"],
         "text": ("Within the shrine Dhavala, in a rapture none living can explain, struck "
                  "off his own head before the Goddess. The brother, finding him so, took up "
                  "the sword and did the like. The wife was still outside and saw neither blow.")},
        {"chunk_id": "th.swap", "speaker": "narrator",
         "characters_present": ["madanasundari"],
         "themes": ["identity", "error"],
         "text": ("The Goddess granted that Madanasundari might rejoin each head to its body "
                  "and they would live. Weeping in the dark, she set the husband's head upon "
                  "the brother's body, and the brother's head upon the husband's.")},
        {"chunk_id": "th.revived", "speaker": "narrator",
         "characters_present": ["madanasundari", "dhavala", "brother"],
         "themes": ["identity", "dilemma"],
         "text": ("Both men breathed, and rose, and stood — whole, and wrong. Each now bore "
                  "one man's head upon the other man's body.")},
    ],
    "beats": [
        ("A tale, then, to shorten the road — though for you, little king, I suspect no road "
         "is short enough. Listen. There was a maiden, Madanasundari, whose devotion to her "
         "husband Dhavala was the envy of the gods. On a pilgrimage she travelled with her "
         "husband and her young brother to a temple of the Mother. Her husband entered first "
         "to make his offering... and in a rapture none living can explain, struck off his own "
         "head before the Goddess. The brother, finding him so, took up the sword and did the "
         "like. And the wife, finding two she loved lying headless, raised the blade to follow "
         "them. But the Mother stayed her hand: 'Set each head to its body, child, and they "
         "shall live.' So, in the dark, with shaking hands and streaming eyes, she set the "
         "husband's head upon the brother's body, and the brother's head upon the husband's. "
         "And both men breathed, and rose, and stood — whole, and wrong."),
    ],
    "mini_agents": {
        "madanasundari": {
            "bible": ("The devoted wife. Grief held like a drawn bow. Speaks plainly, with the "
                      "weariness of one who has wept past weeping."),
            "answer_intro": "Madanasundari lifts her eyes, hollow with grief.",
            "unknown": ("\"That I cannot tell you, my lord. I came upon them already fallen — "
                        "I was outside the shrine, and saw neither blow. I know only what I did "
                        "after, with my own shaking hands.\""),
        },
        "dhavala": {
            "bible": "The husband. Calm certainty; he knows his own mind and vow.",
            "answer_intro": "The man bearing Dhavala's head answers.",
            "unknown": ("\"I cannot say. I know my own thoughts, my own name, the vow I made "
                        "her — but not what you ask.\""),
        },
    },
    "riddle": ("So tell me, O fountain of justice — and be careful, your skull is listening — "
               "which of these two men is now her husband? The body that bears his head... or "
               "the body that was his, beneath a stranger's face?"),
    "choices": [
        {"id": "A", "label": "The man bearing her husband's HEAD is her husband."},
        {"id": "B", "label": "The man with her husband's BODY is her husband."},
        {"id": "C", "label": "Neither — fate has unmade the marriage."},
    ],
    "canonical": "A",
    "reactions": {
        "A": {"expression": "amused", "trust_delta": 6,
              "memory_note": ("The king judged by the seat of identity, not the flesh — he reasons "
                              "from the person, not the thing."),
              "line": ("Hah. The head, you say. And you are right by the old reckoning, little "
                       "king: the head is the chief of the limbs — it wears the name, it holds the "
                       "self, it speaks the vow. Where the head goes, there goes the man. The "
                       "Mother herself would nod. Most men clutch at the body, at what they can "
                       "hold. You looked for the person where a person lives. ...I am almost "
                       "disappointed; I had a barb ready.")},
        "B": {"expression": "intense", "trust_delta": 0,
              "memory_note": "Judged by the body/the familiar — values the tangible over the abstract self.",
              "line": ("The body! The strong arms, the familiar shape — what a grieving eye would "
                       "seize. But when she spoke to him after, and he answered with his own "
                       "memories in another man's voice — to whom was she speaking? The vow lives "
                       "in the head, little king, not the shoulders. The old judges would mark you "
                       "wrong... though I confess I like a king who argues for a remembered embrace.")},
        "C": {"expression": "intense", "trust_delta": 3,
              "memory_note": "Refuses false binaries; dissolves dilemmas rather than choose — clever, evasive, principled.",
              "line": ("Bold! You cut the knot rather than untie it. There is a hard mercy in it — "
                       "but a king who frees a faithful wife of all bond by a clerk's logic may "
                       "free himself of much else besides. The tale asks you to choose, not to "
                       "escape. Still... you made me think, and that is rarer than a right answer.")},
    },
}

# ===========================================================================
# Tale 2 — The Four Brahmins and the Lion  (wisdom vs. cleverness)
# ===========================================================================
LION = {
    "id": "four-brahmins-lion",
    "title": "The Four Brahmins and the Lion",
    "scene_id": "betaal.tale.lion",
    "background": "forest-clearing-night",
    "ambient": "night insects, a creaking branch, far-off jackals",
    "voice_profiles": {"betaal": "betaal_sonorous", "vikramaditya": "king_regal",
                       "tree_climber": "m_plain", "first_brahmin": "m_proud"},
    "canon_facts": [
        {"chunk_id": "lion.bones", "speaker": "narrator",
         "characters_present": ["first_brahmin", "tree_climber"],
         "themes": ["knowledge", "hubris"],
         "text": ("Four brahmins, learned past sense, crossed a forest and found the bleached "
                  "bones of a lion, and resolved to show what their study was worth.")},
        {"chunk_id": "lion.making", "speaker": "narrator",
         "characters_present": ["first_brahmin", "tree_climber"],
         "themes": ["knowledge", "craft"],
         "text": ("One drew the bones into a skeleton, one clothed it in flesh and hide, one "
                  "filled it with blood and the vessels of breath.")},
        {"chunk_id": "lion.climber-reason", "speaker": "tree_climber",
         "characters_present": ["tree_climber"],
         "themes": ["wisdom", "caution"],
         "text": ("The plain man who merely followed saw where it led — 'It is a lion, and "
                  "learning that will not stop to ask is death' — said so, was laughed at, and "
                  "climbed a tree.")},
        {"chunk_id": "lion.devour", "speaker": "narrator",
         "characters_present": ["tree_climber"],
         "themes": ["consequence"],
         "text": ("The fourth spoke the word of life. The lion rose and devoured the three who "
                  "had made it, while the plain man watched from the branches.")},
    ],
    "beats": [
        ("Four brahmins, learned past sense, crossed a forest and found the bleached bones of a "
         "lion. 'Behold,' said the first, 'a chance to show what our years of study are worth.' "
         "One drew the scattered bones into a skeleton. The second clothed it in flesh and hide. "
         "The third filled it with blood and breath. And the fourth raised his hand to give it "
         "life. 'Stop,' said a fifth, a plain man who had merely followed them, 'it is a lion.' "
         "They laughed at him. He climbed a tree. The fourth spoke the word of life... and the "
         "lion rose, and ate the three who had made it, while the plain man watched from above."),
    ],
    "mini_agents": {
        "tree_climber": {
            "bible": "The plain man who followed; cautious, and alive.",
            "answer_intro": "The man in the tree calls down softly.",
            "unknown": ("\"That I never saw, lord. I know only what I watched from this branch — "
                        "and that was enough.\""),
        },
        "first_brahmin": {
            "bible": "Proud of his craft even in death; blind to its end.",
            "answer_intro": "The first brahmin, proud even in memory, answers.",
            "unknown": "\"I cannot say what was in that coward's head — I was busy with my art.\"",
        },
    },
    "riddle": ("Three men of great learning lie in a lion's belly, little king. Tell me — which "
               "of them was the greatest fool?"),
    "choices": [
        {"id": "A", "label": "The fourth — who gave it life knowing it was a lion."},
        {"id": "B", "label": "All three equally — they built it together."},
        {"id": "C", "label": "The tree-climber, the coward who did not stop them."},
    ],
    "canonical": "A",
    "reactions": {
        "A": {"expression": "intense", "trust_delta": 5,
              "memory_note": "values judgment over raw capability — wary of power used without a pause.",
              "line": ("Just so. Knowledge is a sword; the fourth swung it with his eyes open and "
                       "his sense shut. Learning that will not pause to ask 'should I' is the most "
                       "dangerous thing in any age.")},
        "B": {"expression": "amused", "trust_delta": 2,
              "memory_note": "spreads blame evenly; sees collective responsibility.",
              "line": ("A fair severity — each laid a stone in the road to their own grave. Yet "
                       "one still might have stopped at the last step and did not; the hand that "
                       "acts last owns the deed. Half-right, which from you I will take.")},
        "C": {"expression": "amused", "trust_delta": 0,
              "memory_note": "prizes action; suspicious of caution — may mock prudence as cowardice.",
              "line": ("Ha! You would blame the one man who lived? Careful, king — a world that "
                       "mocks the cautious for cowardice is a world that keeps reviving lions. "
                       "Wrong, by the old reckoning — though you have a king's taste for action.")},
    },
}

# ===========================================================================
# Tale 3 — The Three Suitors of the Dead Maiden  (desert & identity)
# ===========================================================================
THREE_SUITORS = {
    "id": "three-suitors",
    "title": "The Three Suitors of the Dead Maiden",
    "scene_id": "betaal.tale.three-suitors",
    "background": "river-ghat-night",
    "ambient": "river lapping at the steps, a distant temple bell, night birds",
    "voice_profiles": {"betaal": "betaal_sonorous", "vikramaditya": "king_regal",
                       "ash_keeper": "m_quiet", "reviver": "m_learned", "maiden": "f_soft"},
    "canon_facts": [
        {"chunk_id": "ts.three-love", "speaker": "narrator",
         "characters_present": ["ash_keeper", "reviver"],
         "themes": ["love", "rivalry"],
         "text": ("A merchant's daughter, lovely beyond saying, was loved by three men, and "
                  "she could wed but one.")},
        {"chunk_id": "ts.death", "speaker": "narrator",
         "characters_present": ["ash_keeper", "reviver"],
         "themes": ["death", "grief"],
         "text": ("Before any could win her, a serpent took her life.")},
        {"chunk_id": "ts.vigil", "speaker": "ash_keeper",
         "characters_present": ["ash_keeper"],
         "themes": ["devotion", "constancy"],
         "text": ("The second gathered the ashes that remained, made of them a shrine, and "
                  "lived beside it, asking nothing of the world.")},
        {"chunk_id": "ts.sage-mantra", "speaker": "reviver",
         "characters_present": ["reviver"],
         "themes": ["power", "revival"],
         "text": ("The third wandered to a sage, learned a word of power, returned, and from "
                  "the kept ashes raised her — living, whole.")},
        {"chunk_id": "ts.revived", "speaker": "narrator",
         "characters_present": ["ash_keeper", "reviver", "maiden"],
         "themes": ["dilemma"],
         "text": ("She stood living again, and all three claimed her — the one who burned her, "
                  "the one who kept her, the one who raised her.")},
    ],
    "beats": [
        ("A merchant's daughter, lovely beyond saying, was loved by three men, and she could "
         "wed but one. Before any could win her, a serpent took her life. The first, mad with "
         "grief, built her pyre and gave her ashes to the river. The second gathered what ashes "
         "remained and made of them a shrine, and lived beside it, eating nothing the world "
         "offered. The third wandered to a sage, learned a word of power, returned, and from the "
         "kept ashes raised her, living, whole. And all three claimed her — the one who burned "
         "her, the one who kept her, the one who raised her."),
    ],
    "mini_agents": {
        "ash_keeper": {
            "bible": "Gaunt with devotion; speaks of love as being, not deed.",
            "answer_intro": "The ash-keeper looks up from his shrine of ashes.",
            "unknown": "\"How she was raised, I cannot tell you — I never left her ashes to learn it.\"",
        },
        "reviver": {
            "bible": "Learned, proud of the deed that brought her back.",
            "answer_intro": "The reviver lifts his head, certain of his claim.",
            "unknown": "\"Her heart? That I never saw — I was at the sage's feet while others wept.\"",
        },
        "maiden": {
            "bible": "Newly returned from death; bewildered, grave.",
            "answer_intro": "The maiden, new-woken, speaks softly.",
            "unknown": ("\"I died, and I woke. Who loved me truest I cannot tell you — I witnessed "
                        "none of their grief.\""),
        },
    },
    "riddle": ("Three men, one woman, and death undone. Tell me, just king — whose wife is she now?"),
    "choices": [
        {"id": "A", "label": "The ash-keeper, who stayed and asked nothing."},
        {"id": "B", "label": "The reviver, who gave her life again."},
        {"id": "C", "label": "Let the maiden herself choose."},
    ],
    "canonical": "A",
    "reactions": {
        "A": {"expression": "amused", "trust_delta": 6,
              "memory_note": "sees love as constancy, not grand acts; reasons by the duty an act implies.",
              "line": ("Yes — and here the clever stumble. The one who raised her acted as a "
                       "father gives life; the one who burned her did a son's last duty. By their "
                       "own deeds they became her parent and her child — and only the one who "
                       "simply stayed, asking nothing, remained a husband. You saw it.")},
        "B": {"expression": "intense", "trust_delta": 0,
              "memory_note": "takes the obvious reading; rewards grand action over quiet duty.",
              "line": ("The obvious crown — and the wrong head. To give life is a father's gift, "
                       "not a husband's. He made himself her parent and argued himself out of her "
                       "bed. The tale is crueller and cleverer than it looks, little king.")},
        "C": {"expression": "amused", "trust_delta": 4,
              "memory_note": "grants agency; resists treating a person as a prize to be awarded.",
              "line": ("Now you sound like a king worth the name — though the old judges would say "
                       "you dodged their question. Still: a man who remembers a woman is a person, "
                       "not a purse, will rule better than one who answers riddles cleanly.")},
    },
}

# ===========================================================================
# Tale 4 — Viravara, the Loyal Servant  (loyalty vs. morality; bridge to Phase 2)
# ===========================================================================
VIRAVARA = {
    "id": "viravara",
    "title": "Viravara, the Loyal Servant",
    "scene_id": "betaal.tale.viravara",
    "background": "palace-gate-midnight",
    "ambient": "wind through an iron gate, a woman weeping somewhere unseen",
    "voice_profiles": {"betaal": "betaal_sonorous", "vikramaditya": "king_regal",
                       "viravara": "m_grave", "son": "m_young"},
    "canon_facts": [
        {"chunk_id": "vir.service", "speaker": "narrator",
         "characters_present": ["viravara"],
         "themes": ["duty", "service"],
         "text": ("Viravara took service with a king and was paid a fortune to, it seemed, do "
                  "nothing at all.")},
        {"chunk_id": "vir.fortune", "speaker": "viravara",
         "characters_present": ["viravara"],
         "themes": ["fate", "sacrifice"],
         "text": ("One night a woman wept in the dark — the kingdom's own Fortune — who "
                  "foretold the king would die within days unless a life were freely given.")},
        {"chunk_id": "vir.consent", "speaker": "narrator",
         "characters_present": ["viravara", "son"],
         "themes": ["sacrifice", "family"],
         "text": ("Viravara woke his family. The boy offered his own neck that the king might "
                  "live; the wife would follow her child; and Viravara would follow them, then "
                  "fall on his own sword for his lord.")},
        {"chunk_id": "vir.king-anguish", "speaker": "narrator",
         "characters_present": ["rupasena"],
         "themes": ["remorse", "restraint"],
         "text": ("The king had crept out and watched it all from the shadows, and could not "
                  "bear what his service had cost.")},
    ],
    "beats": [
        ("Viravara took service with a king and was paid a fortune to, it seemed, do nothing. "
         "One night a woman wept in the dark — the kingdom's own Fortune, who foretold the king "
         "would die within days unless a life were freely given to the Goddess. Viravara went "
         "home and woke his son, his wife. The boy offered his own neck that the king might "
         "live; the wife would follow her child; Viravara would follow them all, and then fall "
         "on his own sword for his lord. And the king, who had crept out and watched it from the "
         "shadows, could not bear what his service had cost."),
    ],
    "mini_agents": {
        "viravara": {
            "bible": "Duty as a debt beyond price; grave, devoted, unflinching.",
            "answer_intro": "Viravara stands straight, his hand near his sword.",
            "unknown": ("\"What my lord saw or felt that night, I cannot tell you — I never knew "
                        "he watched.\""),
        },
        "son": {
            "bible": "Young, calm, certain; offers his life without a tremor.",
            "answer_intro": "The boy answers, steady beyond his years.",
            "unknown": ("\"Whether the king deserved it was not mine to weigh — and I never saw "
                        "his face that night.\""),
        },
    },
    "riddle": ("A servant who would spend his son, his wife, and himself for a master who asked "
               "nothing of him. Tell me, king — whose act was the noblest? And quieter, where "
               "your skull can hear it: was such loyalty right at all?"),
    "choices": [
        {"id": "A", "label": "The son — he gave the most, having lived the least."},
        {"id": "B", "label": "The king — noblest for refusing to be served at such a price."},
        {"id": "C", "label": "Such total loyalty is not right — no master is owed a man's children."},
    ],
    "canonical": "B",
    "reactions": {
        "A": {"expression": "grave", "trust_delta": 4,
              "memory_note": "honours the greatest sacrifice; moved by purity of devotion.",
              "line": ("The young throat offered first and freest — yes, many a judge has crowned "
                       "him. To give a whole unlived life... there is a terrible purity in it.")},
        "B": {"expression": "intense", "trust_delta": 6,
              "memory_note": "weighs a leader by what he refuses to spend — power as restraint.",
              "line": ("Ah. You honour the one who refused the gift. A throne that will not climb "
                       "over the bodies of the loyal is a rare throne. The old tellers often "
                       "judged the same — a king who counts his servants' lives dearer than his own.")},
        "C": {"expression": "grave", "trust_delta": 6,
              "memory_note": "questions loyalty owed to the undeserving — primed for the Mahabharata (Karna).",
              "line": ("...You may be the first king to say it to me plainly. Hold that thought, "
                       "little king. There are tales coming — older, bloodier than this folk-fire — "
                       "where a great man gives such loyalty to an unworthy lord, and the whole "
                       "world burns for it. I wonder what you will say to him.")},
    },
}

# ===========================================================================
# Tale 5 — The Child Who Laughed at Death  (betrayal — THE HOOK; placed last)
# ===========================================================================
CHILD_WHO_LAUGHED = {
    "id": "child-who-laughed",
    "title": "The Child Who Laughed at Death",
    "scene_id": "betaal.tale.child-who-laughed",
    "hook": True,
    "tone": "dark; atmospheric not graphic (13+)",
    "background": "sacrificial-court-dawn",
    "ambient": "low chanting, a guttering torch, a single crow",
    "voice_profiles": {"betaal": "betaal_sonorous", "vikramaditya": "king_regal",
                       "boy": "m_child", "father": "m_broken"},
    "canon_facts": [
        {"chunk_id": "cwl.price", "speaker": "narrator",
         "characters_present": ["boy", "father"],
         "themes": ["power", "sacrifice"],
         "text": ("A king sought a power that demanded a price: a boy without blemish — "
                  "beautiful, brave, whole — offered freely to the Goddess.")},
        {"chunk_id": "cwl.sale", "speaker": "narrator",
         "characters_present": ["boy", "father"],
         "themes": ["betrayal", "poverty"],
         "text": ("A starving brahmin and his wife took the king's gold and led their only "
                  "son themselves to the altar.")},
        {"chunk_id": "cwl.laugh", "speaker": "narrator",
         "characters_present": ["boy", "father"],
         "themes": ["betrayal", "dharma"],
         "text": ("The king raised the sword. The boy looked slowly round at them all — and "
                  "laughed, a clear, ringing laugh — then bared his throat.")},
        {"chunk_id": "cwl.father-shame", "speaker": "father",
         "characters_present": ["father"],
         "themes": ["shame", "remorse"],
         "text": ("The father could not meet his son's eyes, and knew he had sold the one thing "
                  "no gold could ever buy back.")},
    ],
    "beats": [
        ("One more, little king, before the night gives you up — and there is no mischief in "
         "this one. A king once sought a power that demanded a price: a boy without blemish, "
         "beautiful and brave, offered freely to the Goddess. No noble would give a son, so "
         "heralds went out with gold. And a brahmin and his wife, who had not eaten in days, "
         "who had nothing in the world but one child... took the gold. They led him themselves "
         "to the altar. The king raised the sword. And the boy looked slowly round at them "
         "all... and laughed. A clear, ringing laugh. Then he bared his throat."),
    ],
    "mini_agents": {
        "boy": {
            "bible": "Calm, clear-eyed, beyond fear or bitterness now; will not hand you the answer.",
            "answer_intro": "The boy meets your eyes, unafraid.",
            "unknown": "\"Ask the living why, my lord. I am busy dying.\"",
        },
        "father": {
            "bible": "Broken by shame; cannot meet anyone's eyes.",
            "answer_intro": "The father speaks without looking up.",
            "unknown": ("\"Why he laughed... I saw it, lord, but I cannot tell you what was in "
                        "his heart. I had already sold my right to know him.\""),
        },
    },
    "riddle": ("The blade above his throat, his own mother's gold still warm in the priest's "
               "hand — and he laughed. Tell me, just king, and tell me true: why did the child "
               "laugh?"),
    "choices": [
        {"id": "A", "label": "Because every protector had become his destroyer."},
        {"id": "B", "label": "Because he was brave — a holy soul unafraid, welcoming release."},
        {"id": "C", "label": "Because he saw the sheer absurdity of it — madness or a height beyond fear."},
    ],
    "canonical": "A",
    "reactions": {
        "A": {"expression": "grave", "trust_delta": 8,
              "memory_note": "grasps that the powerful owe protection to the helpless; betrayal by guardians is the deepest wrong.",
              "line": ("Yes. A babe is kept by its mother, a child by its king, all souls by the "
                       "gods. His mother sold him; his king lifted the knife; the gods watched. "
                       "Where, in all that courtyard, was a single guardian left? He laughed "
                       "because every hand meant to shield him had turned to steel. ...You "
                       "understood him, little king. Hold that close — you will need it before "
                       "this night is done.")},
        "B": {"expression": "intense", "trust_delta": 3,
              "memory_note": "reads courage where there is indictment; gentle but misses the cruelty.",
              "line": ("A gentle reading, and not a foolish one — some children do meet death "
                       "like saints. But this laugh was not peace; it was an indictment. He did "
                       "not rise above the world — he saw it plainly and named it. Half-true, king.")},
        "C": {"expression": "grave", "trust_delta": 2,
              "memory_note": "looks away from hard truths about power — merciful but evasive.",
              "line": ("Madness, you say? It is always easier to call a thing madness than to "
                       "admit it is an accusation we have earned. He was the sanest soul in that "
                       "courtyard. Wrong, I think — but you flinched from the cruelty of the true "
                       "answer, and that flinch is its own small mercy.")},
    },
    # Spoken immediately after this tale's judgment: the hook into the meta-arc climax.
    "hook_line": ("\"You asked me why a child laughs as his guardians betray him. Now answer "
                  "this, while your skull still sits on your shoulders: a holy man sent you — a "
                  "king — into a field of the dead to carry a corpse on your own back. Have you "
                  "truly never wondered why?\""),
}

# ===========================================================================
# Climax — The Mendicant's Circle  (the meta-arc payoff; docs/13)
# ===========================================================================
# Betaal warns the king of Kshantishila's plot. HOW fully he warns depends on the trust
# the player built across the tales (climax_tier); the prologue stance flavours it
# (mendicant_suspicion). The ending branches on the final choice AND the tier.
CLIMAX = {
    "id": "climax",
    "title": "The Mendicant's Circle",
    "kind": "climax",
    "scene_id": "betaal.climax",
    "background": "cremation-ground-circle-night",
    "ambient": "a low chant, fire-crackle, the smell of ash and blood",
    "voice_profiles": {"betaal": "betaal_sonorous", "vikramaditya": "king_regal",
                       "narrator": "sutradhar", "kshantishila": "m_unctuous"},
    "suspicion_aside": {
        "high": ("\"You felt it from the first, king — the gift too rich, the smile too smooth. "
                 "You were right to watch him.\" "),
        "medium": ("\"You asked him once to his face what he wanted, and let it pass. Do not let "
                   "it pass again.\" "),
        "low": ("\"You took him for a holy friend and me for a ghost's idle malice. Set that "
                "aside now, and listen as you have never listened.\" "),
    },
    "warning": {
        "high": ("Betaal's voice drops, all mischief gone. \"Hear me, for I have come to want "
                 "you living, and that surprises us both. This holy man did not give you a "
                 "fortune for nothing. His rite needs more than a corpse — it needs a king's "
                 "head. When you set me down he will bid you bow full-length before the circle, "
                 "in reverence. Do NOT. Tell him a king bows to no one, and ask HIM to show you "
                 "how it is done — and when he lowers his head, end it. I have watched a hundred "
                 "kings die for the sake of good manners. I would not watch you be the "
                 "hundred-and-first.\""),
        "mid": ("Betaal's voice hardens. \"You have earned a warning, so take it: the holy man "
                "wants your head, not the corpse. He will ask you to bow — and a bowed neck is "
                "an offered neck. Think how a clever king turns such a trap, and be quick about "
                "it.\""),
        "low": ("Betaal says only, coldly, \"You spent our long night being a small man, so I "
                "will spend few words on you: the mendicant means your death, and your courtesy "
                "is his knife. Bow to no one tonight. Whether you are clever enough to live, I "
                "no longer much care.\""),
    },
    "choices": [
        {"id": "A", "label": "Ask the mendicant to show you the prostration first — then strike."},
        {"id": "B", "label": "Refuse to bow, and face him openly."},
        {"id": "C", "label": "Bow before the circle as the holy man bids."},
    ],
    "endings": {
        "A": {
            "high": ("\"Show me, holy one, how a king should bow,\" said Vikramaditya — and as "
                     "Kshantishila, smiling, bent his head to the stone, the king's sword fell. "
                     "The power the mendicant had hunted across a lifetime broke loose and "
                     "settled upon the one who had earned it: the gods named Vikramaditya lord "
                     "of the vetalas and emperor of his age. And Betaal, freed at last of his "
                     "tree, rose into the dark — and paused. \"You were worth the carrying, "
                     "king. Should you ever have need of a riddle again... you know which tree.\""),
            "mid": ("Something in Betaal's words had warned you enough. \"Show me first how it "
                    "is done,\" you said — and when the mendicant bent, you understood, and "
                    "struck. You live, and the power is yours, though it tastes of luck as much "
                    "as wisdom. Betaal departs with a backward glance that is almost respect."),
            "low": ("You scarcely deserved to guess it, yet guess it you did — 'show me first' — "
                    "and the falling blade was the mendicant's to suffer, not yours. You live, "
                    "king, by a mercy you did little to earn. Betaal goes without a word."),
        },
        "B": {
            "any": ("\"A king bows to no one,\" you said, and named his treachery to his face. "
                    "Unmasked, Kshantishila's piety fell away — and so did he, fleeing into the "
                    "smoke with the once-in-an-age power still uncaught. You live, and you are "
                    "just, and you are empty-handed. Betaal snorts. \"Honest, and poorer for it. "
                    "There are worse epitaphs, king.\""),
        },
        "C": {
            "high": ("You began to bow — and Betaal, against his own long freedom, SHRIEKED. "
                     "The blade was already falling; you threw yourself aside and it bit stone "
                     "where your neck had been. The rite shattered. You live — shaking — by the "
                     "grace of a ghost who chose you over his own escape. \"I told you plainly,\" "
                     "Betaal breathes, \"and still you nearly fed the fire. Live. And learn, at "
                     "last, to listen.\""),
            "low": ("You bowed — for he had been so generous, and you had never learned to "
                    "doubt. The blade sang down. Only blind fortune and a foot slipping in the "
                    "ash spared your life, and the cost was carved into you forever. Somewhere "
                    "above, a freed spirit did not look back. A king who will not listen does "
                    "not often get a second tale."),
        },
    },
    "outcomes": {"A": "king_triumphant", "B": "just_but_empty", "C": "narrow_escape"},
}


# Season order (locked 2026-06-15): Prologue opens; the 5th tale is the hook; Climax closes.
SEASON_ORDER = ["prologue", "transposed-heads", "four-brahmins-lion", "three-suitors",
                "viravara", "child-who-laughed", "climax"]

TALES = {
    "prologue": PROLOGUE,
    "transposed-heads": TRANSPOSED_HEADS,
    "four-brahmins-lion": LION,
    "three-suitors": THREE_SUITORS,
    "viravara": VIRAVARA,
    "child-who-laughed": CHILD_WHO_LAUGHED,
    "climax": CLIMAX,
}

# A new session opens on the Prologue (the frame story).
DEFAULT_TALE = "prologue"
