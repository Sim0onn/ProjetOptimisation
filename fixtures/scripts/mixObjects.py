import csv
import random
import glob
import os

def mixObjects(directory_name: str):
    
    if not os.path.isdir(directory_name):
        print(f"ERROR: The directory '{directory_name}' was not found.")
        return

    search_pattern = os.path.join(directory_name, '*.csv')
    files_to_shuffle = glob.glob(search_pattern)
    
    if not files_to_shuffle:
        print(f"No CSV files were found in the directory '{directory_name}'.")
        return

    #print(f"--- Starting shuffle process for {len(files_to_shuffle)} file(s) in '{directory_name}' ---\n")

    for file_path in files_to_shuffle:
        try:
            #print(f"Processing file: '{file_path}'...")
            
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                
                header = next(reader)
                
                data_rows = list(reader)

            random.shuffle(data_rows)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                writer.writerow(header)
                
                writer.writerows(data_rows)
            
            #print(f"-> File '{file_path}' shuffled successfully.")

        except StopIteration:
            print(f"-> File '{file_path}' is empty or has only a header. Skipped.")
        except Exception as e:
            print(f"ERROR while processing '{file_path}': {e}")
            
    #print("\n--- Shuffle operation complete. ---")

