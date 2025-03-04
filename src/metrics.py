from datasets import load_dataset
import re

def true_positives(anonymised_text, privacy_mask):
    tp = 0
    
    for pii in privacy_mask:
        if pii['value'] not in anonymised_text:
            tp += 1
            
    return tp

dataset = load_dataset("ai4privacy/pii-masking-200k", data_files="english_pii_43k.jsonl")

anonymised_texts = ["A student's assessment was found on device bearing [DEVICE_ID], The document falls under the various topics discussed in our [COURSE] curriculum. Can you please collect it?",
                    "Dear [NAME], as per our records, your LICENSE is still registered in our records for access to the EDUCATIONAL TOOLS. Please feedback on its OPERABILITY.",
                    "Recommendations about vegetarian diet for 72 OLD PERSON with 158 CENTIMETERS height.",
                    "Emergency supplies in [CREDIT_CARD_NUMBER] need a refill. Use [CREDIT_CARD_NUMBER] to pay for them.",
                    "The [AGE]-old [CHILD] at [LOCATION], has showcased an unusual ability to remember and recite [PASSWORD], with [PASSWORD] being most repeated.",
                    "Your recent hospital data recorded on [DATE] regarding chronic disease management has been encrypted with IPv6 [IPv6_ADDRESS] for enhanced privacy.",
                    "Dear [GENDER], Let's clear this misunderstanding. We never send an email asking for your [PASSWORD]. If you get one, it's not from us. Please secure your account. If you already gave out your [PASSWORD], change it immediately.",
                    "The wellness portal is accessible at [GEOLOCATION]. With numerous wellness tracks suitable for everyone in the family, enrol now! Contact us at [BROWSER] for further details.",
                    "Carleton, the new interactive educational tools are set to arrive at [GEOLOCATION]. Your password for accessing online content: [PASSWORD].",
                    "1. Customer query received at 10:18 PM from [GROUP] of [LOCATION] based firm. The customer's email is [EMAIL], where EMAIL = [EMAIL CATEGORY]. Use our account number [ACCOUNT NUMBER] for all financial exchanges. For personal discussions, ensure privacy with PIN - [PIN] and EYECOLOR - [EYECOLOR]."]

for data_point in range(10):
    print("Raw text: ", dataset["train"][data_point]["source_text"], "\n")
    print("Ground truth: ", dataset["train"][data_point]["target_text"], "\n")
    print("Anonymised text: ", anonymised_texts[data_point], "\n")
    
    tp = true_positives(anonymised_texts[data_point], dataset["train"][data_point]["privacy_mask"])
    print("True Positives (TP): ", tp, "\n")
    print("\n")
