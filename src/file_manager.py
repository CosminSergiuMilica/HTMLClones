import os
import shutil
from bs4 import BeautifulSoup
from src.MarkelTree import build_merkel_tree


def load_html_files(folder_path):
    html_trees = {}
    for filename in os.listdir(folder_path):
        if not filename.endswith('.html'):
            continue
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as f:
            bs = BeautifulSoup(f, "html.parser")
            html_root = bs.find('html')
            if html_root:
                markel_root = build_merkel_tree(html_root)
                html_trees[filename] = markel_root
    return html_trees

def move_files_to_clusters(groups, source_folder, output_base_folder):
    os.makedirs(output_base_folder, exist_ok=True)

    for i, group in enumerate(groups, start=1):
        cluster_folder = os.path.join(output_base_folder, f"group_{i}")
        os.makedirs(cluster_folder, exist_ok=True)

        for filename in group:
            src_path = os.path.join(source_folder, filename)
            dst_path = os.path.join(cluster_folder, filename)
            shutil.copy2(src_path, dst_path)