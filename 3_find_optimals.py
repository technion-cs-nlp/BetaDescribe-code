import networkx as nx
import evaluate
import os
import pandas as pd
import sys
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="BetaDescribe: find optimal descriptions")

    parser.add_argument("--protein_name", type=str, help="Input protein name", default='protein')
    parser.add_argument("--working_dir", type=str, required=True, help="Path to save predictions")
    
    parser.add_argument("--rejection_results_file_name", type=str, help="Rejection results file name", default='rejection_summary')
    parser.add_argument("--optimal_results_file_name", type=str, help="Optimal descriptions file name", default='optimal_results')
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    protein_name = args.protein_name
    
    df_path = os.path.join(args.working_dir, f'{protein_name}_{args.rejection_results_file_name}.csv')
    
    df = pd.read_csv(df_path)

    df = df[df["is_rejected_origin_and_cell_location"] == True]

    chrf = evaluate.load("chrf")

    list_of_rows = []

    for protein, df_specific_protein in df.groupby(by=["protein_name"]):
        df_specific_protein.reset_index(inplace=True)
        df_specific_protein['ID'] = df_specific_protein.prediction_type.map(str) + "_" + df_specific_protein.alterntive_num.map(str)
        df_specific_protein = df_specific_protein.drop_duplicates(subset=['ID'], keep='last')
        df_specific_protein.reset_index(inplace=True)
        G = nx.Graph()
        edges = {}
        for _, row_1 in df_specific_protein.iterrows():
            for _, row_2 in df_specific_protein.iterrows():
                if not row_1['ID'] in list(G.nodes):
                    G.add_node(row_1['ID'])
                if not row_2['ID'] in list(G.nodes):
                    G.add_node(row_2['ID'])
                if row_1['ID'] == row_2['ID']:
                    continue
                rows_title = f"{row_1['ID']}-{row_2['ID']}"
                rows_title_reveresed = f"{row_2['ID']}-{row_1['ID']}"
                if rows_title in edges or rows_title_reveresed in edges:
                    continue
                chrf_score_1 = chrf.compute(predictions=[row_1['prediction_str']], references=[row_2['prediction_str']])['score'] / 100
                chrf_score_2 = chrf.compute(predictions=[row_2['prediction_str']], references=[row_1['prediction_str']])['score'] / 100
                # not a distance but a score
                # 0 weight is no link -> the higher the wieght the closer are the nodes
                chrf_score = (chrf_score_1 + chrf_score_2) / 2
                edges[rows_title] = chrf_score
                edges[rows_title_reveresed] = chrf_score
                #print(row_1['ID'], row_2['ID'], edges[rows_title])
                G.add_edge(row_1['ID'], row_2['ID'], weight = edges[rows_title])
        
        try:
            communites = nx.community.louvain_communities(G, seed=123, resolution=1.1)
        except Exception as e:
            communites = []
            pass
        
        backup_communites = None
        
        if len(G.nodes) > 8:
            res = 0.9
            
            while res < 1.4:
                if not (len(communites) > 10 or len(communites) <= 2):
                    if len(communites) == 2:
                        backup_communites = communites
                    break
                #print(res, len(communites))
                try:
                    communites = nx.community.louvain_communities(G, seed=123, resolution=res)
                except Exception as e:
                    print(e)
                    pass
                
                res += 0.01
        
        if backup_communites:
            communites = backup_communites
        
        communites.sort(reverse=True,key=len)
        #print(communites)
        if len(G.nodes) == 1:
            print(df_specific_protein.iloc[0]['prediction_str'])
            prediction_str = df_specific_protein.iloc[0]['prediction_str']
            list_of_rows.append({'protein': protein, 'option': 0, 'prediction_str': prediction_str})
            continue
        
        
        if len(communites[0]) > 1:
            for idx, communi in enumerate(communites):
                if idx >= 3:
                    break
                max_node = (None, -1)
                for node1 in communi:
                    sum_weights = 0
                    for node2 in communi:
                        if node1 == node2:
                            continue
                        title = f"{node1}-{node2}"
                        sum_weights += edges[title]
                    if len(communi) > 1:
                        average_node = sum_weights / (len(communi) - 1)
                    else:
                        average_node = sum_weights
                    if average_node > max_node[1]:
                        max_node = (node1, average_node)
                print(max_node)
                prediction_str = df_specific_protein.loc[df_specific_protein['ID'] == max_node[0], 'prediction_str'].item()
                print(max_node[0], prediction_str)
                list_of_rows.append({'protein': protein, 'option': idx, 'prediction_str': prediction_str})
        else:
            # no communites
            nodes_scores = []
            for _, row_1 in df_specific_protein.iterrows():
                sum_weights = 0
                for _, row_2 in df_specific_protein.iterrows():
                    node1 = row_1['ID']
                    node2 = row_2['ID']
                    if node1 == node2:
                        continue
                    title = f"{node1}-{node2}"
                    sum_weights += edges[title]
                average_node = sum_weights / (len(df_specific_protein.index) - 1)
                nodes_scores.append({'node': node1, 'average': average_node})
            nodes_scores.sort(reverse=True, key=lambda d: d['average'])
            for idx, node in enumerate(nodes_scores[0:min(len(nodes_scores), 3)]):
                prediction_str = df_specific_protein.loc[df_specific_protein['ID'] == node['node'], 'prediction_str'].item()
                print(node['node'], prediction_str)
                list_of_rows.append({'protein': protein, 'option': idx, 'prediction_str': prediction_str})

    results_df = pd.DataFrame(list_of_rows)
    results_df.to_csv(os.path.join(args.working_dir, f'{protein_name}_{args.optimal_results_file_name}.csv'))
