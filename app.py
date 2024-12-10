# import streamlit as st
# import nibabel as nib
# import numpy as np
# import matplotlib.pyplot as plt
# from io import BytesIO  # Import BytesIO
# import os
# import tempfile  # Import tempfile for temporary file handling


# st.title("NIFTI Image Middle Slice Viewer")

# data = np.load(".static/subj1_data.npy")

# data = np.transpose(data, [0, 2, 1])

# print(data.shape)

# slice_index = st.slider("Select slice index", 0, data.shape[2] - 1, int(data.shape[2]/2) )  # Default to slice 220
# st.image(data[:, :, slice_index] / np.max(data[:, :, slice_index]), caption=f'Slice {slice_index}')
    
# print("asdf")



import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO  # Import BytesIO
import os
import tempfile  # Import tempfile for temporary file handling


st.title("NIFTI Image Middle Slice Viewer")

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

    with col1:
        st.image(data_img[:,:,slice_index]/np.max(data_img[:,:,:]))

    with col2:
        st.image(data_segm[:,:,slice_index]/np.max(data_segm[:,:,:]))

    with col3:
        st.image(data_ts[:,:,slice_index]/np.max(data_ts[:,:,:]))

st.write("end of app")
