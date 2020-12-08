import os, json, math

def open_dictionary_file(file: str) -> dict:
    '''
    The following function inputs a file name & loads it into a dictionary
    that is returned.
    '''
    assert os.path.isfile(file), "The file does not exist!"
    dictionary = dict()
    with open(file, 'r') as json_file: 
        dictionary = json.load(json_file)

    if 'result' in file:
        assert len(dictionary) == 1, "The results rendered too many times."
        assert type(dictionary[0]) == dict, "The results did not run correctly."
        return dictionary[0]

    return dictionary

def get_avg_doc_length():
    '''
    Gets the average length per document.
    '''
    urls = open_dictionary_file("visited_urls.json")
    totalDocLength = 0
    for url, docLength in urls.values():
        totalDocLength += docLength
    return totalDocLength / len(urls)

def idf(N: int, df: int) -> float:
    ''' 
    The following function computes the inverse document frequency
    '''
    value = 0
    try:
        value = math.log10(N/df)
    except ZeroDivisionError:
        value = 0
    return value

def _numerator(k: float, tf: float) -> float:
    '''
    The following function computes the numerator of the BM25 formula.
    (k + 1) * tf
    '''
    return tf * (1+k)

def _denominator(k: float, b: float, L_d: float, L_ave: float, tf: float):
    '''
    The following function computes the denominator of the BM25 formula.
    k * ((1-b) + b * (L_d / L_ave)) + tf
    '''
    product1_1 = 1-b
    product1_2 = b * (L_d / L_ave)
    product = k * (product1_1 + product1_2)
    return product + tf

def BM25(df, tf, Ld, Lave, N, b=0.5, k=10) -> float:
    '''
    The following function computes the BM25 formula.
    '''
    try: 
        product1 = idf(N, df)
        product2 = _numerator(k, tf) / _denominator(k, b, Ld, Lave, tf)
    except ZeroDivisionError:
        return 0

    return product1 * product2

def tf_idf(tf, df, N):
    urls = open_dictionary_file("visited_urls.json")
    idf_score = idf(N, idf)

def single_query_compute(scoreType: str, postings_list: list, URLs: dict):
    scores = []

    if scoreType == "1":
        for docID, tf in postings_list[1]:
            df = postings_list[0]
            L_d = URLs[str(docID)][1]
            rsv_score = BM25(df, tf, L_d, get_avg_doc_length(), len(URLs))
            scores.append((docID , rsv_score))

    scores = sorted(scores, reverse=True, key = lambda x: x[1]) 
    top = 15 if (len(scores) > 15) else len(scores)
    print(f'The top {top} documents are:')
    for i in range(top):
        print(f'{i+1}. Document {scores[i][0]} with a score of {round(scores[i][1], 3)}\t- {URLs[str(scores[i][0])][0]}')