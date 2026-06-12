import py7zr
import os 

def extract_data(file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    with py7zr.SevenZipFile(file_path, mode='r') as z:
        z.extractall(path=output_dir)
        
    print(f"Data extracted to {output_dir}")

if __name__ == "__main__":
    extract_data(
      "data/raw/Processed_Data_CSV.7z",
      "data/raw/refit_extracted"
    )
