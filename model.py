import chromadb
import cohere
import os
import re
import subprocess
from model_utils import mo_utils
import threading
import time

class Model():
    def __init__(self):
        chroma_client = chromadb.Client()
        self.collection = chroma_client.create_collection(name="main")
        self.co = cohere.Client(os.environ["COHERE_API_KEY"])

        with open("prompts/generate.txt", 'r') as f:
            self.generate_prompt = f.read()

        documents = []
        filenames = []

        dataset = "dataset/curated"

        for filename in os.listdir(dataset):
            with open(os.path.join(dataset, filename), 'r') as f:
                documents.append(f.read())
                filenames.append(filename)

        self._add_documents(documents, filenames)

    def run_retrieval(self, query):
        result = self.collection.query(
            query_texts=[query],
            n_results=1
        )
        vector_choice = result["documents"][0][0]

        pattern = r'```(.*?)```'
        extracted = re.findall(pattern, vector_choice, re.DOTALL)

        name = re.search(r'"(.*?)"', vector_choice).group(1)

        gene = {
            "seq": extracted[0][1:-2],
            "name": name
        }

        return gene, None

    def run_scratch(self, query):
        prompt = self.generate_prompt + "\n" + query

        print('starting gen')
        # using ft-ed model
        response = self.co_chat_with_timeout(prompt)
        print("done gen")

        dna = response.text
        print(dna)

        z_score = self.verify_structure(dna)

        gene = {
            "seq": dna,
            "name": "Gen"
        }

        return gene, z_score

    def verify_structure(self, dna):
        # given generated string, use alphafold to asses biological viability
        # colabfold_batch input outputdir/
        # need to build file

        mo_utils.clean_folder()
        mo_utils.generate_fasta(dna)
        
        command = ["colabfold_batch", "input/structure", "output/verify/"]
        command = 'source "/home/nomitchell/anaconda3/etc/profile.d/conda.sh" && conda activate base && colabfold_batch input/structure/temp.fasta output/verify'

        try:
            result = subprocess.run(['bash', '-c', command], check=True, text=True)
            print("LCF executed succesfully")
        except subprocess.CalledProcessError as e:
            print("Couldn't execute subprocess command.")

        # for some reason prosa wasn't working when file had a header
        folder_path = 'output/verify'
        fname = mo_utils.get_rank_1_path(folder_path)

        with open(fname, 'r') as file:
            lines = file.readlines()
            lines = lines[1:]

        with open(fname, 'w') as file:
            file.writelines(lines)

        # access prosa site, make post, scrape results

        z_score = mo_utils.get_z_score(fname)

        print("Z score", z_score)

        return z_score

    def co_chat_with_timeout(self, prompt):
        # sorry cohere, your api kept timing out so I had to set a time limit and retry
        def target():
            nonlocal result
            try:
                result = self.co.chat(message=prompt, model='c4e6f320-6a12-4385-ba5d-d39bc8935c0b-ft')
            except Exception as e:
                result = str(e)

        result = None

        thread = threading.Thread(target=target)
        thread.start()
        
        thread.join(5)

        if thread.is_alive():
            print("Operation timed out. Retrying...")
            thread.join()
            return self.co_chat_with_timeout(prompt)

        return result

    def _add_documents(self, documents, filenames):
        self.collection.add(
            documents=documents,
            ids=filenames
        )

            

