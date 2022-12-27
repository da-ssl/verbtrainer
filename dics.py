personDict = {
    "it": {0: "1. Person Singular",
        1: "2. Person Singular",
        2: "3. Person Singular",
        3: "1. Person Plural",
        4: "2. Person Plural",
        5: "3. Person Plural"},
    "fr": {0: "1. Person Singular",
        1: "2. Person Singular",
        2: "3. Person Singular, maskulin",
        3: "3. Person Singular, feminin",
        4: "1. Person Plural",
        5: "2. Person Plural",
        6: "3. Person Plural, maskulin",
        7: "3. Person Plural, feminin"
        }
}

personenDictDB = {
    "it": {0: "s1",
        1: "s2",
        2: "s3",
        3: "p1",
        4: "p2",
        5: "p3"},
    "fr": {0: "s1",
        1: "s2",
        2: "s31",
        3: "s32",
        4: "p1",
        5: "p2",
        6: "p31",
        7: "p32"}
}

personcount = {
    "it": 6,
    "fr": 8
}

pronomenDic = {
    "it": {
        0: "io",
        1: "tu",
        2: "lei/lui",
        3: "noi",
        4: "voi",
        5: "loro"},
    "fr": {
        0: "je/j'",
        1: "tu",
        2: "il",
        3: "elle",
        4: "nous",
        5: "vous",
        6: "ils",
        7: "elles",
    }
}

tenses = {
    "fr": [
        "present", 
        "imparfait", 
        "futur",
        "passesimple",
        "passecompose",
        "plusqueparfait",
        "passeanterieur",
        "futuranterieur",
        "subpresent",
        "subimparfait",
        "subplusqueparfait",
        "subpasse",
        "condpresent",
        "condpasse1",
        "condpasse2"
    ],
    "it": [
        "presente", 
        "futuro", 
        "passato prossimo",
        "imperfetto",
        "congiuntivo"
]}

tensesDB = {
"it": {
    "passato prossimo": "passatoprossimo",
}}

tensenames = {
    "fr": {
        "present": "Présent", 
        "imparfait": "Imparfait", 
        "futur": "Futur",
        "passesimple": "Passé simple",
        "passecompose": "Passé composé",
        "plusqueparfait": "Plus-que-parfait",
        "passeanterieur": "Passé antérieur",
        "futuranterieur": "Futur antérieur",
        "subpresent": "Subjonctif Présent",
        "subimparfait": "Subjonctif Imparfait",
        "subplusqueparfait": "Subjonctif Plus-que-parfait",
        "subpasse": "Subjonctif Passé",
        "condpresent": "Conditionnel Présent",
        "condpasse1": "Conditionnel Passé première forme",
        "condpasse2": "Conditionnel Passé deuxième forme"},
    "it": {
        "presente": "presente", 
        "futuro": "futuro", 
        "passato prossimo": "passato prossimo",
        "imperfetto": "imperfetto",
        "congiuntivo": "congiuntivo"
        }
}

most_important_verbs = {
    "fr": [
        "être",
        "faire",
        "avoir",
        "voir",
        "dire",
        "prendre",
        "assurer",
        "obtenir",
        "pouvoir",
        "utiliser"
    ],
    "it":[
        "essere",
        "vedere",
        "avere",
        "dire",
        "fare",
        "trovare",
        "sapere",
        "prendere",
        "parlare"
    ]
}

supported_languages = {
    "Italienisch": "it",
    "Französisch": "fr"
}

supported_languages_2 = {
    "it": "Italienisch",
    "fr":"Französisch"
}