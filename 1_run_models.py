import argparse
import json
import os
import pandas as pd
from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer
from transformers import LlamaForCausalLM, LlamaTokenizer, set_seed
import torch
from itertools import groupby


DESCRIPTION_KEYS = ["FUNCTION$", "CATALYTIC ACTIVITY$", "PATHWAY$", "SUBCELLULAR LOCATION$", "DOMAIN$", "COFACTOR$", "PTM$", "SUBUNIT$", "SIMILARITY$", "INDUCTION$", "MISCELLANEOUS$", "ACTIVITY REGULATION$", "keywords:", "features:"]

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def parse_arguments():
    parser = argparse.ArgumentParser(description="BetaDescribe: generate predictions")

    parser.add_argument("--protein_sequence", type=str, required=True, help="Input protein sequence")
    parser.add_argument("--protein_name", type=str, help="Input protein name", default='protein')
    
    parser.add_argument("--id2label_path_cell_location", type=str, required=True, help="Path to cell location id2label JSON file")
    parser.add_argument("--label2id_path_cell_location", type=str, required=True, help="Path to cell location label2id JSON file")
    parser.add_argument("--model_path_cell_location", type=str, required=True, help="Path to cell location model")

    parser.add_argument("--id2label_path_origin", type=str, required=True, help="Path to origin id2label JSON file")
    parser.add_argument("--label2id_path_origin", type=str, required=True, help="Path to origin label2id JSON file")
    parser.add_argument("--model_path_origin", type=str, required=True, help="Path to origin model")

    parser.add_argument("--id2label_path_enzymes", type=str, required=True, help="Path to enzymes id2label JSON file")
    parser.add_argument("--label2id_path_enzymes", type=str, required=True, help="Path to enzymes label2id JSON file")
    parser.add_argument("--model_path_enzymes", type=str, required=True, help="Path to enzymes model")

    parser.add_argument("--base_model", type=str, required=True, help="Path to base model")
    parser.add_argument("--working_dir", type=str, required=True, help="Path to save predictions")

    parser.add_argument("--temperature", type=float, default=1.0, help="Temperature for generation")
    parser.add_argument("--num_of_descritpions", type=int, default=15,help="Number of description per prompt")
    parser.add_argument("--max_sequence_length", type=int, default=1536, help="Maximum number of tokens per generation")
    parser.add_argument("--validators_results_name", type=str, help="Validators file name", default='validators_results')
    return parser.parse_args()

def provide_simple_print(text):
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
            idx -= 2
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

    return {'clean': description, 'raw': text}


def create_json_files(path2folder, predicted_description, primaryAccession, protein_sequence, num_prediction):
    predicted_description_dict = provide_simple_print(predicted_description)
    predicted_description_dict['sequence'] = protein_sequence
    if not "FUNCTION$" in predicted_description_dict["clean"]:
        print(f'failed to predict, for predictino num : {num_prediction}')
        return
    os.makedirs(path2folder, exist_ok=True)
        
    with open(os.path.join(path2folder, f'{primaryAccession}_{num_prediction}_prediction.json'), 'w') as f:
        json.dump(predicted_description_dict, f)

def create_multi_samples(prompt, title, protein_name, protein_seq, tokenizer, model, json_path, temp, num_sequences, max_sequence):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    sample_outputs = model.generate(
        **inputs, 
        max_length=min(inputs.input_ids.shape[1] + 1024, max_sequence), 
        do_sample=True,
        temperature=temp,
        num_return_sequences=num_sequences,
    )
    
    for sample_idx, sample_output in enumerate(sample_outputs):
        output_str = tokenizer.decode(sample_output, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        create_json_files(
            json_path,
            output_str,
            f'{protein_name}{title}',
            protein_seq,
            sample_idx
        )

def create_pipe(label2id_path, id2label_path, model_path, problem_type=None):
    with open(label2id_path) as f:
        label2id = json.load(f)

    with open(id2label_path) as f:
        id2label_tmp = json.load(f)

    id2label = {}
    for key, value in id2label_tmp.items():
        id2label[int(key)] = value

    model = AutoModelForSequenceClassification.from_pretrained(
        model_path, num_labels=len(label2id.keys()),
        id2label=id2label, label2id=label2id,
        problem_type=problem_type
    )

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    return TextClassificationPipeline(model=model, tokenizer=tokenizer, device=DEVICE, return_all_scores=True)

if __name__ == "__main__":
    args = parse_arguments()

    os.makedirs(args.working_dir, exist_ok=True)

    pipe_cell_location = create_pipe(args.label2id_path_cell_location, args.id2label_path_cell_location, args.model_path_cell_location, "multi_label_classification")
    pipe_origin = create_pipe(args.label2id_path_origin, args.id2label_path_origin, args.model_path_origin)
    pipe_enzymes = create_pipe(args.label2id_path_enzymes, args.id2label_path_enzymes, args.model_path_enzymes)

    tokenizer = LlamaTokenizer.from_pretrained(args.base_model)
    model = LlamaForCausalLM.from_pretrained(args.base_model, torch_dtype=torch.bfloat16, use_flash_attention_2=True)
    model = model.to(DEVICE)

    set_seed(42)
    model.eval()

    with torch.no_grad():
        title = args.protein_name
        protein = args.protein_sequence
        print(f'title = {title}, protein = {protein}')
        validators_predictions = {'cell_location': [], 'origin': [], 'enzymes': []}
        for res in pipe_cell_location(protein)[0]:
            if res['score'] > 0.2:
                validators_predictions['cell_location'].append(res)
        
        for res in pipe_origin(protein)[0]:
            if res['score'] > 0.5:
                validators_predictions['origin'].append(res)
        
        for res in pipe_enzymes(protein)[0]:
            if res['score'] > 0.5:
                validators_predictions['enzymes'].append(res)
        
        with open(os.path.join(args.working_dir, f'{title}_{args.validators_results_name}.json'), 'w') as f:
            json.dump(validators_predictions, f)
        
        create_multi_samples("protein sequence: " + protein + " description: ", '', title, protein, tokenizer, model, args.working_dir, args.temperature, args.num_of_descritpions, args.max_sequence_length)
        create_multi_samples("protein sequence: " + protein + " description: FUNCTION$", '_with_FUNCTIONS_at_DESCRIPTION', title, protein, tokenizer, model, args.working_dir, args.temperature, args.num_of_descritpions, args.max_sequence_length)
        create_multi_samples("protein sequence: " + protein + " description:  FUNCTION$", '_with_FUNCTIONS_and_space_at_DESCRIPTION', title, protein, tokenizer, model, args.working_dir, args.temperature, args.num_of_descritpions, args.max_sequence_length)
