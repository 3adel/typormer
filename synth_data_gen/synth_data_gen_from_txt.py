import json
import ollama

def show_common_typos_ollama(word):
    # Call to the Ollama API using the llama3 model
    response = ollama.generate(
        model='llama3', 
        prompt=f"List only ten common non-word spelling errors for the word '{word}'. These errors should be common typos that an English native speaker would make regularly. The errrors shoulo not form real English words. The typos should be more than 1 characters long each. Only provide a comma-separated list of these errors. Ensure the list does never include the word '{word}' or synonyms of the word '{word}'. Ensure that the answer never include any additinal text. The list of errors should be ranked from most common to the least commmon",)
    return response

def save_typos_to_jsonl(source_file_path, output_file_path):
    # Open the source file and output file
    with open(source_file_path, "r") as file, open(output_file_path, "w") as outfile:

        words_count = 0

        # Iterate over each line in the source file
        for line in file:
            word = line.strip()
            

            # Get the response from Ollama
            typo_response = show_common_typos_ollama(word)
            

            # Assuming the typo_response returns JSON with a specific structure. Adjust according to actual API response.
            typos_list = typo_response['response']
            print(words_count,word,"->",typos_list)

            # Create a JSON object for each line and write to the output file
            json_line = json.dumps({
                "correct_word": word,
                "misspellings": typos_list
            })
            outfile.write(json_line + "\n")  # Write the JSON line followed by a newline character

            # Decide how many words to process
            words_count += 1
            if words_count == 10000:
                break

# Define file paths
source_file_path = "/Users/adel/adel/dev/training_data/auto-correct/gwords/raw/raw_words.txt"
output_file_path = "/Users/adel/adel/dev/training_data/auto-correct/gwords/jsonified/frequency-alpha-alldicts.jsonl"

# Call the function to process and save typos
save_typos_to_jsonl(source_file_path, output_file_path)
