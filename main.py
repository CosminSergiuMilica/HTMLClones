from src.clustering import group_similar_htmls
from src.file_manager import move_files_to_clusters, load_html_files


def main():
    source_folder = './data/tier1'
    output_folder = './data/clusters_tier1'

    print("Loading HTML files...")
    html_trees = load_html_files(source_folder)

    print("Clustering files...")
    groups = group_similar_htmls(html_trees, threshold=80)

    for i, group in enumerate(groups, start=1):
        print(f"Group {i}: {group}")

    print("Moving files to clusters...")
    move_files_to_clusters(groups, source_folder, output_folder)

    print("Done!")

if __name__ == "__main__":
    main()
