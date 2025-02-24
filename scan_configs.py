# Notes for sometime in the future when ill need it again :joy:
# This script searches DayZ's config.bin files for itemSize definitions
# BI's configs are a nightmare to parse - if this script doesn't work, use 
# DayZ Tools' CfgConvert.exe to convert all their stupid bin files to readable text:
# D:\SteamLibrary\steamapps\common\DayZ Tools\Bin\CfgConvert\CfgConvert.exe
# Because god forbid they should just use normal files that actual humans can read...

import os
import re

def find_all_config_bins(start_path):
    # God, another script to parse BI's ridiculous config structure...
    config_bins = []
    
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.lower() == "config.bin":
                full_path = os.path.join(root, file)
                config_bins.append(full_path)
    
    print(f"Found {len(config_bins)} config.bin files")
    return config_bins

def search_item_sizes(config_bins):
    # Here we go again... digging through hundreds of config files for simple data that 
    # should just be in one god damn FILE
    items_found = []
    processed_count = 0
    
    # Let's hope this regex works on BI's inconsistent formatting...
    item_size_pattern = re.compile(r'itemSize\[\]\s*=\s*{([^}]+)}')
    class_pattern = re.compile(r'class\s+(\w+)')
    
    for bin_path in config_bins:
        processed_count += 1
        if processed_count % 10 == 0:
            print(f"Processed {processed_count}/{len(config_bins)} files... (kill me now)")
        
        try:
            # Try to read this mess, encoding is probably wrong but whatever
            with open(bin_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            for match in item_size_pattern.finditer(content):
                item_size = match.group(1).strip()
                
                # Look backward to find the class name... because BI can't just put this stuff together
                content_before = content[:match.start()]
                class_matches = list(class_pattern.finditer(content_before))
                
                if class_matches:
                    class_name = class_matches[-1].group(1)
                else:
                    # FFS, no class name? Typical.
                    class_name = "Unknown"
                
                try:
                    # Why can't they just use a simple "width, height" format consistently?
                    size_values = [int(v.strip()) for v in item_size.split(',')]
                    if len(size_values) == 2:
                        slot_size_total = size_values[0] * size_values[1]
                        slot_size_formatted = f"{size_values[0]}x{size_values[1]} ({slot_size_total} Slots)"
                    else:
                        # Of course there are exceptions to the format...
                        slot_size_formatted = "Invalid format"
                except:
                    slot_size_formatted = "Error calculating"
                
                items_found.append({
                    'class_name': class_name,
                    'item_size': item_size,
                    'slot_size_total': slot_size_formatted,
                    'file_path': bin_path
                })
                
                print(f"Found: {class_name} with itemSize[] = {{{item_size}}} - {slot_size_formatted} in {bin_path}")
                
        except Exception as e:
            # Oh look, another broken file I bet
            print(f"Error processing {bin_path}: {e}")
    
    return items_found

def main():
    # Change this if your P: drive is mapped differently, because OF COURSE
    # everyone has to have a P: drive for this to work...
    dz_path = r"P:\DZ"
    
    print(f"Searching for itemSize definitions in all config.bin files in {dz_path}...")
    
    config_bins = find_all_config_bins(dz_path)
    
    if not config_bins:
        print("No config.bin files found. Check the path.")
        return
    
    items = search_item_sizes(config_bins)
    
    # Sort by slot size - doing math that should have been done in the config files...
    items.sort(key=lambda x: int(x['slot_size_total'].split('(')[1].split(' ')[0]) 
               if '(' in x['slot_size_total'] else 0, reverse=True)
    
    # Write everything out because who knows when I'll need to do this again
    with open('dayz_all_item_sizes.txt', 'w', encoding='utf-8') as f:
        f.write("DayZ Items with itemSize definitions:\n")
        f.write("==================================================\n")
        f.write(f"Total items found: {len(items)}\n\n")
        
        for item in items:
            f.write(f"Class: {item['class_name']}\n")
            f.write(f"Size: {item['item_size']}\n")
            f.write(f"SlotSizeTotal: {item['slot_size_total']}\n")
            f.write(f"Path: {item['file_path']}\n")
            f.write("--------------------------------------------------\n")
    
    # CSV for importing to Excel since that's what normal people use
    with open('dayz_all_item_sizes.csv', 'w', encoding='utf-8') as f:
        f.write("Class,Size,SlotSizeTotal,Path\n")
        for item in items:
            size_escaped = f"\"{item['item_size']}\"" if ',' in item['item_size'] else item['item_size']
            slot_total_escaped = f"\"{item['slot_size_total']}\""
            path_escaped = f"\"{item['file_path']}\""
            f.write(f"{item['class_name']},{size_escaped},{slot_total_escaped},{path_escaped}\n")
    
    # Might as well group them too, since I'm spending all day on this anyway
    with open('dayz_item_sizes_by_slot.txt', 'w', encoding='utf-8') as f:
        f.write("DayZ Items grouped by total slot size (largest to smallest):\n")
        f.write("==================================================\n")
        
        current_slot_size = None
        for item in items:
            slot_size = item['slot_size_total'].split('(')[1].split(' ')[0] if '(' in item['slot_size_total'] else "Unknown"
            
            if slot_size != current_slot_size:
                current_slot_size = slot_size
                f.write(f"\n{'-'*50}\n")
                f.write(f"Items using {current_slot_size} slots:\n")
                f.write(f"{'-'*50}\n\n")
            
            f.write(f"{item['class_name']} - {item['slot_size_total']}\n")
    
    print(f"\nFinally! Found {len(items)} items with itemSize definitions")
    print(f"Results saved to:")
    print(f"- dayz_all_item_sizes.txt - Complete list of all items")
    print(f"- dayz_all_item_sizes.csv - CSV format for importing to spreadsheets")
    print(f"- dayz_item_sizes_by_slot.txt - Items grouped by total slot size")
    print(f"- fk you BI, fk you..")

if __name__ == "__main__":
    main()