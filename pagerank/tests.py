from pagerank import sample_pagerank, iterate_pagerank


def test_sample():
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    df = 0.85
    n = 100000

    print(sample_pagerank(corpus, df, n))



def test_iterate():
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    df = 0.85

    print(iterate_pagerank(corpus, df))




#test_sample()
test_iterate()