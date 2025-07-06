import os
import shutil
from bs4 import BeautifulSoup
from src.MarkelTree import build_merkel_tree

VISUAL_ATTRS = {"style", "class"}

def normalize_html(soup: BeautifulSoup) -> BeautifulSoup:
    style_content = []
    for tag in soup.find_all("style"):
        if tag.string:
            style_content.append(tag.string)
        tag.decompose()

    if style_content:
        full_style = "\n".join(style_content)
        style_tag = soup.new_tag("style")
        style_tag.string = full_style

        if soup.head:
            soup.head.insert(0, style_tag)
        else:
            head_tag = soup.new_tag("head")
            head_tag.insert(0, style_tag)
            soup.html.insert(0, head_tag)

    tags_to_remove = {"script", "noscript", "link", "meta", "iframe", "svg"}
    for tag_name in tags_to_remove:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    for tag in soup.find_all(True):
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in VISUAL_ATTRS}

        if tag.string and tag.string.strip():
            tag.string = " ".join(tag.string.strip().split())
    return soup


def load_html_files(folder_path):
    html_trees = {}
    for filename in os.listdir(folder_path):
        if not filename.endswith('.html'):
            continue
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            bs = BeautifulSoup(f, "html.parser")
            normalized_soup = normalize_html(bs)
            html_root = normalized_soup.find('html')
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