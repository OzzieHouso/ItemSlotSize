# If you're having trouble reading DayZ's binary config files, this script will convert
# all of them to readable text using CfgConvert.exe from DayZ Tools.
# Just run this before running the main itemSize finder script.
# Because clearly making configs readable by default was too damn hard for BI...

import os
import subprocess
import time

def find_all_config_bins(start_path):
    # Find all the binary config files that need converting
    config_bins = []
    
    print(f"Searching for config.bin files in {start_path}...")
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.lower() == "config.bin":
                full_path = os.path.join(root, file)
                config_bins.append(full_path)
    
    print(f"Found {len(config_bins)} config.bin files to convert")
    return config_bins

def convert_configs(config_bins, output_dir, cfg_convert_path):
    # Convert all the stupid bin files to something a human can actually read
    converted_count = 0
    failed_count = 0
    
    # Make the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    start_time = time.time()
    
    for bin_path in config_bins:
        # Create a mirrored file structure in the output directory
        rel_path = os.path.relpath(bin_path, "P:\\")  # Assumes P: drive mapping.. it should already be P but ya know?
        output_path = os.path.join(output_dir, rel_path + ".txt")
        
        # Make sure the directory exists
        output_dir_path = os.path.dirname(output_path)
        if not os.path.exists(output_dir_path):
            os.makedirs(output_dir_path)
        
        print(f"Converting: {bin_path}")
        
        try:
            # Run CfgConvert to do the conversion
            result = subprocess.run([
                cfg_convert_path,
                "-txt",
                bin_path,
                output_path
            ], check=True, capture_output=True, text=True)
            
            converted_count += 1
            
            if converted_count % 10 == 0:
                elapsed = time.time() - start_time
                print(f"Converted {converted_count}/{len(config_bins)} files... ({elapsed:.2f} seconds elapsed)")
                
        except subprocess.CalledProcessError as e:
            failed_count += 1
            print(f"Failed to convert {bin_path}: {e.stderr}")
        except Exception as e:
            failed_count += 1
            print(f"Error: {e}")
    
    total_time = time.time() - start_time
    
    print(f"\nConversion completed in {total_time:.2f} seconds")
    print(f"Successfully converted: {converted_count} files")
    print(f"Failed to convert: {failed_count} files")
    print(f"Converted files are in: {output_dir}")

def main():
    # Paths - change these if needed
    dz_path = r"P:\DZ"
    output_dir = r"C:\DayzConvertedConfigs"
    cfg_convert_path = r"D:\SteamLibrary\steamapps\common\DayZ Tools\Bin\CfgConvert\CfgConvert.exe"
    
    # Check if CfgConvert exists
    if not os.path.exists(cfg_convert_path):
        print(f"ERROR: CfgConvert.exe not found at {cfg_convert_path}")
        print("Please install DayZ Tools through Steam or update the path to CfgConvert.exe")
        return
    
    # Find all config.bin files
    config_bins = find_all_config_bins(dz_path)
    
    if not config_bins:
        print("No config.bin files found. Make sure your P: drive is mapped correctly.")
        return
    
    # Convert all configs
    convert_configs(config_bins, output_dir, cfg_convert_path)
    
    print("\nDONE! Now you can run the itemSize finder script on the converted files.")
    print(f"Just update the script to look in {output_dir} instead of the P: drive.")

if __name__ == "__main__":
    main()