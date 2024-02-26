import json
import os
from collections import defaultdict
from pprint import pprint
    # except Exception as e:
    #     print(e)
    #     print(file)
count = defaultdict(int)
files = []
with open('kaggle_data/arxiv-metadata-oai-snapshot.json', encoding='latin-1') as f:
    for line in f:
        doc = json.loads(line)
        for ele in ['cs.LG', 'cs.AI', 'cs.CL', 'cs.CV', 'cs.IR', 'cs.IT', 'cs.MA', 'cs.RO', 'stat.ML']:
            if ele in doc['categories']:
                files.append(doc)
                count['20' + doc['id'][:2]] += 1

            #     pprint(doc)
            
            # break
        # lst = [doc['id'], doc['title'], doc['abstract'], doc['categories']]
        # data.append(lst)
    
with open(f"kaggle_data/data_subset.json", "w") as outfile:
    json.dump(files, outfile)

pprint(count)
# print(sum(count.values()))