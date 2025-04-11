import os

def swap_faces(source_path, target_path, gpu_id=0):
    simswap_dir = "/home/umang.shikarvar/DeepFake/SimSwap"
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    # Change directory to SimSwap
    os.chdir(simswap_dir)

    # Run the SimSwap command with GPU enabled
    os.system(
        f"python test_one_image.py "
        f"--name people "
        f"--Arc_path arcface_model/arcface_checkpoint.tar "
        f"--pic_a_path {source_path} "
        f"--pic_b_path {target_path} "
        f"--output_path {output_dir}/ "
        f"--crop_size 224 "
        f"--gpu_ids {gpu_id}"
    )

# Example usage (use GPU 0)
swap_faces("crop_224/trump.jpg", "crop_224/zjl.jpg", gpu_id=0)