import kagglehub
import json

# Download latest version
path = kagglehub.dataset_download("verracodeguacas/ai4privacy-pii")

# absolute path
dataset_65k_english = path + "\pii-masking-65k\english_balanced_10k.jsonl"

'''
dataset format of one text:
{
"masked_text" : string,
"unmasked_text": string,
"token_entity_labels": [label1, label2...],
"tokenised_unmasked_text": [unmasked_text1, unmasked_text2...]
}
'''

with open(dataset_65k_english, "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]  # each line is a json object

# store those four data types into four lists
'''
note that masked_text and unmasked_text are strings lists
while token_entity_labels and tokenised_unmasked_text are two-dimensional lists, which means that
to extract the value you need token_entity_labels[i][j]
'''
masked_text = [entry["masked_text"] for entry in data]
unmasked_text = [entry["unmasked_text"] for entry in data]
token_entity_labels = [entry["token_entity_labels"] for entry in data]
tokenised_unmasked_text = [entry["tokenised_unmasked_text"] for entry in data]


print(masked_text[0])
print(unmasked_text[0])
print(token_entity_labels[0])
print(tokenised_unmasked_text[0])


