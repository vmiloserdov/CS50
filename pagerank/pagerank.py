import os
import random
import re
import sys

from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    dicti = dict()
    links = corpus[page]

    num_pages = len(corpus)
    num_links = len(links)

    for link in links:
        dicti[link] = damping_factor / num_links

    for key, _ in corpus.items():
        dicti[key] = dicti.get(key, 0) + ((1 - damping_factor) / num_pages)

    return dicti



    
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Generate the first sample
    page_names = list(corpus.keys())
    first_page = random.choice(page_names)
    samples = [first_page]

    for _ in range(n-1):
        model = transition_model(corpus, samples[-1], damping_factor)
        formatted = [(key, value) for key, value in model.items()]

        names = [item[0] for item in formatted]
        probs = [item[1] for item in formatted]

        selected = random.choices(names, weights=probs, k=1)[0]
        samples.append(selected)

    counts = Counter(samples)
    res_dict = dict()

    for page, count in counts.items():
        res_dict[page] = count / n


    return res_dict






def assign_init(corpus, N):
    dicti = dict()

    for key in corpus:
        dicti[key] = 1/N

    return dicti


def sigma(corpus, probs, curr_page):
    leading_pages = [page for page, links in corpus.items() if curr_page in links]
    summy = 0

    for page in leading_pages:
        summy += probs[page] / len(corpus[page])

    return summy

def clean_corpus(corpus):
    all_pages = {page for page in corpus}
    for page in all_pages:
        if not corpus[page]:
            corpus[page] = all_pages

    return corpus

    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    corpus = clean_corpus(corpus)
    probs = assign_init(corpus, N)
    keep_going = True

    while (keep_going):
        diffs = []

        # Calculate all the new ranks
        for page in corpus:
            new_rank = (1-damping_factor) / N + damping_factor * sigma(corpus, probs, page)

            diff = abs(probs[page] - new_rank)
            diffs.append(diff)

            probs[page] = new_rank
            
        keep_going = not all(dif <= 0.001 for dif in diffs)

    return probs
            

if __name__ == "__main__":
    main()
