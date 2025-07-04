import os
import asyncio
from pathlib import Path
from PIL import Image
import imagehash
import time
from playwright.async_api import async_playwright

from src.file_manager import move_files_to_clusters

html_dir = "./data/tier4"
ss_dir = "./data/ss"
cluster_dir= "./data/clustering"
threshold = 10

async def take_screenshot(context, html_file):
    html_path = os.path.join(html_dir, html_file)
    ss_path = os.path.join(ss_dir, html_file.replace(".html", ".png"))
    file_url = f"file://{Path(html_path).resolve()}"

    try:
        page = await context.new_page()
        await page.goto(file_url, timeout=60000, wait_until='domcontentloaded')
        await page.screenshot(path=ss_path, full_page=True)
        await page.close()
        print(f"Screenshot: {ss_path}")
    except Exception as e:
        print(f"Error {html_file}: {e}")

async def generate_screenshots_parallel(html_files):
    if not os.path.exists(ss_dir):
        os.makedirs(ss_dir)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})

        tasks = [take_screenshot(context, html_file) for html_file in html_files]
        await asyncio.gather(*tasks)

        await browser.close()

def group_by_similarity(html_files, threshold=10):
    hashes = {}
    for html_file in html_files:
        img_path = os.path.join(ss_dir, html_file.replace(".html", ".png"))
        if not os.path.exists(img_path):
            continue
        img = Image.open(img_path)
        hashes[html_file] = imagehash.phash(img)

    visited = set()
    groups = []

    for f1 in html_files:
        if f1 not in hashes or f1 in visited:
            continue
        group = [f1]
        visited.add(f1)
        for f2 in html_files:
            if f2 not in hashes or f2 in visited or f1 == f2:
                continue
            if hashes[f1] - hashes[f2] <= threshold:
                group.append(f2)
                visited.add(f2)
        groups.append(group)

    return groups

async def main():
    start = time.time()

    html_files = [f for f in os.listdir(html_dir) if f.endswith(".html")]
    print(f"No. {len(html_files)} HTML files.")

    await generate_screenshots_parallel(html_files)

    groups = group_by_similarity(html_files, threshold)

    print("\nGroups:")
    for i, group in enumerate(groups, 1):
        print(f"Group {i}: {group}")

    print(f"\nTime: {time.time() - start:.2f}s.")
    move_files_to_clusters(groups, html_dir, cluster_dir)

if __name__ == "__main__":
    asyncio.run(main())
