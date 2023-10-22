import re
import qq_parser as qq

s = "John's mom went there, but he wasn't c++, c#, .net, Q&A/Q-A, #nope i_t IT at-all'. So' she said: 'Where are& viix.co. !!' 'A a'"


def translate(txt: str):
    translation = {
        0xfffd: 0x0020, 0x00b7: 0x0020, 0xfeff: 0x0020, 0x2026: 0x0020, 0x2713: 0x0020, 0x205F: 0x0020, 0x202c: 0x0020, 
        0x202a: 0x0020, 0x200e: 0x0020, 0x200d: 0x0020, 0x200c: 0x0020, 0x200b: 0x0020, 0x2002: 0x0020, 0x2003: 0x0020, 
        0x2009: 0x0020, 0x2011: 0x002d, 0x2015: 0x002d, 0x201e: 0x0020, 0x2028: 0x0020, 0x2032: 0x0027, 0x2012: 0x002d, 
        0x0080: 0x0020, 0x0094: 0x0020, 0x009c: 0x0020, 0xFE0F: 0x0020, 0x200a: 0x0020, 0x202f: 0x0020, 0x2033: 0x0020, 
        0x2013: 0x0020, 0x00a0: 0x0020, 0x2705: 0x0020, 0x2714: 0x0020, # 0x2013: 0x002d
        0x201c: 0x0020, 0x201d: 0x0020, 0x021f: 0x0020, 0x0022: 0x0020, 0x2019: 0x0027, 0x2018: 0x0027, 0x201b: 0x0027, 
        0x0060: 0x0027, 0x00ab: 0x0020, 0x00bb: 0x0020, 0x2026: 0x002e, 0x2014: 0x0020 } # 0x2014: 0x002d

    txt = txt.translate(translation)
    return txt.strip()


def str_to_ngrams(str_line: str, stopwords: set()):
   
    line1 = str_line.replace(". ", "! ")
    line1 = re.sub('[!?;,:\[\]\(\)]', "!", line1)
    strips = [x.strip() for x in line1.split("!") if x !='']

    punctuation = " ©®-%$!?:,;\'\" @~&()=*_<=>{|}[/]^\\"
    result = []
    exclude = { "2d", "3d", "3g", "4g", "5g", "6g" }

    for item in strips:

        #words_list = [x.strip(" ") for x in item.split(" ") if (x != '')]
        #words_list = [x.strip(punctuation) if x not in self.dictionary else x for x in item.split(" ") if (x != '')]

        word_list = [x.strip(punctuation) for x in item.split(" ") if (x.strip(punctuation) != '')]
        tokens = []
        for w in word_list:
            wlow = w.lower()
            if (w == "IT") or (wlow == "c#") or (wlow in exclude):
                tokens.append(wlow)
            else:
                wlow = wlow.strip("#")
                if qq.is_word(wlow, stopwords):
                    tokens.append(wlow)

        if tokens: result.append(tokens)
    return result
