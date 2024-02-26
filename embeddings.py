from collections import defaultdict
from sentence_transformers import SentenceTransformer
import json
from dataclasses import dataclass
import torch
import pickle
import os
import logging
import time

logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
logger = logging.getLogger(__name__)


device = torch.device('mps')
model = SentenceTransformer('BAAI/bge-large-en-v1.5', device=device)

@dataclass
class Paper:
    id: str
    title: str
    authors: str
    categories: str
    abstract: str
    update_date: str
    
    def __post_init__(self):
        if "/" in self.id:
            year_postfix = self.id.split('/')[1][:2]
        else:
            year_postfix = self.id[:2]

        self.year = '19' + year_postfix if year_postfix <= '99' and year_postfix >= '30' else '20' + year_postfix

    def __repr__(self):
        return f"Title: {self.title}\nAuthors: {self.authors}\nAbstract: {self.abstract}\nLatest Update Date: {self.update_date}"


with open('kaggle_data/data_subset.json', encoding='latin-1') as f:
    papers = json.load(f)

years_to_paper = defaultdict(list)
for paper in papers:
    curr_paper = Paper(id=paper['id'], title=paper['title'], abstract=paper['abstract'],
                              authors=paper['authors'], update_date=paper['update_date'], categories=paper['categories'])
    years_to_paper[curr_paper.year].append(curr_paper)


curr_time = time.time()
for year in years_to_paper.keys():
    logger.info(f"Processing year {year}")
    papers_per_year = years_to_paper[year]

    per_year_embeddings = {}

    embeddings = model.encode(sentences=[str(val) for val in papers_per_year], batch_size=64, show_progress_bar=True, convert_to_numpy=True, device=device)
    res = {papers[i]['id']: embeddings[i] for i in range(len(embeddings))}

    base_dir = f"embeddings/{year}"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    logger.info(f"Saving embeddings {year} in {base_dir}/data.pkl")
    with open(base_dir + "/data.pkl", "wb") as f:
        pickle.dump(res, f)

logger.info(f"Total time to process: {time.time() - curr_time}")
