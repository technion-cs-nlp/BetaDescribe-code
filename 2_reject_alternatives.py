import pandas as pd
import subprocess
import glob
import os
import json
import sys
import re
from openai import OpenAI
import argparse


DESCRIPTION_KEYS = ["FUNCTION$", "CATALYTIC ACTIVITY$", "PATHWAY$", "SUBCELLULAR LOCATION$", "DOMAIN$", "COFACTOR$", "PTM$", "SUBUNIT$", "SIMILARITY$", "INDUCTION$", "MISCELLANEOUS$", "ACTIVITY REGULATION$", "keywords:", "features:"]

DESCRIPTION_KEYS_FOR_EVALUATION = ["FUNCTION$", "CATALYTIC ACTIVITY$", "PATHWAY$", "SUBCELLULAR LOCATION$", "DOMAIN$", "COFACTOR$", "PTM$", "SUBUNIT$", "SIMILARITY$", "INDUCTION$", "MISCELLANEOUS$", "ACTIVITY REGULATION$"]

def parse_arguments():
    parser = argparse.ArgumentParser(description="BetaDescribe: reject alternatives")

    parser.add_argument("--protein_name", type=str, help="Input protein name", default='protein')
    parser.add_argument("--working_dir", type=str, required=True, help="Path to save predictions")
    
    parser.add_argument("--results_file_name", type=str, help="Results file name", default='rejection_summary')
    parser.add_argument("--validators_results_name", type=str, help="Validators file name", default='validators_results')
    
    parser.add_argument("--chat_gpt_api_key", type=str, required=True, help="ChatGPT api key")
    return parser.parse_args()

def provide_simple_print(text, title = ''):
    words_in_sentence = text.split()
    idx_for_word = 0
    preivous_idx_for_word = 0
    key = ''
    previous_key = ''
    previous_word = ''
    description = {}
    for idx, word in enumerate(words_in_sentence):
        last_two_words = f'{previous_word} {word}'
        if last_two_words == 'protein sequence:' and idx > 4:
            idx -= 1
            break
        if last_two_words in DESCRIPTION_KEYS:
            idx_for_word = idx
            key = word
            if previous_key != '':
                description[previous_key] = description.get(previous_key, [])
                description[previous_key].append(" ".join(words_in_sentence[preivous_idx_for_word+1: idx - 1]))
            preivous_idx_for_word = idx_for_word
            previous_key = last_two_words
        
        if word in DESCRIPTION_KEYS:
            idx_for_word = idx
            key = word
            if previous_key != '':
                description[previous_key] = description.get(previous_key, [])
                description[previous_key].append(" ".join(words_in_sentence[preivous_idx_for_word+1: idx]))
            preivous_idx_for_word = idx_for_word
            previous_key = key
        previous_word = word
    
    description[previous_key] = description.get(previous_key, [])
    description[previous_key].append(" ".join(words_in_sentence[preivous_idx_for_word+1:idx + 1]))

    return description


def create_meaningful_str(dict2process):
    str2return = ''
    for key in DESCRIPTION_KEYS_FOR_EVALUATION:
        if key in dict2process:
            str2return += f'{key} {" & ".join(dict2process[key])}'
    return str2return



if __name__ == "__main__":
    args = parse_arguments()
    protein_name = args.protein_name
    
    validators_results_path = os.path.join(args.working_dir, f'{protein_name}_{args.validators_results_name}.json')
    
    list_of_rows_for_df = []

    client = OpenAI(
        api_key=args.chat_gpt_api_key
    )
    if not os.path.isfile(validators_results_path):
        exit(f'validators_results_path not aviable for protein {protein_name}, path {validators_results_path}')
    
    with open(validators_results_path, 'r') as f:
        validators_data = json.load(f)
    
    if validators_data["enzymes"][0]["label"] == "not_enzyme":
        is_enzyme = False
    elif validators_data["enzymes"][0]["label"] == "enzyme":
        is_enzyme = True
    else:
        print(f'error enzyme not declated protein = {protein} enzymes = {validators_data["enzymes"]}')
    
    cell_locations = [x['label'] for x in validators_data['cell_location']]
    
    if len(validators_data['origin']) and 'label' in validators_data['origin'][0]:
        origin = validators_data['origin'][0]['label']
    else:
        origin = None
    
    for file_prediction in glob.glob(f'{args.working_dir}/{protein_name}_*'):
        file_name = os.path.basename(file_prediction)
        
        if not 'prediction' in file_name:
            continue
        if 'with_FUNCTIONS_and_space_at_DESCRIPTION' in file_name:
            prediction_type = 'with_space_and_function'
        elif 'with_FUNCTIONS_at_DESCRIPTION' in file_name:
            prediction_type = 'with_function'
        else:
            prediction_type = 'solo'
        
        alterntive_num = re.findall(r'\d+', file_name)[-1]
        
        if not os.path.exists(file_prediction):
            exit(f'file_prediction = {file_prediction} doesn not exists')
            continue
        with open(file_prediction, 'r') as f:
            try:
                prediction_data = json.load(f)
            except:
                prediction_data = {'clean': {'': 'failed'}, 'raw': 'failed'}
        prediction_str = create_meaningful_str(prediction_data['clean'])
        line_lower = prediction_str.lower()
        
        # check if prediction is enzyme
        if 'enzyme' in line_lower and not 'enzyme]' in line_lower and 'belongs to' in line_lower and 'family' in line_lower:
            location_belongs_to = line_lower.find('belongs to')
            if 'enzyme' in line_lower[location_belongs_to: location_belongs_to + 200]:
                is_predicted_enzyme = True
        elif 'catalytic activity$' in line_lower:
            is_predicted_enzyme = True
        else:
            is_predicted_enzyme = False
        is_okay_with_enzyme = is_predicted_enzyme == is_enzyme
        
        
        prompt_system = '''You're a biology expert, and you can answer only yes or no. No explanation is needed.\n'''
        
        
        # reject by origin
        if origin:
            if validators_data['origin'][0]['score'] > 0.9:
                prompt_origin = f'''We are certain that the following protein belongs to the {origin}.\n'''
            else:
                prompt_origin = f'''We think that the following protein belongs to the {origin}.\n'''
            prompt_origin += f'''Do you think the following function is possible? please answer yes or no only.\n'''
            prompt_origin += f'''{prediction_data['clean']['FUNCTION$'][0]}'''
            
            is_okay_with_origin = None
            if is_okay_with_enzyme:
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt_system},
                        {"role": "user", "content": prompt_origin}
                ])
                if "yes" in str(completion.choices[0].message.content).lower():
                    is_okay_with_origin = True
                elif "no" in str(completion.choices[0].message.content).lower():
                    is_okay_with_origin = False
        else:
            is_okay_with_origin = True
        
        
        
        # reject by cell location
        #prompt_cell_location = '''You're a biology expert, and you can answer only yes or no. No explanation is needed.\n'''
        prompt_cell_location = f'''The protein subcellular localization is probably in one or more of the following locations: {cell_locations}\n'''
        prompt_cell_location += f'''Do you think the following function is possible? please answer yes or no only.\n'''
        prompt_cell_location += f'''{prediction_data['clean']['FUNCTION$'][0]}'''
        
        is_okay_with_cell_location = None
        if is_okay_with_enzyme and is_okay_with_origin:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_cell_location}
            ])
            if "yes" in str(completion.choices[0].message.content).lower():
                is_okay_with_cell_location = True
            elif "no" in str(completion.choices[0].message.content).lower():
                is_okay_with_cell_location = False
        
        # reject by origin & cell location
        #prompt_origin_and_cell_location = '''You're a biology expert, and you can answer only yes or no. No explanation is needed.\n'''
        if origin:
            if validators_data['origin'][0]['score'] > 0.9:
                prompt_origin_and_cell_location = '''We are certain that the following protein belongs to the {origin}.\n'''
            else:
                prompt_origin_and_cell_location = '''We think that the following protein belongs to the {origin}.\n'''
            prompt_origin_and_cell_location += f'''In addition, the protein subcellular localization is probably in one or more of the following locations: {cell_locations}\n'''
            prompt_origin_and_cell_location += f'''Do you think the following function is possible? please answer yes or no only.\n'''
            prompt_origin_and_cell_location += f'''{prediction_data['clean']['FUNCTION$'][0]}'''
            is_okay_with_origin_and_cell_location = None
            if is_okay_with_enzyme and is_okay_with_origin and is_okay_with_cell_location:
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt_system},
                        {"role": "user", "content": prompt_origin_and_cell_location}
                ])
                if "yes" in str(completion.choices[0].message.content).lower():
                    is_okay_with_origin_and_cell_location = True
                elif "no" in str(completion.choices[0].message.content).lower():
                    is_okay_with_origin_and_cell_location = False
        else:
            is_okay_with_origin_and_cell_location = True
        
        list_of_rows_for_df.append({
            'protein_name': protein_name,
            'prediction_type': prediction_type,
            'alterntive_num': alterntive_num,
            'prediction_str': prediction_str,
            'is_rejected_by_enzmye': is_okay_with_enzyme,
            'is_rejected_origin': is_okay_with_origin,
            'is_rejected_cell_location': is_okay_with_cell_location,
            'is_rejected_origin_and_cell_location': is_okay_with_origin_and_cell_location,
        })
    
    
    df = pd.DataFrame(list_of_rows_for_df)
    os.makedirs(args.working_dir, exist_ok=True)
    df.to_csv(os.path.join(args.working_dir, f'{protein_name}_{args.results_file_name}.csv'), index=False)
