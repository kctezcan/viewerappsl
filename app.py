import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO  # Import BytesIO
import os
import tempfile  # Import tempfile for temporary file handling
import matplotlib.cm as cm


st.title("Body Composition Analysis")

cont1 = st.container()

with cont1:

    input_path_img = st.file_uploader('Upload image files')
    input_path_segm = st.file_uploader('Upload segmentation files')
    input_path_ts = st.file_uploader('Upload TS files')

    if (not input_path_img) or (not input_path_segm) or (not input_path_ts):
        st.write("upload all files")

col1, col2, col3 = st.columns(3)

if input_path_img and input_path_segm and input_path_ts:
    temp_data_directory = './data/temp_folder/'
    os.makedirs(temp_data_directory, exist_ok=True)

    with open(temp_data_directory + "niftifile_img.nii", 'wb') as out:
            out.write(input_path_img.getbuffer())

    with open(temp_data_directory + "niftifile_segm.nii", 'wb') as out:
            out.write(input_path_segm.getbuffer())

    with open(temp_data_directory + "niftifile_ts.nii", 'wb') as out:
            out.write(input_path_ts.getbuffer())


    img_img = nib.load(temp_data_directory + "niftifile_img.nii")
    img_segm = nib.load(temp_data_directory + "niftifile_segm.nii")
    img_ts = nib.load(temp_data_directory + "niftifile_ts.nii")

    # Get the image data as a NumPy array
    data_img = img_img.get_fdata()
    data_segm = img_segm.get_fdata()
    data_ts = img_ts.get_fdata()

    data_img = np.transpose(data_img, [0, 2,1 ])
    data_segm = np.transpose(data_segm, [0, 2,1 ])
    data_ts = np.transpose(data_ts, [0, 2,1 ])

    data_img = np.rot90( data_img, 1)
    data_segm = np.rot90( data_segm, 1)
    data_ts = np.rot90( data_ts, 1)


    num_slices_img = data_img.shape[2]
    slice_index = st.slider("Select slice index", 0, num_slices_img - 1, int(num_slices_img / 2))  # Default to the middle slice

  
    cont2 = st.container()

    with cont2:
        with col1:
            colormap1 = st.selectbox("Select Colormap Img", ["gray", "viridis", "plasma", "inferno", "magma", "cividis"])
            img_colored = cm.get_cmap(colormap1)(data_img[:, :, slice_index] / np.max(data_img))
            st.image(img_colored)

        with col2:
            colormap2 = st.selectbox("Select Colormap Segm", ["gray", "viridis", "plasma", "inferno", "magma", "cividis"])
            segm_colored = cm.get_cmap(colormap2)(data_segm[:, :, slice_index] / np.max(data_segm))
            st.image(segm_colored)

        with col3:
            colormap3 = st.selectbox("Select Colormap TS", ["gray", "viridis", "plasma", "inferno", "magma", "cividis"])
            ts_colored = cm.get_cmap(colormap3)(data_ts[:, :, slice_index] / np.max(data_ts))
            st.image(ts_colored)

st.write("end of app")
