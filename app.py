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

input_path = st.file_uploader('Upload files')


if input_path:
    temp_data_directory = './data/temp_folder/'
    os.makedirs(temp_data_directory, exist_ok=True)

    with open(temp_data_directory + "niftifile.nii", 'wb') as out:
            out.write(input_path.getbuffer())


    img = nib.load(temp_data_directory + "niftifile.nii")

    # Get the image data as a NumPy array
    data = img.get_fdata()

    st.image(data[:,:,200]/np.max(data[:,:,200]))

st.write("end of app")
