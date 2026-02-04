import json
from rag.retrieval import retrieval_chromadb
from typing import List
import re

# removes punctuation and lowercase
def normalize(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()

with open('eval/gold_set.json') as f:
    dataset: List= json.load(f)

    len_data = len(dataset)

    rank = [] # for MRR
    rr = 0

    source_counter = 0
    keywords_counter = 0

    joint_counter = 0

    for i, data in enumerate(dataset):
        
        source = False
        keywords = False

        response = retrieval_chromadb(data['question'], n_results = 5)

        # print(type(data['relevant_sources']))
        # print(type(response['metadatas'][0][0]['source']))

        # print(type(response['metadatas'][0][0]))
        # print(response['metadatas'][0][0])

        # checking source and r is for the rank of the documents retrieved
        for r in range(len(response['metadatas'][0])):
            
            # relevant_source is a string
            if data['relevant_sources'] in response['metadatas'][0][r]['source']:
                source = True
                rr = (1 / (r + 1))
                break
        
        rank.append(rr)
    
        # checking keywords
        for j in range(len(response['documents'][0])):

            # normailizing for each word in reponse.split()
            content = [normalize(w) for w in response['documents'][0][j].split()]

            for word in data['expected_keywords']:
                if normalize(word) in content:
                    keywords = True

        if source:
            source_counter += 1
        else:
            print(f"Data {i+1}, Source not hit: {data['relevant_sources']}. Source from document retrieved: {[m['source'] for m in response['metadatas'][0]]}")
        
        if keywords:
            keywords_counter += 1
        else:
            print(f"Keywords not hit: {data['expected_keywords']}")

        
        if source and keywords:
            joint_counter += 1
    
    # MRR
    num_of_queries = len(dataset) # one data has one queries

    mean_reciprocal_rank = (1/num_of_queries) * sum(rank)

    source_recall_at_5 = source_counter / len_data
    keyword_hit_rate = keywords_counter / len_data
    joint_success_rate = joint_counter / len_data

    print(f"Source Recall@5 (Hit@5): {source_recall_at_5:.3f}")
    print(f"Keyword Hit Rate@5:      {keyword_hit_rate:.3f}")
    print(f"Joint Success Rate:      {joint_success_rate:.3f}")
    print(f"Mean Reciprocal Rank:    {mean_reciprocal_rank:.3f}")
   