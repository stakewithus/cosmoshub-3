import argparse
import json
import os
import re

def extract_conspub(bech32_out):
    validator_conspub = re.search(r'Bech32 Validator Consensus: (.*)\n', bech32_out).group(1)
    return validator_conspub

def base64_to_bech32(pubkey):
    cmd = f"docker run --rm -it cosmos-gaiadebug:v2.0.0 pubkey {pubkey}"
    bech32_out = os.popen(cmd).read()
    return extract_conspub(bech32_out)

def main():
    parser = argparse.ArgumentParser(description='Reformat validator keys')
    parser.add_argument('pre_genesis')
    args = parser.parse_args()
    # Open the File
    with open(args.pre_genesis, 'r') as input_file:
        pre_data = json.load(input_file)
        # Final Validators
        validators = []
        # Get the validators
        pre_validators = pre_data['app_state']['staking']['validators']
        for pre_validator in pre_validators:
            pubkey_base64 = pre_validator['consensus_pubkey']['value']
            valconspub = base64_to_bech32(pubkey_base64)
            pre_validator['consensus_pubkey'] = valconspub
            validators.append(pre_validator)
        # Set it in data
        pre_data['app_state']['staking']['validators'] = validators
        with open('genesis.json', 'w') as output_file:
            json.dump(pre_data, output_file)
        

if __name__ == "__main__":
    main()
