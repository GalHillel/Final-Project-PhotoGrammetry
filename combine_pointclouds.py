import os
import argparse
import subprocess


def convert_mesh_to_cloud(input_mesh, output_cloud):
    meshlabserver_cli = "meshlabserver"
    command = [meshlabserver_cli, "-i", input_mesh, "-o", output_cloud, "-m", "vn"]
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error during conversion: {result.stderr}")
    else:
        print(f"Converted {input_mesh} to point cloud {output_cloud}")


def merge_pointclouds(cloud1, cloud2, output):
    meshlabserver_cli = "meshlabserver"
    merged_temp = "merged_temp.ply"

    # Create a script file for merging the clouds
    script_content = f"""
    <!DOCTYPE FilterScript>
    <FilterScript>
        <filter name="Merge Selected Layers">
            <Param name="mesh" value="{cloud1}"/>
            <Param name="mesh" value="{cloud2}"/>
        </filter>
        <filter name="Remove Duplicated Vertex"> </filter>
    </FilterScript>
    """
    script_path = "merge_clouds.mlx"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    command = [
        meshlabserver_cli,
        "-i",
        cloud1,
        cloud2,
        "-o",
        merged_temp,
        "-s",
        script_path,
    ]
    print(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error during merging: {result.stderr}")
    else:
        os.rename(merged_temp, output)
        print(f"Merged point cloud saved to {output}")

    # Clean up script and temporary files
    os.remove(script_path)
    if os.path.exists(merged_temp):
        os.remove(merged_temp)


def main():
    parser = argparse.ArgumentParser(description="Combine two point clouds.")
    parser.add_argument(
        "--pc1", required=True, help="Path to the first point cloud file."
    )
    parser.add_argument(
        "--pc2", required=True, help="Path to the second point cloud file."
    )
    parser.add_argument(
        "--output", required=True, help="Path to save the combined point cloud."
    )
    args = parser.parse_args()

    # Convert meshes to point clouds using MeshLab
    cloud1_path = args.pc1.replace(".ply", "_cloud.ply")
    cloud2_path = args.pc2.replace(".ply", "_cloud.ply")
    convert_mesh_to_cloud(args.pc1, cloud1_path)
    convert_mesh_to_cloud(args.pc2, cloud2_path)

    # Check if conversion was successful
    if not os.path.exists(cloud1_path):
        print(f"Error: {cloud1_path} does not exist!")
        return
    if not os.path.exists(cloud2_path):
        print(f"Error: {cloud2_path} does not exist!")
        return

    # Merge point clouds using MeshLab
    merge_pointclouds(cloud1_path, cloud2_path, args.output)


if __name__ == "__main__":
    main()
