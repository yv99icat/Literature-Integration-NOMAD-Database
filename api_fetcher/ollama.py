import subprocess
import time
import pandas as pd
import pickle

def ask_ollama(prompt, model="mistral"):
    result = subprocess.run(
        ['ollama', 'run', model],
        input=prompt.encode(),
        capture_output=True
    )
    return result.stdout.decode()


#example usage

abstract_text = """
We modulated a solvent-mediated adduct for one-step crystallization of lead-free AgBi2I7 at a lower temperature (90 °C)
 and to obtain remnant BiI3 by controlling the nature of the substrate and precursor concentration. 
"""

raw_abstracts = pd.read_csv("cleaned_abstracts.csv")

raw_abstracts = raw_abstracts["abstracts"]

label_list_text = ['zno based',
 'ticl4 treatment',
 'nio films',
 'niox film',
 'device stability',
 'sheet resistance',
 'device performance',
 'organic inorganic',
 'carbon based',
 'small molecule',
 'titanium dioxide',
 'cu cu2o',
 'fluorine doped',
 'tin oxide',
 'photovoltaic performance',
 '3d hybrid',
 'csxfa1 xpbi3',
 'low temperature',
 'ambient conditions',
 'black phase',
 'pedot pss',
 'material htm',
 'f4 tcnq',
 'layer etl',
 'metal substrate',
 'open circuit',
 'bending cycles',
 'highly efficient',
 'aspect ratio',
 'spacer cations',
 'layer htl',
 'designed synthesized',
 'ma 3pb4i13',
 'high performance',
 'cesium lead',
 'relative humidity',
 'hole transporting',
 'active layers',
 'spiro ometad',
 'metal halide',
 'formula text',
 'spray pyrolysis',
 'quasi 2d',
 'band alignment',
 'solution processed',
 'composite electrode',
 'dopant free',
 'nickel oxide',
 'binding energy',
 'efficient stable',
 'power sources',
 'materials htms',
 'counter electrode',
 'efficiency pce',
 'low cost',
 'tio2 layer',
 'high quality',
 'radius mm',
 'inverted planar',
 'wearable electronics',
 'cells pscs',
 'devices based',
 'hole blocking',
 'crystal growth',
 'htm free',
 'band gap',
 'charge carrier',
 'flexible pescs',
 'circuit current',
 'charge recombination',
 'sol gel',
 'large area',
 'tetrakis di',
 'work function',
 'transparent conductive',
 'energy levels',
 'hole extraction',
 'surface modification',
 'graphene oxide',
 'long term',
 'ruddlesden popper',
 'thermal stability',
 'circuit voltage',
 'electron extraction']





#This is our prompt
prompt = f"""
start from scratch
System Prompt: You are a strict JSON generator.
You will ONLY output a single JSON object with the assigned label.
You MUST NOT output any explanations, instructions, formatting guides, or any additional text.

If you disobey, your response will be discarded.

Your task:
- You are a lead professor and your task is  classifying scientific abstracts.
 -Assign exactly ONE label from the allowed list.
- Use ONLY the labels provided.
- No invented labels.
-labels from the list only 
- for each of them in raw_abstracts assign a label 

Allowed labels:
{label_list_text}

Format:
{{
  "assigned_label": "chosen_label_from_list"
}}

Input Abstract:
\"\"\"
{abstract_text}
\"\"\"

Respond ONLY with the JSON object.
"""
# prompt = "are you there ? "


start_time = time.time()  # ⏱️ Start
response = ask_ollama(prompt)
print("Predicted topic:", response.strip())
end_time = time.time()  # ⏱️ End

elapsed = end_time - start_time  # ⏱️ Duration

print(f"{elapsed:.2f} seconds")


print("----------------------------")

print(raw_abstracts[0:5])


# load the list from contrastive

with open("../embedding_clustering/final_label_list.pkl", 'rb') as f:
 loaded_list = pickle.load(f)

print("-----------------")

print(loaded_list)
