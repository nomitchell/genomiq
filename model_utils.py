from Bio.Seq import Seq
import os
import shutil
import requests
from bs4 import BeautifulSoup


class mo_utils():
    def generate_fasta(dna):
        header = ">sp|AA"

        sequence = str(mo_utils._to_amino(dna))
        print(sequence)
        #sequence = "MALKSLVLLSLLVLVLMALKSLVLLSLLVLVLMALKSLVLLSLLVLVL"
        
        with open("input/structure/temp.fasta", 'w') as f:
            f.write(header)
            f.write("\n")
            f.write(sequence)

    def clean_folder():
        folder_path = "output/verify"
        
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Removed file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")

        print("Done cleaning output/verify")

    def get_z_score(fp):
        url = 'https://prosa.services.came.sbg.ac.at/prosa.php'

        with open(fp, 'rb') as pdb_file:
            files = {'userfile': pdb_file}
            data = {'max_file_size': '26214400'}
            
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                zscore_element = soup.find('span', class_='zscore')
                if zscore_element:
                    zscore = zscore_element.get_text(strip=True)
                    return zscore
                else:
                    print("Failed to find z score")
                    return 10000000
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
                return 10000000
    
    def _to_amino(dna):
        seq = Seq(dna)
        translated = seq.translate().replace("*", "")
        
        return translated
            