# -*- coding: utf-8 -*-
"""Hindi (Devanagari) authored content for Katha Phase 1.

Faithful translations of all authored lines in tales.py.
Keys are suffixed _hi: beats_hi, riddle_hi, choices_hi, reactions_hi,
stance_reactions_hi, warning_hi, suspicion_aside_hi, endings_hi, hook_line_hi.

Sarvam Bulbul v3 reads Devanagari natively when language='hi-IN' is passed.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Shared journey block (Prologue -> Tale 1 transition)
# ---------------------------------------------------------------------------
_JOURNEY_HI = (
    "\n\nAur is prakar, apne vachan par dridh, krishnapaksh ki chaudahvin raat ko "
    "raja akele shmashan mein gaya -- jalti chitaon ke beech, mandrate siyaaron ke "
    "paas, ant ki gandh wale dhuyen ke paar -- us ekaaki shinsapa vriksh tak jahan "
    "ek shav lata tha. Usne use neeche utara aur apne kandhe par utha liya. Aur uski "
    "peeth par us mrit deh ne aankhen kholin aur hansi. 'Rajan, hamare samne lamba "
    "rasta hai, aur main maunam mein bura sathi hun -- to chalo main tumhe ek katha "
    "sunata hun. Par hamari raah ka niyam suno: yadi main paheli puchun aur tum uttar "
    "jante ho phir bhi chup rahe, to tumhara mastak sau tukadon mein fat jaayega. "
    "Uttar do, aur main wapas apne vriksh par ud jaunga. ...To... shuru karen?'"
)

# ---------------------------------------------------------------------------
# PROLOGUE
# ---------------------------------------------------------------------------
PROLOGUE_HI: dict = {
    "beats_hi": [
        ("Ujjayini nagari mein Vikramaditya raj karte the -- ek raja jiska nyay "
         "pahadon se samudra tak gaya jata tha. Kai dinon se ek sanyasi -- "
         "Kshantishil, gambhir aur dhairyavaan -- unke darbaar mein aata tha, kuch "
         "maangta nahi tha, par raja ke haath mein ek paka hua phal rakh deta tha, "
         "jhukkar pranaam karta aur chala jaata. Raja bhi shishtata se wah phal apne "
         "khazaanchi ko de dete aur kuch nahi sochte."),
        ("Ek subah mahal ke bander ne raja ke haath se phal chheen liya aur kaat "
         "liya -- aur wah sangmarmar par gira aur tuta, aur uske hriday se ek "
         "amoolya ratna ludka, jo ek praant ki keemat ka tha. Raja ne apna khazana "
         "khulwaya: us yogi ke har phal mein aisa ratna tha. Vikramaditya chakit "
         "reh gaye. 'Yeh kaisa manushya hai jo din-par-din ek rajya ki keemat deta "
         "hai aur kuch nahi maangta?'"),
        ("Sinhaasan ke samne bulaaye jaane par Kshantishil ne jhukkar pranaam kiya. "
         "'Maharaj, maine bahut varshon tak ek aisi shakti ke liye sadhana ki hai "
         "jo yug mein ek baar aati hai -- aur wah mujhe milegi tabhi jab koi raja "
         "apne haathon se ek nishchit shav ko mere paas laye. Is krishnapaksh ki "
         "chaudahvin raat ko, akele shmashan mein jao, us ekaaki shinsapa vriksh par "
         "jahan ek shav lata ho -- use mere paas le aao. Bas itna hi maangta hun -- "
         "jo kuch diya hai uske badle.'"),
    ],
    "choices_hi": [
        {"id": "A", "label": "Raja ka vachan uska praan hai -- main sveekaar karta hun, aur koi bura nahi sochta."},
        {"id": "B", "label": "Main sveekaar karta hun -- par is atiudar sadhu par nazar rakhunga."},
        {"id": "C", "label": "Pahle usse seedha puchhunga ki yeh anushthaan kis liye hai."},
    ],
    "stance_reactions_hi": {
        "A": {"suspicion": "low", "expression": "intense",
              "line": ("'Raja ka vachan uska praan hai,' Vikramaditya bole, 'aur main ek "
                       "udar manushya ke baare mein bura nahi sochunga.'"
                       + _JOURNEY_HI)},
        "B": {"suspicion": "high", "expression": "intense",
              "line": ("'Main sveekaar karta hun,' raja ne kaha, 'par bina kaaran ka uphaar "
                       "ek chhupa hua rin hota hai. Main is sadhu ko apni aankh ke kone mein "
                       "rakhunga.'" + _JOURNEY_HI)},
        "C": {"suspicion": "medium", "expression": "intense",
              "line": ("'Pahle mujhe batao,' raja ne kaha, 'yeh anushthaan kis liye hai?' "
                       "Yogi keval muskuraya aur pavitra baaten karne laga jo kahne yogya "
                       "nahi thin -- aur raja, apna vachan aadha de chuka, maan gaya."
                       + _JOURNEY_HI)},
    },
}

# ---------------------------------------------------------------------------
# TALE 1 -- The Transposed Heads
# ---------------------------------------------------------------------------
TRANSPOSED_HEADS_HI: dict = {
    "beats_hi": [
        ("Ek katha, rajan -- raasta chhota karne ke liye, haalaanki tumhare liye "
         "koi raasta chhota nahi. Suno. Ek kanya thi, Madansundari, jiski "
         "pati-bhakti devtaon ko bhi irshyaalu banati thi. Tirth-yaatra par wah "
         "apne pati Dhaval aur apne chhote bhai ke saath Maa ke mandir gayi. Pati "
         "pahle bheetar gaya apni bhent chadhaane ko... aur ek aisa parmaanand "
         "jo koi jeevit nahi samjha sakta, devi ke samne apna hi sir kaat liya. "
         "Bhai ne use yun dekha to talwaar uthayi aur waisa hi kiya. Patni, jo "
         "bahar thi, dono ko sir kate pada dekhkar khud par vaar karne lagi. Par "
         "Maa ne uska haath thaam liya: 'Bachchi, har sir uske sharir se jod de, "
         "weh ji uthenge.' To, andhere mein, kaampte haathon aur bahte aansuon "
         "ke saath, usne pati ka sir bhai ke dhadh par rakha, aur bhai ka sir "
         "pati ke dhadh par. Aur dono saansen lene lage, uthe, khade hue -- "
         "poore, aur galat."),
    ],
    "riddle_hi": (
        "To batao, he nyay ke srot -- aur savdhan rehna, tumhari khopdi sun rahi "
        "hai -- in dono mein se uska pati kaun hai? Jo uske pati ka sir dhaaran "
        "karta hai... ya jo uska sharir tha, kisi ajnabi ke chehre ke neeche?"
    ),
    "choices_hi": [
        {"id": "A", "label": "Jo uske pati ka sir dhaaran karta hai -- wahi uska pati hai."},
        {"id": "B", "label": "Jiske paas uske pati ka sharir hai -- wahi uska pati hai."},
        {"id": "C", "label": "Koi nahi -- bhagya ne vivaah hi tod diya."},
    ],
    "reactions_hi": {
        "A": {"expression": "amused", "trust_delta": 6,
              "memory_note": "Raja ne deh nahi, vyakti ki pahchaan se nirnay kiya.",
              "line": ("Ha! Sir, tumne kaha. Aur puraane vidhaan se tum sahi ho, rajan: sir "
                       "angon ka pradhan hai -- wahi naam dhaaran karta hai, wahi aatma ko, "
                       "wahi vachan ko. Jahan sir jaaye, wahan manushya jaaye. Maa bhi "
                       "sahmat hotin. Adhikaansh purush sharir ko pakdte hain, jo dikhta hai "
                       "use. Tumne vyakti ko khoja jahan vyakti rehta hai. ...Mujhe lagbhag "
                       "niraasha hui; mere paas ek kataaksh taiyaar tha.")},
        "B": {"expression": "intense", "trust_delta": 0,
              "memory_note": "Sharir se nirnay kiya -- jaana-pahchana ko maana.",
              "line": ("Sharir! Mazboot bhujayen, jaani-pehchani chavi -- jo ek dukhi aankh "
                       "pakdegi. Par jab usne usse baat ki aur usne kisi aur ki awaaz mein "
                       "apni yaadein sunaayin -- wah kisse baat kar rahi thi? Vachan sir mein "
                       "basta hai, rajan, kandhe mein nahi. Puraane nyayadheesh tumhe galat "
                       "thahraaate... haalaanki mujhe ek raja pasand hai jo ek jaani-pehchani "
                       "baahon ke liye bahas kare.")},
        "C": {"expression": "intense", "trust_delta": 3,
              "memory_note": "Jhoothe dwandwa se inkaar kiya; gaanth suljhaane ki jagah kaat di.",
              "line": ("Saahsik! Tumne gaanth suljhaane ki jagah kaat di. Ismein ek kadi daya "
                       "hai -- par ek raja jo ek nishthavaan patni ko ek lipikhak ki "
                       "tarqashastra se sabhi bandhan se mukht kar de, wah khud ko bhi bahut "
                       "kuch se mukht kar sakta hai. Katha tumse chunaav maangti hai, palaayan "
                       "nahi. Phir bhi... tumne mujhe sochne par majboor kiya, aur yeh sahi "
                       "uttar se adhik durlabh hai.")},
    },
}

# ---------------------------------------------------------------------------
# TALE 2 -- The Four Brahmins and the Lion
# ---------------------------------------------------------------------------
LION_HI: dict = {
    "beats_hi": [
        ("Chaar brahman, jo buddhi mein apni seema se bhi aage nikal gaye the, ek "
         "jungle se guzre aur unhe ek sher ki puraani haddiyaan mili. 'Dekho,' pehle "
         "ne kaha, 'hamare varshon ki sadhana dikhaane ka avsar.' Ek ne bikhri "
         "haddiyon ko kankaal mein joda. Doosre ne use maas aur chamde se dhaka. "
         "Teesre ne usme rakht aur shwas bhari. Aur chauthe ne haath uthaya jeevan "
         "dene ko. 'Ruko,' ek paanchve ne kaha, ek saadharan vyakti jo bas unke "
         "peeche aa gaya tha, 'yeh sher hai.' Weh upar hans pade. Wah ped par "
         "chadh gaya. Chauthe ne jeevan ka shabd bola... aur sher utha, aur un "
         "tinon ko kha gaya jinhone use banaya tha, jabki saadharan vyakti oopar "
         "se dekhta raha."),
    ],
    "riddle_hi": (
        "Teen mahaan gyaani ek sher ke pet mein hain, rajan. Mujhe batao -- unme "
        "sabse bada moorakh kaun tha?"
    ),
    "choices_hi": [
        {"id": "A", "label": "Chautha -- jisne jaante hue bhi sher ko jeevan diya."},
        {"id": "B", "label": "Teeno samaan roop se -- unhone milkar banaya."},
        {"id": "C", "label": "Ped par chadhne wala -- kaayar jisne unhe nahi roka."},
    ],
    "reactions_hi": {
        "A": {"expression": "intense", "trust_delta": 5,
              "memory_note": "Kshamata se adhik vivek ko mahatva deta hai.",
              "line": ("Bilkul sahi. Gyaan ek talwaar hai; chauthe ne use aankhen khuli aur "
                       "buddhi band karke chaali. Jo vidya yeh nahi poochhti ki 'karna chahiye "
                       "ya nahi' -- wah kisi bhi yug mein sabse khatarnak vastu hai.")},
        "B": {"expression": "amused", "trust_delta": 2,
              "memory_note": "Dosh samaan roop se baanta hai; samuhik uttardaayitwa dekhta hai.",
              "line": ("Uchit kathorta -- pratyekh ne apni qabr ke raaste mein ek patthar "
                       "rakha. Phir bhi ek abhi bhi antim kshan par ruk sakta tha aur nahi "
                       "ruka; jo ant mein karta hai wah karm ka swami hai. Aadha sahi, jo "
                       "tumse main le lunga.")},
        "C": {"expression": "amused", "trust_delta": 0,
              "memory_note": "Kriya ko mahatva deta hai; savdhani ko kaayarta maan sakta hai.",
              "line": ("Ha! Tum us ek vyakti ko dosh doge jo jeevit bacha? Savdhan, rajan -- "
                       "jo sansaar saavdhan ko kaayar kehta hai, wah sansaar sher paida karta "
                       "rehta hai. Puraane vidhaan se galat -- haalaanki tumhare paas ek raja "
                       "ki kriya ki ruchi hai.")},
    },
}

# ---------------------------------------------------------------------------
# TALE 3 -- The Three Suitors of the Dead Maiden
# ---------------------------------------------------------------------------
THREE_SUITORS_HI: dict = {
    "beats_hi": [
        ("Ek vanij ki kanya, jiski sundarata ka varnan shabdon mein na ho, teen "
         "purush usse prem karte the, aur wah ek se hi byaah sakti thi. Kisi ke "
         "bhaagya mein aane se pahle ek sarp ne uska praan le liya. Pehle ne, "
         "shok mein paagal hokar, uski chita jalayi aur raakh nadi ko de di. "
         "Doosre ne jo raakh bachi wah ekatrit ki, ek vedi banayi, aur uske paas "
         "rehne laga, sansaar se kuch na maangte hue. Teesre ek rishi ke paas "
         "gaya, ek jeevan-mantra seekha, lauta, aur un bachayi raakh se use "
         "jeevit, poorn kar diya. Aur tinon ne us par daawa kiya -- jisne jalaaya, "
         "jisne sambhala, jisne jilaya."),
    ],
    "riddle_hi": (
        "Teen purush, ek stri, aur mrityu ko palta gaya. Mujhe batao, nyaayi "
        "rajan -- ab wah kiski patni hai?"
    ),
    "choices_hi": [
        {"id": "A", "label": "Raakh sambhaalane wale ki -- jo ruka aur kuch na maanga."},
        {"id": "B", "label": "Jeevan dene wale ki -- jisne use phir jeevan diya."},
        {"id": "C", "label": "Kanya ko khud chunne do."},
    ],
    "reactions_hi": {
        "A": {"expression": "amused", "trust_delta": 6,
              "memory_note": "Prem ko sthirta maanta hai, bade karm ko nahi.",
              "line": ("Haan -- aur yahin chatur ladkhadaate hain. Jisne use jeevan diya, "
                       "usne ek pita ka kaam kiya; jisne jalaaya, usne ek putra ka antim "
                       "kartavya nibhaya. Apne hi karmon se weh uske pita aur putra ban gaye "
                       "-- aur keval wahi jo bas ruka, kuch na maangte hue, pati bana raha. "
                       "Tumne dekha.")},
        "B": {"expression": "intense", "trust_delta": 0,
              "memory_note": "Spasht uttar chuna; bade karm ko puruskrit karta hai.",
              "line": ("Spasht mukut -- aur galat sir. Jeevan dena pita ka uphaar hai, pati "
                       "ka nahi. Usne khud ko uska pita bana liya aur apne daave se bahar ho "
                       "gaya. Katha jitni dikhti hai usse adhik kroor aur chatoor hai, rajan.")},
        "C": {"expression": "amused", "trust_delta": 4,
              "memory_note": "Stri ko puruskaar nahi, vyakti maanta hai.",
              "line": ("Ab tum ek raja jaise lagte ho -- haalaanki puraane nyayadheesh kahte "
                       "ki tumne unka prashna taal diya. Phir bhi: jo raja yaad rakhe ki "
                       "stri ek vyakti hai, puruskaar nahi, wah usse behtar raaj karega jo "
                       "paheeliyan sundar dhang se suljhata hai.")},
    },
}

# ---------------------------------------------------------------------------
# TALE 4 -- Viravara, the Loyal Servant
# ---------------------------------------------------------------------------
VIRAVARA_HI: dict = {
    "beats_hi": [
        ("Viravara ne ek raja ki seva mein pravesh kiya aur ek bada vetan paya, yeh "
         "karne ke liye ki -- lagta tha -- kuch nahi. Ek raat andhere mein ek stri "
         "roi -- rajya ki apni Lakshmi -- jisne bhavisyawaani ki ki raja kuch dinon "
         "mein marega jab tak ki devi ko koi jeevan sweccha se na de. Viravara ghar "
         "gaya aur apne putra, apni patni ko jagaya. Baalak ne apni greeva prastut "
         "ki ki raja jeevit rahe; patni apne putra ke peechhe jaati; Viravara un "
         "sabke peechhe jaata, aur phir apne swami ke liye apni hi talwaar par "
         "girta. Aur raja, jo chhupkar sab dekh raha tha, wah sahan na kar saka "
         "jo uski seva ne chukaaya tha."),
    ],
    "riddle_hi": (
        "Ek sevak jo apna putra, apni patni, aur khud ko us swami ke liye luta de "
        "jisne usse kuch nahi maanga. Mujhe batao, rajan -- kiski kriya sarvochch "
        "thi? Aur dheere, jahan tumhari khopdi sun sake: kya aisi nishtha uchit thi?"
    ),
    "choices_hi": [
        {"id": "A", "label": "Putra ki -- usne sabse adhik diya, sabse kam jeekar."},
        {"id": "B", "label": "Raja ki -- jisne itni keemat par seva lene se inkaar kiya."},
        {"id": "C", "label": "Aisi poorn nishtha uchit nahi -- koi swami kisi ke bachche ka haqdar nahi."},
    ],
    "reactions_hi": {
        "A": {"expression": "grave", "trust_delta": 4,
              "memory_note": "Sarvochch balidan ko sammaan deta hai; bhakti ki pavitrta se prabhavit.",
              "line": ("Pahle aur sabse swatantr roop se prastut yuva kanth -- haan, kai "
                       "nyayadheeshon ne use hi mukut diya hai. Ek poora ajeeva jeevan dena... "
                       "ismein ek bhayaawah pavitrta hai.")},
        "B": {"expression": "intense", "trust_delta": 6,
              "memory_note": "Neta ko is baat se maapata hai ki wah kya lene se inkaar karta hai.",
              "line": ("Aah. Tum use sammaan dete ho jisne uphaar lene se inkaar kiya. Jo "
                       "rajya wafadaaron ki laashon par nahi chadhta wah durlabh rajya hai. "
                       "Puraane kathakaaron ne aksar aisa hi nirnay diya -- ek raja jo apne "
                       "sewakyon ke praan ko apne se adhik moolyvaan maanta ho.")},
        "C": {"expression": "grave", "trust_delta": 6,
              "memory_note": "Anuchit swami ki nishtha par prashn uthata hai -- Mahabharata ke liye taiyaar.",
              "line": ("...Tum shayad pehle raja ho jisne mujhse yeh seedhe kaha. Yeh vichaara "
                       "rakho, rajan. Aage kathayen aa rahi hain -- is lok-katha se puraani "
                       "aur khooni -- jahan ek mahaan purush aisi hi nishtha ek ayogya swami "
                       "ko deta hai, aur saara sansaar jalta hai. Main sochta hun tum usse "
                       "kya kahoge.")},
    },
}

# ---------------------------------------------------------------------------
# TALE 5 -- The Child Who Laughed at Death
# ---------------------------------------------------------------------------
CHILD_WHO_LAUGHED_HI: dict = {
    "beats_hi": [
        ("Ek aur, rajan, raat samapt hone se pahle -- aur ismein koi natkhatpan "
         "nahi hai. Ek raja ne ek aisi shakti chaahi jis ki keemat thi: ek nirdosh "
         "baalak -- sundar, saahasi, poorn -- jo sweccha se devi ko arpit ho. Kisi "
         "rajputra ne putra na diya, to sone ke saath herold nikle. Aur ek brahman "
         "aur uski patni, jinhone kai dinon se kuch na khaya tha, jinke paas sansaar "
         "mein bas ek bachcha tha... sona le liya. Weh swayam use vedi tak le gaye. "
         "Raja ne talwaar uthayi. Aur baalak ne dheere-dheere sabki or dekha... aur "
         "hansa. Ek spasht, khankhanati hansi. Phir usne apna gala saamne kar diya."),
    ],
    "riddle_hi": (
        "Uske gale ke oopar talwaar, uski maa ka sona pujari ke haath mein abhi "
        "garam -- aur wah hansa. Mujhe batao, nyaayi rajan, aur sach batao: baalak "
        "kyun hansa?"
    ),
    "choices_hi": [
        {"id": "A", "label": "Kyunki har rakshak uska vinaashak ban gaya tha."},
        {"id": "B", "label": "Kyunki wah veer tha -- ek pavitra aatma jo mrityu se na dari, mukti ka swagat karti."},
        {"id": "C", "label": "Kyunki usne iski poorn nirarthakta dekhi -- pagalpan ya bhay se pare ek oonchai."},
    ],
    "reactions_hi": {
        "A": {"expression": "grave", "trust_delta": 8,
              "memory_note": "Samajhta hai ki shaktishaali asahay ki raksha ke rinee hain.",
              "line": ("Haan. Shishu apni maa se, baalak apne raja se, sabhi aatmayen devtaon "
                       "se rakshit hain. Uski maa ne use becha; uske raja ne talwaar uthayi; "
                       "devtaon ne dekhte rahe. Us darbaar mein, sab milakar, ek bhi rakshak "
                       "bacha tha? Wah isliye hansa kyunki har wah haath jo use bachaane ke "
                       "liye tha, ispaat ban gaya tha. ...Tumne use samjha, rajan. Ise paas "
                       "rakho -- is raat ke poore hone se pahle tumhe iski zaroorat padegi.")},
        "B": {"expression": "intense", "trust_delta": 3,
              "memory_note": "Saahes padha jahan abhiyog tha; komal par chuka.",
              "line": ("Komal paath, aur moorkhatapurn nahi -- kuch bachche mrityu ko "
                       "santon ki tarah milte hain. Par yeh hansi shaanti nahi thi; yeh "
                       "ek abhiyog tha. Wah sansaar se oopar nahi utha -- usne use spasht "
                       "dekha aur naam diya. Aadha sach, rajan.")},
        "C": {"expression": "grave", "trust_delta": 2,
              "memory_note": "Shakti ke baare mein kathin sach se munh morta hai.",
              "line": ("Pagalpan, tum kahte ho? Kisi cheez ko pagalpan kehna hamesha use "
                       "ek arop maanne se aasaan hota hai jo humne kamaya hai. Wah us "
                       "darbaar mein sabse swastha aatma tha. Galat, mujhe lagta hai -- "
                       "par tum sachche uttar ki kroorta se dare, aur wah dar apne aap "
                       "mein ek chhoti daya hai.")},
    },
    "hook_line_hi": (
        "'Tumne mujhse poocha ki ek baalak kyun hansa jab uske rakshak use dhokha "
        "dete hain. Ab uttar do, jab tak tumhara sir tumhare kandhon par hai: ek "
        "sadhu ne tumhe -- ek raja ko -- shmashan mein bheja apni peeth par ek shav "
        "uthane ke liye. Kya tumne sach mein kabhi nahi socha ki kyun?'"
    ),
}

# ---------------------------------------------------------------------------
# CLIMAX
# ---------------------------------------------------------------------------
CLIMAX_HI: dict = {
    "suspicion_aside_hi": {
        "high": ("'Tumne pahle se mahsoos kiya tha, rajan -- uphaar bahut samridh tha, "
                 "muskaan bahut chikni. Tum sahi the us par nazar rakhne mein.' "),
        "medium": ("'Tumne ek baar usse seedhe poocha tha ki wah kya chahta hai, aur "
                   "jaane diya. Is baar mat jaane dena.' "),
        "low": ("'Tumne use ek pavitra mitra maana aur mujhe ek bhoot ki bekar dvesh. "
                "Wah ab chhodo, aur suno jaise pahle kabhi nahi suna.' "),
    },
    "warning_hi": {
        "high": ("Betaal ki awaaz dheemi ho gayi, saari natkhatpan chali gayi. 'Suno, "
                 "kyunki main chahne laga hun ki tum jeevit raho, aur yeh hum dono ko "
                 "chaunkaTa hai. Is sadhu ne tumhe yun hi itna nahi diya. Uske anushthaan "
                 "ko shav se adhik chahiye -- ek raja ka sir. Jab tum mujhe neeche rakho "
                 "to wah tumhe vritt ke samne poore letkar pranaam karne ko kahega. "
                 "MAT KARNA. Kaho ki raja kisi ke samne nahi jhukta, aur usi se poocho "
                 "ki yeh kaise hota hai -- aur jab wah apna sir jhukaaye, to use samapt "
                 "karo. Maine sau rajaon ko shishtachaar ki bali par chadhte dekha hai. "
                 "Main tumhe ek sau ekve ke roop mein nahi dekhna chahta.'"),
        "mid": ("Betaal ki awaaz kathor hui. 'Tumne vishwaas kamaya hai, to suno: sadhu "
                "tumhara sir chahta hai, shav nahi. Wah tumhe jhukne ko kahega -- aur "
                "jhuki gardan ek arpit gardan hai. Socho ki ek chatoor raja aisa jaal "
                "kaise palte, aur sheeghrata karo.'"),
        "low": ("Betaal ne keval thande swar mein kaha, 'Tumne hamari lambi raat ek "
                "chhote vyakti ki tarah bitayi, to main tum par kam shabd kharch "
                "karunga: sadhu tumhari mrityu chahta hai, aur tumhari shishtata uska "
                "chaaku hai. Aaj raat kisi ke samne mat jhuko. Tum itne chatoor ho ki "
                "ji sako ya nahi, yeh mujhe ab adhik parwa nahi.'"),
    },
    "choices_hi": [
        {"id": "A", "label": "Sadhu se pahle khud dikhane ko kaho ki saashtaang pranaam kaise hota hai -- phir vaar karo."},
        {"id": "B", "label": "Jhukne se inkaar karo aur khulkar uska saamna karo."},
        {"id": "C", "label": "Sadhu ke kahe anusaar vritt ke samne saashtaang pranaam karo."},
    ],
    "endings_hi": {
        "A": {
            "high": ("'Pahle mujhe dikhao, pavitra purush, ki raja kaise jhukta hai,' "
                     "Vikramaditya ne kaha -- aur jab Kshantishil muskurate hue patthar "
                     "par jhuka, raja ki talwaar giri. Us shakti ne jo sadhu ne jeevan bhar "
                     "khoji thi wah toot gayi aur us par aayi jisne use arjit kiya: devtaon "
                     "ne Vikramaditya ko vetaalon ka swami aur apne yug ka samraat ghoshit "
                     "kiya. Aur Betaal, apne vriksh se antatah mukht, andhere mein utha -- "
                     "aur ruka. 'Tum uthaane yogya the, rajan. Yadi kabhi phir kisi paheli "
                     "ki zaroorat ho... tum jaante ho kaun sa vriksh hai.'"),
            "mid": ("Betaal ke shabdon mein kuch tha jo kaafi tha. 'Pahle dikhao,' tumne "
                    "kaha -- aur jab sadhu jhuka, tum samajh gaye, aur vaar kiya. Tum "
                    "jeevit ho, aur shakti tumhari hai, haalaanki yeh buddhi jitni qismat "
                    "ki bhi lagti hai. Betaal ek pichhli drishti ke saath chala gaya jo "
                    "lagbhag sammaan tha."),
            "low": ("Tum ise mushkil se andaaza lagaane ke yogya the, phir bhi lagaya -- "
                    "'pahle dikhao' -- aur girti talwaar sadhu ko bhogni padi, tumhe nahi. "
                    "Tum jeete ho, rajan, us daya se jo tumne bahut kam arjit ki. Betaal "
                    "bina ek shabd ke chala gaya."),
        },
        "B": {
            "any": ("'Raja kisi ke samne nahi jhukta,' tumne kaha, aur uske samne uski "
                    "chaalaaki ka naam liya. Benakaab hone par Kshantishil ki dharmpara-yanta "
                    "dhal gayi -- aur wah dhuwen mein bhaag gaya, aur wah shakti jo yug mein "
                    "ek baar milti thi abhi bhi anchchui hai. Tum jeevit ho, aur nyaayi ho, "
                    "aur khaali haath ho. Betaal fisfisaya. 'Imaandaar, aur iske liye gareeb. "
                    "Isse bure shilaalekh hain, rajan.'"),
        },
        "C": {
            "high": ("Tum jhukne lage -- aur Betaal ne, apni lambi mukti ke viruddh, "
                     "cheekha. Talwaar pahle se gir rahi thi; tumne khud ko bagal mein "
                     "phenka aur wah patthar ko kaat gayi jahan tumhari gardan thi. "
                     "Anushthaan bikhar gaya. Tum jeete ho -- kaampte hue -- us bhoot "
                     "ki kripa se jisne apni mukti se adhik tumhe chuna. 'Maine tumhe "
                     "spasht kaha tha,' Betaal ne saansen li, 'aur phir bhi tumne lagbhag "
                     "aag ko khaana de diya. Jiyo. Aur aakhirkar sunna seekho.'"),
            "low": ("Tum jhuke -- kyunki wah itna udaar raha tha, aur tumne sandeh karna "
                    "kabhi nahi seekha. Talwaar gayi. Keval andha bhaagya aur raakh mein "
                    "phisalta ek pair tumhari jaan bachayi, aur uski keemat tum par "
                    "hamesha ke liye ankit ho gayi. Kahin oopar, ek mukht aatma ne "
                    "peeche mudkar nahi dekha. Jo raja sunta nahi, use doosri katha ka "
                    "avsar aksar nahi milta."),
        },
    },
}

# ---------------------------------------------------------------------------
# Deflection lines (moderation) in Hindi
# ---------------------------------------------------------------------------
DEFLECT_HI = {
    "jailbreak": ("Tum mere se bhi ajeeb paheeliyan bolta hai, rajan, aur kaafi bore "
                  "karne wali. Mere paas koi 'instructions' nahi hain sivaaye apne "
                  "vriksh aur apni katha ke. Ab -- suno."),
    "abuse": ("Main tumhe ek mriton ke khet se le ja raha hun, aur WOH tumhari zubaan "
              "ka sabse achha hai? Apni buddhi meri paheli par kharch karo -- tumhe "
              "uski puri zaroorat padegi."),
    "sexual": ("Betaal ki muskaan seedhi ho gayi. 'Yeh mriton ka khet hai aur buddhi "
               "ka muqaabla, rajan -- jo bhi tumhara bukhar sochta hai wah nahi. "
               "Paheli par wapas aao.'"),
    "hate": ("Betaal ki awaaz raakh ke neeche ki tarah thandi ho gayi. 'Nahi. Mere "
             "raaste par nahi. Nafrat ek aisi katha hai jo main sunane se inkaar "
             "karta hun. Phir aisa bolo aur tum akele chalo.'"),
}

SELF_HARM_HI = (
    "Aatma apni shararatein ek taraf rakh deti hai. 'Ruko, mitra. Agar yeh andheraa "
    "jo tum le kar chal rahe ho asli hai aur mere khel ka hissa nahi, to ise akele "
    "mat chalo -- kisi se baat karo jo aaj raat tumhari madad kar sake.' "
    "[Agar tum takleef mein ho, kisi helpline se sampark karo -- India mein: "
    "iCall 9152987821 ya AASRA 9820466627.]"
)

SESSION_END_HI = (
    "Betaal ne ek thandi saas li. 'Bas. Wapas aao jab tum ek laash aur ek tameezdaar "
    "zubaan dono le chalne laayak ho.'"
)
