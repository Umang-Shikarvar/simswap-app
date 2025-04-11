import os
import streamlit as st
from PIL import Image

def swap_faces(source_path, target_path):
    output_dir = "output"

    os.system(
        f"python3 test_one_image.py "
        f"--name people "
        f"--Arc_path arcface_model/arcface_checkpoint.tar "
        f"--pic_a_path {source_path} "
        f"--pic_b_path {target_path} "
        f"--output_path {output_dir}/ "
        f"--crop_size 224 "
    )

def get_images(folder, max_images=4):
    exts = (".jpg", ".jpeg", ".png")
    return [f for f in os.listdir(folder) if f.lower().endswith(exts)][:max_images]

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🌀 SimSwap Face Swapper")

image_dir = "crop_224"
available_images = get_images(image_dir)
IMAGE_DISPLAY_SIZE = 180

if len(available_images) < 2:
    st.warning("At least 2 images are required.")
    st.stop()

st.markdown("### Step 1: Select **Source Face (A)**")
cols = st.columns(4)
for i, img_file in enumerate(available_images):
    with cols[i % 4]:
        img = Image.open(os.path.join(image_dir, img_file))
        st.image(img, width=IMAGE_DISPLAY_SIZE)
        if st.button("Select A", key=f"src_{img_file}"):
            st.session_state["source_img"] = img_file

st.divider()

st.markdown("### Step 2: Select **Target Face (B)**")
cols = st.columns(4)
for i, img_file in enumerate(available_images):
    with cols[i % 4]:
        img = Image.open(os.path.join(image_dir, img_file))
        st.image(img, width=IMAGE_DISPLAY_SIZE)
        if st.button("Select B", key=f"tgt_{img_file}"):
            st.session_state["target_img"] = img_file

source_img = st.session_state.get("source_img", None)
target_img = st.session_state.get("target_img", None)

if source_img and target_img:
    if source_img == target_img:
        st.warning("Please select two different images.")
    else:
        if st.button("🔁 Swap Faces"):
            with st.spinner("Running SimSwap..."):
                src_path = os.path.join(image_dir, source_img)
                tgt_path = os.path.join(image_dir, target_img)
                swap_faces(src_path, tgt_path)

                result_path = "output/result.jpg"
                if os.path.exists(result_path):
                    st.success("✅ Face swap completed!")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("**Source (A)**")
                        st.image(src_path, width=IMAGE_DISPLAY_SIZE)
                    with col2:
                        st.markdown("**Target (B)**")
                        st.image(tgt_path, width=IMAGE_DISPLAY_SIZE)
                    with col3:
                        st.markdown("**Result**")
                        st.image(result_path, width=IMAGE_DISPLAY_SIZE)
                else:
                    st.error("❌ Face swap failed. Please check logs.")