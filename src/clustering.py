import ssdeep
from difflib import SequenceMatcher

def fingerprint_similarity(fp1: str, fp2: str) -> float:
    return SequenceMatcher(None, fp1, fp2).ratio() * 100

def compare_merkel_trees(nodeA, nodeB, path="root", threshold=80):
    diffs = []
    diff_count = 0

    similarity = ssdeep.compare(nodeA.hash, nodeB.hash)
    if similarity >= threshold:
        return diffs, diff_count

    fp_sim = fingerprint_similarity(nodeA.fingerprint, nodeB.fingerprint)
    if fp_sim >= threshold + 10:
        return diffs, diff_count

    max_len = max(len(nodeA.children), len(nodeB.children))
    for i in range(max_len):
        childA = nodeA.children[i] if i < len(nodeA.children) else None
        childB = nodeB.children[i] if i < len(nodeB.children) else None
        new_path = f"{path}/{nodeA.tag}[{i}]"

        if childA is None or childB is None:
            diffs.append((new_path, "missing node"))
            diff_count += 1
            continue

        child_sim = ssdeep.compare(childA.hash, childB.hash)
        if child_sim >= threshold:
            continue

        child_fp_sim = fingerprint_similarity(childA.fingerprint, childB.fingerprint)
        if child_fp_sim >= threshold + 10:
            continue

        if childA.children or childB.children:
            sub_diffs, sub_count = compare_merkel_trees(childA, childB, new_path, threshold)
            diffs.extend(sub_diffs)
            diff_count += sub_count
        else:
            diffs.append((
                new_path,
                f"leaf mismatch (hash_sim={child_sim}, fp_sim={child_fp_sim:.2f})"
            ))
            diff_count += 1

    return diffs, diff_count


def group_similar_htmls(html_trees, max_allowed_diffs=3, threshold=80):
    files = list(html_trees.keys())
    visited = set()
    groups = []

    for i, f1 in enumerate(files):
        if f1 in visited:
            continue
        group = [f1]
        visited.add(f1)
        t1 = html_trees[f1]

        for f2 in files[i+1:]:
            if f2 in visited:
                continue
            t2 = html_trees[f2]
            diffs, count = compare_merkel_trees(t1, t2, threshold=threshold)
            if count <= max_allowed_diffs:
                group.append(f2)
                visited.add(f2)
        groups.append(group)
    return groups
