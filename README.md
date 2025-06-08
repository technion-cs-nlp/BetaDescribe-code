# Protein2Text: Providing Rich Descriptions from Protein Sequences
## Abstract:
Understanding the functionality of proteins has been a focal point of biological research due to their critical roles in various biological processes. Unraveling protein functions is essential for advancements in medicine, agriculture, and biotechnology, enabling the development of targeted therapies, engineered crops, and novel biomaterials. However, this endeavor is challenging due to the complex nature of proteins, requiring sophisticated experimental designs and extended timelines to uncover their specific functions. Public large language models (LLMs), though proficient in natural language processing, struggle with biological sequences due to the unique and intricate nature of biochemical data. These models often fail to accurately interpret and predict the functional and structural properties of proteins, limiting their utility in bioinformatics. To address this gap, we introduce BetaDescribe, a collection of models designed to generate detailed and rich textual descriptions of proteins, encompassing properties such as function, catalytic activity, involvement in specific metabolic pathways, subcellular localizations, and the presence of particular domains. The trained BetaDescribe model receives protein sequences as input and outputs a textual description of these properties. BetaDescribe’s starting point was the LLAMA2 model, which was trained on trillions of tokens. Next, we trained our model on datasets containing both biological and English text, allowing biological knowledge to be incorporated. We demonstrate the utility of BetaDescribe by providing descriptions for proteins that share little to no sequence similarity to proteins with functional descriptions in public datasets. We also show that BetaDescribe can be harnessed to conduct *in-silico* mutagenesis procedures to identify regions important for protein functionality without needing homologous sequences for the inference. Altogether, BetaDescribe offers a powerful tool to explore protein functionality, augmenting existing approaches such as annotation transfer based on sequence or structure similarity. 

![alt text](https://github.com/technion-cs-nlp/BetaDescribe-code/blob/main/outline_image.png)

BetaDescribe workflow. The generator processes the protein sequences and creates multiple candidate descriptions. Independently, the validators provide simple textual properties of the protein. The judge receives the candidate descriptions (from the generator) and the predicted properties (from the validators) and rejects or accepts each description. Finally, BetaDescribe provides up to three alternative descriptions for each protein.


## Examples of descriptions of unknown proteins:


### SnRV-Env:

Sequence:
MKLVLLFSLSVLLGTSVGRILEIPETNQTRTVQVRKGQLVQLTCPQLPPPQGTGVLIWGRNKRTGGGALDFNGVLTVPVGDNENTYQCMWCQNTTSKNAPRQKRSLRNQPTEWHLHMCGPPGDYICIWTNKKPVCTTYHEGQDTYSLGTHRKVLPKVTEACAVGQPPQIPGTYVASSKGWTMFNKFEVHSYPANVTQIKTNRTLHDVTLWWCHDNSIWRCTQMGFIHPHQGRRIQLGDGTRFRDGLYVIVSNHGDHHTVQHYMLGSGYTVPVSTATRVQMQKIGPGEWKIATSMVGLCLDEWEIECTGFCSGPPPCSLSITQQQDTVGGSYDSWNGCFVKSIHTPVMALNLWWRRSCKGLPEATGMVKIYYPDQFEIAPWMRPQPRQPKLILPFTVAPKYRRQRRGLNPSTTPDYYTNEDYSGSGGWEINDEWEYIPPTVKPTTPSVEFIQKVTTPRQDKLTTVLSRNKRGVNIASSGNSWKAEIDEIRKQKWQKCYFSGKLRIKGTDYEEIDTCPKPLIGPLSGFIPTGVTKTLKTGVTWTTAVVKIDLQQWVDILNSTCKDTLIGKHWIKVIQRLLREYQKTGVTFNLPQVQSLPNWETKNKDNPGHHIPKSRRKRIRRGLGEALGLGNFADNRWKDLQIAGLGVEQQKLMGLTREATFEAWNALKGISNELIKWEEDMVATLRQLLLQIKGTNTTLCSAMGPLMATNIQQIMFALQHGNLPEMSYSNPVLKEIAKQYNGQMLGVPVETTGNNLGIMLSLPTGGENIGRAVAVYDMGVRHNRTLYLDPNARWIHNHTEKSNPKGWVTIVDLSKCVETTGTIYCNEHGFRDRKFTKGPSELVQHLAGNTWCLNSGTWSSLKNETLYVSGRNCSFSLTSRRRPVCFHLNSTAQWRGHVLPFVSNSQEAPNTEIWEGLIEEAIREHNKVQDILTKLEQQHQNWKQNTDNALQNMKDAIDSMDNNMLTFRYEYTQYGLFIVCLLAFLFAVIFGWLCGVTVRLREVFTILSVKIHALKSQAHQLAMLRGLRDPETGEQDRQAPAYREPPTYQEWARRRGGRPPIVTFLIDRETGERHDGQIFQPIRNRSNQVHRPQPPRPTAPNPDNQRPIREPRPEEPEHGDFLQGASWMWQ

Description:
_**FUNCTION$** The leader peptide is a component of released, infectious virions and is required for particle budding, & The transmembrane protein (TM) acts as a class I viral fusion protein. Under the current model, the protein has at least 3 conformational states: pre-fusion native state, pre-hairpin intermediate state, and post-fusion hairpin state. During viral and target cell membrane fusion, the coiled coil regions (heptad repeats) assume a trimer-of-hairpins structure, positioning the fusion peptide in close proximity to the C-terminal region of the ectodomain. The formation of this structure appears to drive apposition and subsequent fusion of viral and target cell membranes. Membranes fusion leads to delivery of the nucleocapsid into the cytoplasm, **SUBCELLULAR LOCATION$** Endoplasmic reticulum membrane._


### TGV-S:

Sequence:
MISGHTLCMLVLFYLYSYSNAQHELQLNPTTYHWLNCATSDCKSWQACPSTQATTCVSFSYTGLAWHKQDNTIIGYSNFTSQSLYDTISYTFAPSYVLSHAMTNLEPQKLCSLKSTIQSFHGFTPADCCLNPSASPACSYFSTGDTSFITGTPYQCTASYYGYGSPYGTDCEPYFASVSPYGTSVTPSGDVFTNFGEKSVHTYDCFYENWARYRPAPYTNNPSDPRWNLCHSIYYYVWTLSDTNHQFTTVESEPGDKVIMKQLSSHTPVYLTLGGWTSNNTVLYQAISSRRLDTIAMLRDLHDNYGVTGVCIDFEFIGGSNQYSNIFLLDWVPDLLSFLSSVRLEFGPSYYITFVGLAVGSHFLPTIYQQIDPLIDAWLISGYDLHGDWEVKATQQAALVDDPKSDFPTYSLFTSVDNMLAITTPDKIILGLPQYTRGVYTSLTGSTTGPYPPTTPMCPTPPACGTDIVISTSHGEIPSTHDTTKGDIIIEDPSQPKFYISKGSRNGRTFNHFFMNSTTASHIRSTLQPKGITRWYSYASSMNLQTNTNFKTALLSQSRKARQLSTYYKYPAPAGSGVTSCPGIVVFTDTFVVTTTAYAGSHALPLLDGNFYSPRSTFTCSPGFSTLMPTTTTRCSGIDPSNLLPSDSSSVSIVCPDMTFFGAKIAICASSTTTSKPTHLQLEVSTSIEGQFQFNSLPIYSQHKVSTTSFSVPYKCINFTPIPSCISSVCGSSHSCVTKLQESPASYACQSAAAIAIVYNNTLDLVKRSQTTTELLFNQVVLESSKFGVVTHTRQTRGLFGILSITSLIMSGVALATSSSALYVSIKNQAELSSLRNDVNSKFTTIDQNFDQITSKFNHLSTTTSDAFIAQSNINTQLQSSINQLQENLEVLSNFVTTQLSSVSSSITQLSEAIDALSDQVNYLAYLTSGISSYTSRLTSVTVQATNTAVKFSTLQSHLSNCLTSLQQQSFTGCIHKSGNIIPLKVVYTPFGNTRYLSFIYAEAELLGYQQYKSALSYCDQNFLYSSSPGCFFLLNGSSIDHRSSLSAACPTPATVVSMSCQNVTLDLSSQSIVRPYVFPLLNLTLPTPVKTNISFTPGKAPVFQNITQIDQTLLLDLAQQLQAIQLQLNPVGPISTSSFSPVVIALTVISAVVFLAVTSIVIYMLCKTAPFKPSRKTA

Descriptions:
1. _**FUNCTION$** Envelope glycoprotein that forms spikes at the surface of virion envelope. Essential for the initial attachment to heparan sulfate moities of the host cell surface proteoglycans. Involved in fusion of viral and cellular membranes leading to virus entry into the host cell. Following initial binding to its host receptors, membrane fusion is mediated by the fusion machinery composed at least of gB and the heterodimer gH/gL. May be involved in the fusion between the virion envelope and the outer nuclear membrane during virion egress, **SUBCELLULAR LOCATION$** Virion membrane, **SUBUNIT$** Homotrimer; disulfide-linked. Binds to heparan sulfate proteoglycans. Interacts with gH/gL heterodimer, **SIMILARITY$** Belongs to the herpesviridae glycoprotein B family._

2. _**FUNCTION$** The surface protein (SU) attaches the virus to the host cell by binding to its receptor. This interaction triggers the refolding of the transmembrane protein (TM) and is thought to activate its fusogenic potential by unmasking its fusion peptide. Fusion occurs at the host cell plasma membrane, & The transmembrane protein (TM) acts as a class I viral fusion protein. Under the current model, the protein has at least 3 conformational states: pre-fusion native state, pre-hairpin intermediate state, and post-fusion hairpin state. During viral and target cell membrane fusion, the coiled coil regions (heptad repeats) assume a trimer-of-hairpins structure, positioning the fusion peptide in close proximity to the C-terminal region of the ectodomain. The formation of this structure appears to drive apposition and subsequent fusion of viral and target cell membranes. Membranes fusion leads to delivery of the nucleocapsid into the cytoplasm, **SUBCELLULAR LOCATION$** Cell membrane. **SUBUNIT$** The mature envelope protein (Env) consists of a trimer of SU-TM heterodimers attached by noncovalent interactions or by a labile interchain disulfide bond_


### Protein 1 (TiLV virus):

Sequence:
MWAFQEGVCKGNLLSGPTSMKAPDSAARESLDRASEIMTGKSYNAVHTGDLSKLPNQGESPLRIVDSDLYSERSCCWVIEKEGRVVCKSTTLTRGMTGLLNTTRCSSPSELICKVLTVESLSEKIGDTSVEELLSHGRYFKCALRDQERGKPKSRAIFLSHPFFRLLSSVVETHARSVLSKVSAVYTATASAEQRAMMAAQVVESRKHVLNGDCTKYNEAIDADTLLKVWDAIGMGSIGVMLAYMVRRKCVLIKDTLVECPGGMLMGMFNATATLALQGTTDRFLSFSDDFITSFNSPAELREIEDLLFASCHNLSLKKSYISVASLEINSCTLTRDGDLATGLGCTAGVPFRGPLVTLKQTAAMLSGAVDSGVMPFHSAERLFQIKQQECAYRYNNPTYTTRNEDFLPTCLGGKTVISFQSLLTWDCHPFWYQVHPDGPDTIDQKVLSVLASKTRRRRTRLEALSDLDPLVPHRLLVSESDVSKIRAARQAHLKSLGLEQPTNFNYAIYKAVQPTAGC

Description:
_**FUNCTION$** Probably involved in the RNA silencing pathway and required for the generation of small interfering RNAs (siRNAs), **CATALYTIC ACTIVITY$** a ribonucleoside 5'-triphosphate + RNA(n) = diphosphate + RNA(n+1), **SIMILARITY$** Belongs to the RdRP family._


### Protein 2 (TiLV virus):

Sequence:
MSQFGKSFKGRTEVTITEYRSHTVKDVHRSLLTADKSLRKSFCFRNALNQFLDKDLPLLPIRPKLESRVAVKKSKLRSQLSFRPGLTQEEAIDLYNKGYDGDSVSGALQDRVVNEPVAYSSADNDKFHRGLAALGYTLADRAFDTCESGFVRAIPTTPCGFICCGPGSFKDSLGFVIKIGEFWHMYDGFQHFVAVEDAKFLASKSPSFWLAKRLAKRLNLVPKEDPSIAAAECPCRKVWEASFARAPTALDPFGGRAFCDQGWVYHRDVGYATANHISQETLFQQALSVRNLGPQGSANVSGSIHTALDRLRAAYSRGTPASRSILQGLANLITPVGENFECDLDKRKLNIKALRSPERYITIEGLVVNLDDVVRGFYLDKAKVTVLSRSKWMGYEDLPQKPPNGTFYCRKRKAMLLISCSPGTYAKKRKVAVQEDRFKDMRVENFREVAENMDLNQ

Description:
_**FUNCTION$** DNA-dependent RNA polymerase catalyzes the transcription of DNA into RNA using the four ribonucleoside triphosphates as substrates, **CATALYTIC ACTIVITY$** a ribonucleoside 5'-triphosphate + RNA(n) = diphosphate + RNA(n+1), **SIMILARITY$** Belongs to the RNA polymerase beta' chain family._


### Protein 3 (TiLV virus):

Sequence:
MDSRFAQLTGVFCDDFTYSEGSRRFLSSYSTVERRPGVPVEGDCYDCLKNKWIAFELEGQPRKFPKATVRCILNNDATYVCSEQEYQQICKVQFKDYLEIDGVVKVGHKASYDAELRERLLELPHPKSGPKPRIEWVAPPRLADISKETAELKRQYGFFECSKFLACGEECGLDQEARELILNEYARDREFEFRNGGWIQRYTVASHKPATQKILPLPASAPLARELLMLIARSTTQAGKVLHSDNTSILAVPVMRDSGKHSKRRPTASTHHLVVGLSKPGCEHDFEFDGYRAAVHVMHLDPKQSANIGEQDFVSTREIYKLDMLELPPISRKGDLDRASGLETRWDVILLLECLDSTRVSQAVAQHFNRHRLALSVCKDEFRKGYQLASEIRGTIPLSSLYYSLCAVRLRMTVHPFAR

Descriptions:
1. _**FUNCTION$** DNA-dependent RNA polymerase catalyzes the transcription of DNA into RNA using the four ribonucleoside triphosphates as substrates. Specific core component of RNA polymerase III which synthesizes small RNAs, such as 5S rRNA and tRNAs, **SUBCELLULAR LOCATION$** Nucleus, **SUBUNIT$** Component of the RNA polymerase III (Pol III) complex consisting of 17 subunits, **SIMILARITY$** Belongs to the eukaryotic RPC3/POLR3C RNA polymerase subunit family._

2. _**FUNCTION$** Decapping enzyme for NAD-capped RNAs: specifically hydrolyzes the nicotinamide adenine dinucleotide (NAD) cap from a subset of RNAs by removing the entire NAD moiety from the 5'-end of an NAD-capped RNA, **SUBCELLULAR LOCATION$** Nucleus, **COFACTOR$** a divalent metal cation, **SIMILARITY$** Belongs to the DXO/Dom3Z family._


## Scripts:

1: You can use the provided script `1_run_models.py` for the generation of the descriptions.

2: You can use the provided script `2_reject_alternatives.py` to reject alternatives.

3: You can use the provided script `3_find_optimals.py` to recive the three best descriptions.


## supports_files:

contains support files for predictions


## 1_run_models:

Generates the descriptions for proteins. Also predicts the origin, subcellular locations and if enzymes using the validators.


### Flags (1_run_models):

+ --protein_sequence (str, required): Input protein sequence.
+ --protein_name (str, optional): Input protein name. Default is 'protein'.
+ --id2label_path_cell_location (str, required): Path to cell location id2label JSON file (see supports_files).
+ --label2id_path_cell_location (str, required): Path to cell location label2id JSON file (see supports_files).
+ --model_path_cell_location (str, required): Path to cell location model.
+ --id2label_path_origin (str, required): Path to origin id2label JSON file (see supports_files).
+ --label2id_path_origin (str, required): Path to origin label2id JSON file (see supports_files).
+ --model_path_origin (str, required): Path to origin model.
+ --id2label_path_enzymes (str, required): Path to enzymes id2label JSON file (see supports_files).
+ --label2id_path_enzymes (str, required): Path to enzymes label2id JSON file (see supports_files).
+ --model_path_enzymes (str, required): Path to enzymes model.
+ --base_model (str, required): Path to base model.
+ --working_dir (str, required): Path to save predictions.
+ --temperature (float, optional): Temperature for generation. Default is 1.0.
+ --num_of_descriptions (int, optional): Number of descriptions per prompt. Default is 15.
+ --max_sequence_length (int, optional): Maximum number of tokens per generation. Default is 1536.
+ --validators_results_name (str, optional): Validators file name. Default is 'validators_results'.


### Examples (1_run_models):

```
python 1_run_models.py --protein_sequence "MSEQNNTEMTFQIQRIYTKDISFEAPNAPHVFQAKGNRITRSSDLAQELNAQVDWLTLSPLTLLHSNLADLSMKMLQEEGESYQEVPSPTFLGNEPISTVPVPPTQPSTTGLVNADGNSNNLALNDNFAVICNQRQSDMVKKRAVFESGAGEIGSKQLSRSILAVVEFLTEGDLHFSVFYNHEGYQFSNTHGGGEIRKLQNVNAELSHVGKDYQEDYAAEYSRVMERNYQSEIAPHLVGNNTLVQDYIKSIKKDVKGDQWRQAAKPNDAILWLKDNKYHPFAGPLSYNNLSSLMVELSYYIPDRLEESY" \
                      --protein_name "example_protein" \
                      --id2label_path_cell_location "/path/to/cell_location/id2label.json" \
                      --label2id_path_cell_location "/path/to/cell_location/label2id.json" \
                      --model_path_cell_location "/path/to/cell_location/model" \
                      --id2label_path_origin "/path/to/origin/id2label.json" \
                      --label2id_path_origin "/path/to/origin/label2id.json" \
                      --model_path_origin "/path/to/origin/model" \
                      --id2label_path_enzymes "/path/to/enzymes/id2label.json" \
                      --label2id_path_enzymes "/path/to/enzymes/label2id.json" \
                      --model_path_enzymes "/path/to/enzymes/model" \
                      --base_model "/path/to/base/model" \
                      --working_dir "/path/to/working/directory" \
                      --temperature 0.8 \
                      --num_of_descriptions 10 \
                      --max_sequence_length 1024 \
                      --validators_results_name "my_validators_results"
```

```
python 1_run_models.py --protein_sequence "MTMKMRILLTLALLALTLASPIRTLSSGLAYFETYLHIGYKTRNSEASKQQQQPPQPPPLIRAGAGLGGQFLVVATDGDGVNDSPHGDQMAKAVRKNGETGPESQERDNTAVRILMVEKEFSSLKCDEYFSTCIVTASDENGVSKYGLKPTHFLFVQISSSGLVAVDPVYANGGHTYVSGAGCISYRVGYRLPVGCVTLLTGYIGSGEITDGKKVVTIKTNWHSKTVVFYEDGSPSLLSKTPVFVNSDGVYHGNITVPFLKREAFHFLQSLPEFGTSHVLPVTWELRVKGVKEGECGSMTIRKVSFVHYPDPTITWVQTVLMQGYPGPSYHRPSTIQIRNLNFKLLEKTNVEVTYGSLAIAECAVMIRGIKNVNEVEPLTTVVSKTAPVPFPFHQKLNQTTVSDTHLEVT" \
                      --protein_name "example_protein" \
                      --id2label_path_cell_location "/path/to/cell_location/id2label.json" \
                      --label2id_path_cell_location "/path/to/cell_location/label2id.json" \
                      --model_path_cell_location "/path/to/cell_location/model" \
                      --id2label_path_origin "/path/to/origin/id2label.json" \
                      --label2id_path_origin "/path/to/origin/label2id.json" \
                      --model_path_origin "/path/to/origin/model" \
                      --id2label_path_enzymes "/path/to/enzymes/id2label.json" \
                      --label2id_path_enzymes "/path/to/enzymes/label2id.json" \
                      --model_path_enzymes "/path/to/enzymes/model" \
                      --base_model "/path/to/base/model" \
                      --working_dir "/path/to/working/directory" \
                      --temperature 1.2 \
                      --num_of_descriptions 20 \
                      --max_sequence_length 2048 \
                      --validators_results_name "custom_validators_results"
```


## 2_reject_alternatives.py

For each description, uses the validators prediction to check if the description is valid (using ChatGPT).


### Flags (2_reject_alternatives):

+ --protein_name: Input protein name (default: 'protein')
+ --working_dir: Path to save predictions (required)
+ --results_file_name: Results file name (default: 'rejection_summary')
+ --validators_results_name: Validators file name (default: 'validators_results')
+ --chat_gpt_api_key: ChatGPT API key (required)


### Examples (2_reject_alternatives):

```
python 2_reject_alternatives.py --protein_name "example_protein" \
                      --working_dir "/path/to/working/directory" \
                      --results_file_name "rejection_summary" \
                      --validators_results_name "validators_results" \
                      --chat_gpt_api_key "your_chatgpt_api_key"
```


## 3_find_optimals.py

Processes the valid descriptions and return the three optimal ones.


### Flags (3_find_optimals):

+ --protein_name: Input protein name (default: 'protein')
+ --working_dir: Path to save predictions (required)
+ --rejection_results_file_name: Rejection results file name (default: 'rejection_summary')
+ --optimal_results_file_name: Optimal descriptions file name (default: 'optimal_results')


### Examples (3_find_optimals):

```
python 3_find_optimals --protein_name "example_protein" \
                      --working_dir "/path/to/working/directory" \
                      --rejection_results_file_name "rejection_summary" \
                      --optimal_results_file_name "optimal_results"
```

# Install BetaDescribe:
We note that we use ChatGPT to reject / accept descriptions, thus, CHAT_GPT_API_KEY is needed. We recommend using GPU to reduce inference time.

```
export BETADESCRIBE_DIR="/path/to/pipeline/"
cd $BETADESCRIBE_DIR
git clone https://github.com/technion-cs-nlp/BetaDescribe-code

mkdir $BETADESCRIBE_DIR/python_venv/
conda create -y -p $BETADESCRIBE_DIR/python_venv/BetaDescribe python=3.11
export PIP_CACHE_DIR=$BETADESCRIBE_DIR/python_venv/
conda activate $BETADESCRIBE_DIR/python_venv/BetaDescribe
pip install -r $BETADESCRIBE_DIR/BetaDescribe-code/requirements.txt

```
# Run BetaDescribe pipeline:

```
export PYTHON_CODE_DIR=$BETADESCRIBE_DIR/BetaDescribe-code
export CHAT_GPT_API_KEY="<YOUR_TOKEN_ID>"

export PROTEIN_SEQUENCE="MWAFQEGVCKGNLLSGPTSMKAPDSAARESLDRASEIMTGKSYNAVHTGDLSKLPNQGESPLRIVDSDLYSERSCCWVIEKEGRVVCKSTTLTRGMTGLLNTTRCSSPSELICKVLTVESLSEKIGDTSVEELLSHGRYFKCALRDQERGKPKSRAIFLSHPFFRLLSSVVETHARSVLSKVSAVYTATASAEQRAMMAAQVVESRKHVLNGDCTKYNEAIDADTLLKVWDAIGMGSIGVMLAYMVRRKCVLIKDTLVECPGGMLMGMFNATATLALQGTTDRFLSFSDDFITSFNSPAELREIEDLLFASCHNLSLKKSYISVASLEINSCTLTRDGDLATGLGCTAGVPFRGPLVTLKQTAAMLSGAVDSGVMPFHSAERLFQIKQQECAYRYNNPTYTTRNEDFLPTCLGGKTVISFQSLLTWDCHPFWYQVHPDGPDTIDQKVLSVLASKTRRRRTRLEALSDLDPLVPHRLLVSESDVSKIRAARQAHLKSLGLEQPTNFNYAIYKAVQPTAGC"
export PROTEIN_NAME="protein1"

export ID2LABEL_PATH_CELL_LOCATION="$PYTHON_CODE_DIR/supports_files/id2label_cell_location.json"
export LABEL2ID_PATH_CELL_LOCATION="$PYTHON_CODE_DIR/supports_files/label2id_cell_location.json"
export MODEL_PATH_CELL_LOCATION="dotan1111/BetaDescribe-Validator-SubcellularLocalization"
export ID2LABEL_PATH_ORIGIN="$PYTHON_CODE_DIR/supports_files/id2label_level_0_origin.json"
export LABEL2ID_PATH_ORIGIN="$PYTHON_CODE_DIR/supports_files/label2id_level_0_origin.json"
export MODEL_PATH_ORIGIN="dotan1111/BetaDescribe-Validator-HigherLevelTaxonomy"
export ID2LABEL_PATH_ENZYMES="$PYTHON_CODE_DIR/supports_files/id2label_enzyme.json"
export LABEL2ID_PATH_ENZYMES="$PYTHON_CODE_DIR/supports_files/label2id_enzyme.json"
export MODEL_PATH_ENZYMES="dotan1111/BetaDescribe-Validator-EnzymaticActivity"

export BASE_MODEL="dotan1111/BetaDescribe-TheGenerator"
export WORKING_DIR="$PYTHON_CODE_DIR/testing/$PROTEIN_NAME"

cd $PYTHON_CODE_DIR

python "1_run_models.py" \
    --protein_sequence $PROTEIN_SEQUENCE \
    --protein_name $PROTEIN_NAME \
    --id2label_path_cell_location $ID2LABEL_PATH_CELL_LOCATION \
    --label2id_path_cell_location $LABEL2ID_PATH_CELL_LOCATION \
    --model_path_cell_location $MODEL_PATH_CELL_LOCATION \
    --id2label_path_origin $ID2LABEL_PATH_ORIGIN \
    --label2id_path_origin $LABEL2ID_PATH_ORIGIN \
    --model_path_origin $MODEL_PATH_ORIGIN \
    --id2label_path_enzymes $ID2LABEL_PATH_ENZYMES \
    --label2id_path_enzymes $LABEL2ID_PATH_ENZYMES \
    --model_path_enzymes $MODEL_PATH_ENZYMES \
    --base_model $BASE_MODEL \
    --working_dir $WORKING_DIR

python "2_reject_alternatives.py" \
    --protein_name $PROTEIN_NAME \
    --working_dir $WORKING_DIR \
    --chat_gpt_api_key $CHAT_GPT_API_KEY

python "3_find_optimals.py" \
    --protein_name $PROTEIN_NAME \
    --working_dir $WORKING_DIR
```

