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

    source_counter = 0
    keywords_counter = 0

    joint_counter = 0

    for data in dataset:
        
        source = False
        keywords = False

        response = retrieval_chromadb(data['question'], n_results = 5)

        # print(type(data['relevant_sources']))
        # print(type(response['metadatas'][0][0]['source']))

        # checking source
        for source_metadata in response['metadatas'][0]:
            
            # relevant_source is a string
            if data['relevant_sources'] in source_metadata['source']:
                source = True

            if source:
                break

        # checking keywords
        for i in range(len(response['documents'][0])):

            # normailizing for each word in reponse.split()
            content = [normalize(w) for w in response['documents'][0][i].split()]

            for word in data['expected_keywords']:
                if word.lower() in content:
                    keywords = True

        if source:
            source_counter += 1
        
        if keywords:
            keywords_counter += 1
        
        if source and keywords:
            joint_counter += 1
    
    # ---------- Metrics ----------
    source_recall_at_5 = source_counter / len_data
    keyword_hit_rate = keywords_counter / len_data
    joint_success_rate = joint_counter / len_data

    print(f"Source Recall@5 (Hit@5): {source_recall_at_5:.3f}")
    print(f"Keyword Hit Rate@5:      {keyword_hit_rate:.3f}")
    print(f"Joint Success Rate:      {joint_success_rate:.3f}")
   