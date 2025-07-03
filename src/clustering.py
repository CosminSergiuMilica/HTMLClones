import ssdeep

def group_similar_htmls(html_trees, threshold=75):
    files = list(html_trees.keys())
    visited = set()
    groups = []

    for i, file1 in enumerate(files):
        if file1 in visited:
            continue
        group = [file1]
        visited.add(file1)
        hash1 = html_trees[file1].hash

        for j in range(i + 1, len(files)):
            file2 = files[j]
            if file2 in visited:
                continue
            hash2 = html_trees[file2].hash
            similarity = ssdeep.compare(hash1, hash2)

            if similarity >= threshold:
                group.append(file2)
                visited.add(file2)

        groups.append(group)

    return groups