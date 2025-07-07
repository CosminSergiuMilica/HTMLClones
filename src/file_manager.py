import os
import shutil
from bs4 import BeautifulSoup
import cssutils
from src.MarkelTree import build_merkel_tree

VISUAL_ATTRS = {"style", "class"}
cssutils.log.setLevel('FATAL')

def extract_css_rules(soup: BeautifulSoup):
    style_content = "\n".join(tag.string for tag in soup.find_all("style") if tag.string)
    sheet = cssutils.parseString(style_content)
    rules = {}
    for rule in sheet:
        if rule.type == rule.STYLE_RULE:
            selector = rule.selectorText.strip()
            css_text = rule.style.cssText
            rules[selector] = css_text
    return rules

def apply_css_rules(soup: BeautifulSoup, rules: dict):
    for selector, css in rules.items():
        try:
            matched_elements = soup.select(selector)
            for el in matched_elements:
                existing_style = el.get("style", "")
                combined = existing_style + ";" + css if existing_style else css
                el["style"] = combined
        except Exception:
            continue

def normalize_html(soup: BeautifulSoup) -> BeautifulSoup:
    tags_to_remove = {"script", "noscript", "link", "meta"}
    for tag_name in tags_to_remove:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    css_rules = extract_css_rules(soup)
    apply_css_rules(soup, css_rules)

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