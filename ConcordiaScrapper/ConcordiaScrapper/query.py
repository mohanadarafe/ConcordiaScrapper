import os, time, utils

def single_term_query(query: str, scoreType: str, inverted_index: dict, URLs: dict):
    '''
    The following function inputs a query term, score type, the inverted index and the
    URLs per document. We compute the score for the query in each document it occurs 
    in & display the output.
    '''
    if query in inverted_index:
        postings_list = inverted_index[query]
        utils.single_query_compute(scoreType, postings_list, URLs)
    else:
        print(f"The query term \"{query}\" was not found!")

def and_term_query(query_terms: str, scoreType: str, inverted_index: dict, URLs: dict):
    '''
    The following function inputs a query term, score type, the inverted index and the
    URLs per document. We compute the intersection of each term in the query & sum the 
    score values of the terms in each document.
    '''
    postings_of_query_terms = []
    terms = [query.lower() for query in query_terms.split()]
    queries = []

    for query in terms:
        if query in inverted_index:
            queries.append(query)
            postings_of_query_terms.append(list(inverted_index[query][1]))
        else:
            print(f"The query term \"{query}\" was not found!")

    if len(queries) == 1:
        single_term_query(queries[0], scoreType, inverted_index, URLs)
    else:
        docs_dictionary = dict()
        and_postings = dict()

        for postings in postings_of_query_terms:
            for docID, tf in postings:
                if docID not in docs_dictionary:
                    docs_dictionary[docID] = tf
                else:
                    and_postings[docID] = tf

        utils.and_query_compute(queries, scoreType, and_postings, inverted_index, URLs)

def parse_query(query: str, queryType: str, scoreType: str):
    '''
    The following function decides which type of query algorithm we should run based on the user input.
    1 - SINGLE
    2 - AND
    3 - OR
    4 - RANKED
    '''
    assert os.path.isfile("visited_urls.json"), "Make sure you run the crawler first! Check README for instructions."
    assert os.path.isfile("result.json"), "Make sure you run the crawler first! Check README for instructions."
    inverted_index = utils.open_dictionary_file("result.json")
    URLs = utils.open_dictionary_file("visited_urls.json")

    start = time.time()
    if queryType == "1":
        assert len(query.split(" ")) == 1, "You have demanded a SINGLE query but you have more than one term."
        single_term_query(query.lower(), scoreType, inverted_index, URLs)
    elif queryType == "2":
        assert len(query.split(" ")) > 1, "You have demanded an AND query but you have only entered one term."
        and_term_query(query, scoreType, inverted_index, URLs)
    # elif queryType == "3":
    #     assert len(query.split(" ")) > 1, "You have demanded an AND query but you have only entered one term."
    #     or_term_query(query, inverted_index, tf_dict_list)
    # elif queryType == "4":
    #     ranked_term_query(query, inverted_index, tf_dict_list)
    end = time.time()
    print(f'\nDone! Your query was found in {"{:.3f}".format(end-start)} seconds')

def _prompt_user():
    '''
    The following function prompts the user to enter query inputs. 
    '''
    keepGoing = True
    while (keepGoing):

        scoreType = input("\nPlease enter a score type: [1] BM25 [2] tf.idf: ")
        while(scoreType not in ["1", "2"]):
            print("Please enter a valid score type")
            scoreType = input("\nPlease enter a score type: [1] BM25 [2] tf.idf: ")

        queryType = input("Please enter a query type: [1] SINGLE [2] AND [3] OR [4] RANKED: ")
        while(queryType not in ["1", "2", "3", "4"]): 
            print("Please enter a valid query type")
            queryType = input("Please enter a query type: [1] SINGLE [2] AND [3] OR [4] RANKED: ")

        query = input("Please enter a query: ")
        while(not query): 
            print("Please enter a valid query type")
            queryType = input("Please enter a query type: ")

        parse_query(query, queryType, scoreType)

        inp = input("Would you like to submit another query? [y/n] ")
        while(inp not in ["y", "n"]):
            print("Please enter a valid response")
            inp = input("Would you like to submit another query? [y/n] ")

        keepGoing = True if inp == "y" else False

if __name__ == "__main__":
    _prompt_user()