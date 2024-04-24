import time
import json
from pathlib import Path
import qq_parser as qq_parser
from qq_crawler2 import Crawler2
import qq_grammar as qq
from qq_prediction import Prediction


def load_stopwords():
    f = Path("data/stopwords.txt")
    if f.exists():
        return set([line.replace('\n', '') for line in open(str(f), 'r', encoding='utf-8').readlines()])
    return set()

class Analyzer:

   def __init__(self):

      self.content = dict()
      self.content["urls"] = dict()
      self.urls = self.content["urls"]
      self.filepath = ""

   def open_json(self, filepath: str):
      path = Path(filepath)
      if path.exists():
         fd = open(filepath, 'r', encoding='utf-8')
         self.content = json.load(fd)
      self.filepath = filepath

      if not self.content.get("urls"):
         self.content["urls"] = dict()
      self.urls = self.content["urls"]


   def save_json(self, filepath = None):
      if filepath != None:
         self.filepath = filepath
      with open(self.filepath, 'w', encoding='utf-8') as fd:
         json.dump(self.content, fd, ensure_ascii=False, indent=3)


   def learn_url(self, url: str, hhh_mask = None):
      url = url.lower().strip('/')
      if url in self.urls:
         return False
      else:
         qq_parser.parse_url(url, self.content, hhh_mask=hhh_mask)
         self.urls[url] = ""
         return True

   def learn_file(self, filepath: str):
      path = Path(filepath)
      if path.name in self.urls:
         print(f"[Analyzer] file={path.name} done already")
      else:
         if path.exists():
            qq_parser.parse_file(filepath, self.content)
            self.urls[path.name] = ""

   def import_json(self, filepath: str):
      if not self.content.get("urls"):
         self.content["urls"] = dict()
      self.urls = self.content["urls"]

      hhh = self.content.get("headings", dict())
      self.content["headings"] = dict.fromkeys(hhh, "")

      path = Path(filepath)
      if path.exists():
         fd = open(filepath, 'r', encoding='utf-8')
         self.content = json.load(fd)
      self.filepath = filepath


def test_url_to_dataset():
   url = "https://allainews.com/news"

   crawler = Crawler2()
   crawler.enqueue_url(url)
   crawler.set_filter(url, [
      "/terms/", 
      "/privacy/", 
      "/accounts/", 
      "/filtered/", 
      "/videos/", 
      "/feed/", 
      "/topic/",
      "/source/",
      "/news/feed",
      "/term",
      "/about",
      "/podcasts",
      "/sources.md"
      ])
   crawler.run()

   ###########################
   urls = crawler.get_urls(url)

   analyzer = Analyzer()
   analyzer.open_json("storage/allainews-news.json")

   #analyzer.learn_file("template/keywords.html")

   print(f">> [Analyzer] :{len(analyzer.content.get('headings', dict()))}")
   for u in urls:
      if analyzer.learn_url(u, hhh_mask=["h1", "H1"]):
         print(f"[Analyzer] ...on [{len(urls)}]: {u}")
         time.sleep(2.0)
   analyzer.save_json()
   print(f"<< [Analyzer] :{len(analyzer.content.get('headings', dict()))}")

   exit(0)
   ####################### analyze keywords #######################
   stopwords = load_stopwords()

   prediction = Prediction()
   keywords = analyzer.content.get("keywords", list())
   content = analyzer.content.get("headings", dict())

   for string in content.keys():
      string = qq.translate(string)
      ngrams = qq.str_to_ngrams(string, stopwords)
      for tokens in ngrams:
         prediction.add_tokens(tokens)


   result = dict()
   for sentence in keywords:
      tokens = qq.str_tokenize_words(sentence)
      sz = len(tokens)
      grams = tuple(tokens[0:sz])

      count = 0
      if sz == 1:
         count = prediction.unigrams_freq_dict.get(grams, count)
      if sz == 2:
         count = prediction.bigrams_freq_dict.get(grams, count)
      if sz == 3:
         count = prediction.trigrams_freq_dict.get(grams, count) 

      if count > 0: result[sentence] = count

   print(f"keywords.sz={len(keywords)}, result.sz={len(result)}")


def test_with_ssl():
   analyzer = Analyzer()
   analyzer.open_json("storage/ssl-content.json")
   analyzer.learn_url("https://www.linkedin.com/pulse/exploring-linear-regression-gradient-descent-mean-squared-ravi-singh", ["h1"])
   #analyzer.learn_url("https://www.marktechpost.com/2023/10/22/google-ai-presents-pali-3-a-smaller-faster-and-stronger-vision-language-model-vlm-that-compares-favorably-to-similar-models-that-are-10x-larger")
   analyzer.save_json()


def test_dataset():
   u1 = "https://pythonexamples.org/"
   u2 = "https://kotlinandroid.org/"
   u3 = "https://www.javatpoint.com/"
   u4 = "http://neevo.net/"
   #u5 = "https://www.geeksforgeeks.org/generative-adversarial-network-gan/"
   #u5 = "https://javascriptcode.org/"
   #u5 = "https://www.javatpoint.com/python-variables"
   #u5 = "https://www.programiz.com/r"
   
   analyzer = Analyzer()
   #analyzer.learn_file('process/techopedia-train-db-v5.data')
   analyzer.open_json("./storage/_data.json")
   analyzer.learn_file('template/template.html')
   analyzer.learn_url(u1)
   analyzer.learn_url(u2)
   analyzer.learn_url(u3)
   analyzer.learn_url(u4)
   analyzer.save_json()


def test_aixploria():
   crawler = Crawler2(delay=3, recursive=True)
   crawler.enqueue_url("https://www.aixploria.com/en")
   crawler.run()

if __name__ == "__main__":
   test_url_to_dataset()
   #test_with_ssl()
   #test_dataset()

   #test_aixploria()
