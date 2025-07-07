import json

from src.clustering import group_similar_htmls
from src.file_manager import move_files_to_clusters, load_html_files

def process_tier(tier_name: str):
    print(f"\nProcessing {tier_name}...")
    source_folder = f'./data/{tier_name}'
    output_folder = f'./data/clusters_{tier_name}'
    json_output_path = f'./data/{tier_name}_clusters.json'

    html_trees = load_html_files(source_folder)

    print("Clustering files...")
    groups = group_similar_htmls(html_trees)

    for i, group in enumerate(groups, start=1):
        print(f"Group {i}: {group}")

    print("Moving files to clusters...")
    move_files_to_clusters(groups, source_folder, output_folder)

    print(f"Saving cluster info to {json_output_path}...")
    with open(json_output_path, 'w', encoding='utf-8') as f:
        json.dump(groups, f, indent=2)

    print(f"Finished {tier_name}!")

def main():
    for tier in ['tier1', 'tier2', 'tier3', 'tier4']:
        process_tier(tier)

if __name__ == "__main__":
    main()