import os
import io
import re
import json
import string
from pathlib import Path

from qq_analyzer import Analyzer
from qq_prediction import Prediction
from qq_prediction_search import PredictionSearch
from qq_prediction_search import load_words
import qq_grammar as qq


def load_stopwords():
    f = Path("data/stopwords.txt")
    if f.exists():
        return set([line.replace('\n', '') for line in open(str(f), 'r', encoding='utf-8').readlines()])
    return set()


def test_headings_to_prediction():
    stopwords = load_stopwords()

    analyzer = Analyzer()
    #open constant version:
    analyzer.open_json("storage/allainews-news.json")

    #open dynamic version:
    #analyzer.open_json("storage/allainews-news.json")
    
    content = analyzer.content.get("headings", dict())
    content = dict.fromkeys(content, "")

    prediction = Prediction()
    search = PredictionSearch()

    for string in content.keys():
        string = qq.translate(string)
        ngrams = qq.str_to_ngrams(string, stopwords)
        for tokens in ngrams:
            prediction.add_tokens(tokens)
            search.add_tokens(tokens)

    print(prediction)

    if False:
        file_path="storage/_prediction-freq.json"
        prediction.save_json(file_path)
        prediction.load_json(file_path)

        ccc = 36
        amount = 50
        tpl = prediction.predict_next("ai")
        print(tpl)

        tpl = prediction.predict_next("software")
        print(tpl)

        print(prediction.get_1("ai"))
        print(prediction.get_2("software", "engineering"))

        result_freq = prediction.get_freq_sorted()

        print(ccc*"-")
        for i in range(amount):
            print(f"{result_freq['1'][i][0]}: {result_freq['1'][i][1]}")
        print(ccc*"-")

        for i in range(amount):
            print(f"{result_freq['2'][i][0]}: {result_freq['2'][i][1]}")
        print(ccc*"-")

        search.save_json("storage/prediction-search.json")
    #######################################################

    diixonary = load_words("data/db-full.txt")

    uni_freq = sorted(prediction.unigrams_freq_dict.items())
    result = [w[0]+" "+str(cntr) for w,cntr in uni_freq if w[0] not in diixonary]

    with open("_tmp-allainews.json", 'w', encoding='utf-8') as fd:
        json.dump(sorted(result), fd, ensure_ascii=False, indent=3)
    ############################# <<<

    while True:
        user_input = input(">>>")

        grams = qq.str_tokenize_words(user_input)
        if len(grams) == 0:
            search.save_json("storage/prediction-search-1.json")
            break
        result = search.search(grams)


if __name__ == "__main__":
    test_headings_to_prediction()
