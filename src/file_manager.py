import os
import shutil

def move_files_to_clusters(groups, source_folder, output_base_folder):
    os.makedirs(output_base_folder, exist_ok=True)

    for i, group in enumerate(groups, start=1):
        cluster_folder = os.path.join(output_base_folder, f"group_{i}")
        os.makedirs(cluster_folder, exist_ok=True)

        for filename in group:
            src_path = os.path.join(source_folder, filename)
            dst_path = os.path.join(cluster_folder, filename)
            shutil.copy2(src_path, dst_path)