import os, time, utils

def single_term_query(query: str, scoreType: str, inverted_index: dict, URLs: dict):
    '''
    The following function inputs a query term, score type, the inverted index and the
    list of dictionaries of tf per document. We compute the score for
    the query in each document it occurs in & display the output.
    '''
    queryFound = True
    if query in inverted_index:
        postings_list = inverted_index[query]
        utils.single_query_compute(scoreType, postings_list, URLs)
    else:
        queryFound = False

    return queryFound

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
        found = single_term_query(query, scoreType, inverted_index, URLs)
    # elif queryType == "2":
    #     assert len(query.split(" ")) > 1, "You have demanded an AND query but you have only entered one term."
    #     and_term_query(query, inverted_index, tf_dict_list)
    # elif queryType == "3":
    #     assert len(query.split(" ")) > 1, "You have demanded an AND query but you have only entered one term."
    #     or_term_query(query, inverted_index, tf_dict_list)
    # elif queryType == "4":
    #     ranked_term_query(query, inverted_index, tf_dict_list)
    end = time.time()
    if found:
        print(f'\nDone! Your query was found in {"{:.3f}".format(end-start)} seconds')
    else:
        print("Query not found!")

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