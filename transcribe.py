import os
import whisper

# Directory configuration
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"

def setup_directories():
    """Ensure the input and output directories exist."""
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    setup_directories()
    
    # Load the Whisper model. You can choose different sizes:
    # 'tiny', 'base', 'small', 'medium', 'large'
    # 'base' is a good balance between speed and accuracy for starting out.
    print("Loading Whisper model (this might take a moment the first time if downloading)...")
    model = whisper.load_model("base")
    
    # Process all files in the input directory
    files_to_process = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f)) and f != ".gitkeep"]
    
    if not files_to_process:
        print(f"No files found in {INPUT_DIR}. Please add some video or audio files there and try again.")
        return

    for filename in files_to_process:
        input_file_path = os.path.join(INPUT_DIR, filename)
        
        # Generate the output txt path (changing the extension to .txt)
        base_name = os.path.splitext(filename)[0]
        output_file_path = os.path.join(OUTPUT_DIR, f"{base_name}.txt")
        
        print(f"\nTranscribing: {filename}...")
        
        try:
            # Transcribe the file
            result = model.transcribe(input_file_path)
            
            # Write transcription to output file
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(result["text"].strip())
            
            print(f"Successfully transcribed to {output_file_path}")
            
        except Exception as e:
            print(f"Error transcribing {filename}: {e}")

if __name__ == "__main__":
    main()
