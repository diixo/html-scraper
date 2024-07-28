
from qq_crawler2 import Crawler2


def test_futuretools():
    crawler = Crawler2()
    crawler.extract_from_file("./test/futuretools.html", "https://www.futuretools.io/", 
        ["/submit-a-tool", "/?d", "/faq", "/learn", "/?tags="])
    crawler.save_json()


def test_unite_ai():
    crawler = Crawler2(recursive=True)
    crawler.enqueue_url("https://www.unite.ai/")
    crawler.open_json("test/www.unite.ai.json")

    crawler.set_filter("https://www.unite.ai/", 
    [
        "mailto:",
        "javascript:",
        "/author",
        "/blogger",
        "/user/login",
        "/privacy-policy",
        "/terms-and-conditions",
        "/contact-us",
        "/meet-the-team",
        "/press-tools",
        "/imagesai",
        "/our-cherter",
        "/cdn-cgi",
        "/?", "=%", "/%", 
        "/de/", "/es/", "/fr/", "/id/", "/it/", "/ja/", "/ko/", "/nl/", "/no/", "/pl/", "/pt/", "/ru/", "/tr/", "/vi/",
        "/about",
        "/affiliate-terms",
        "/agencies",
        "/careers",
        "/compatibilities",
        "/contact",
        "/contactus",
        "/features",
        "/integrations",
        "/partner",
        "/partner-apply",
        "/pricing",
        "/privacy",
        "/refunds",
        "/terms",
        "/enterprise",
        "/faq",
        "/how-does-it-work",
        "/privacy",
        "/terms",
        "/partner",
        "/price",
        "/support"
    ])
    crawler.run()
    crawler.save_json("test/www.unite.ai.json")


def main():
    test_unite_ai()
    return

    crawler = Crawler2(recursive=False)
    crawler.open_json("test/crawler-2.json")

    crawler.enqueue_url("https://www.pythontutorial.net/python-concurrency/")
    crawler.set_filter("https://www.pythontutorial.net", ["/privacy-policy", "/contact", "/donation"])

    crawler.enqueue_url("https://kotlinandroid.org/kotlin/kotlin-hello-world/")
    crawler.set_filter("https://kotlinandroid.org", ["/privacy-policy", "/contact-us", "/terms-of-use"])

    crawler.run()
    crawler.save_json()

###############################################################################################

if __name__ == "__main__":
    main()
