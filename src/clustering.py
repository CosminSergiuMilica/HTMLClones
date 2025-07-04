import ssdeep
def compare_merkel_trees(nodeA, nodeB, path="root"):
    diffs = []
    diff_count = 0

    if nodeA.hash == nodeB.hash:
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

        if ssdeep.compare(childA.hash, childB.hash) == 85:
            continue

        if childA.children or childB.children:
            sub_diffs, sub_count = compare_merkel_trees(childA, childB, new_path)
            diffs.extend(sub_diffs)
            diff_count += sub_count
        else:
            diffs.append((new_path, "leaf hash mismatch"))
            diff_count += 1
    return diffs, diff_count

def group_similar_htmls(html_trees, max_allowed_diffs=3):
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
            diffs, count = compare_merkel_trees(t1, t2)
            if count <= max_allowed_diffs:
                group.append(f2)
                visited.add(f2)
        groups.append(group)
    return groups
