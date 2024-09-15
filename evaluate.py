from tqdm import tqdm
import cohere
import subprocess
from model_utils import mo_utils
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import threading
import time

def get_rank_1_path(folder_path):
    search_pattern = os.path.join(folder_path, 'sp_AA_unrelaxed_rank_001_alphafold2_ptm_model_*.pdb')
    
    files = glob.glob(search_pattern)
    
    rank_1_files = [file for file in files if 'rank_001' in os.path.basename(file)]
    return rank_1_files[0] if rank_1_files else None

def verify_structure(dna):
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
        fname = get_rank_1_path(folder_path)

        with open(fname, 'r') as file:
            lines = file.readlines()
            lines = lines[1:]

        with open(fname, 'w') as file:
            file.writelines(lines)

        # access prosa site, make post, scrape results

        z_score = mo_utils.get_z_score(fname)

        print("Z score", z_score)

        return float(z_score)

co = cohere.Client(os.environ["COHERE_API_KEY"])

def co_chat_with_timeout(prompt, tune):
    # Define a function to run the co.chat call
    def target():
        nonlocal result
        try:
            if tune:
                result = co.chat(message=prompt, model='c4e6f320-6a12-4385-ba5d-d39bc8935c0b-ft')
            else:
                result = co.chat(message=prompt)
        except Exception as e:
            result = str(e)

    # Initialize the result
    result = None

    # Create and start the thread
    thread = threading.Thread(target=target)
    thread.start()
    
    # Wait for the thread to complete or timeout
    thread.join(5)

    if thread.is_alive():
        # Timeout occurred, handle it
        print("Operation timed out. Retrying...")
        thread.join()  # Ensure the thread finishes
        return co_chat_with_timeout(prompt, timeout)  # Retry

    return result

def main():
    with open("prompts/generate.txt", 'r') as f:
        generate_prompt = f.read()

    # run through all 100 questions
    # first naive model, then fine tuned
    # generate string, then fold, repeat

    with open("dataset/evaluation/questions.txt", 'r') as f:
        questions = f.readlines()

    z_score_hist_no = []
    z_score_hist_tune = []

    for question in tqdm(questions):
        prompt = generate_prompt + "\n" + question
        
        # first no tune
        print('starting gen no tune')
        # using ft-ed model
        response = co_chat_with_timeout(prompt, False)
        print("done gen")
        print(response)
        dna = response.text
        z_score = verify_structure(dna)
        z_score_hist_no.append(z_score)

        # now fine tuned version

        print("starting gen tune")
        response = co_chat_with_timeout(prompt, True)
        print("done gen tune")

        dna = response.text
        z_score = verify_structure(dna)
        z_score_hist_tune.append(z_score)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.hist(z_score_hist_no, bins=30, alpha=0.5, label='Normal Model', color='blue')
    plt.hist(z_score_hist_tune, bins=30, alpha=0.5, label='Fine-Tuned Model', color='red')
    plt.xlabel('Z-score')
    plt.ylabel('Frequency')
    plt.title('Histogram of Z-scores')
    plt.legend()

    # Create a box plot to compare spread and median
    plt.subplot(1, 2, 2)
    plt.boxplot([z_score_hist_no, z_score_hist_tune], labels=['Normal Model', 'Fine-Tuned Model'])
    plt.ylabel('Z-score')
    plt.title('Box Plot of Z-scores')

    # Save plots as images
    plt.tight_layout()
    plt.savefig('z_score_comparison.png')
    plt.show()

main()



