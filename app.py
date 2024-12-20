import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO  # Import BytesIO
import os
import tempfile  # Import tempfile for temporary file handling
import matplotlib.cm as cm
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd
# https://image-coordinates.streamlit.app/

st.set_page_config(layout="wide")
st.session_state["images_loaded"] = False

def latest_inx():
    np_keys = [key for key in st.session_state.keys() if ("numpy" in key)]

    unix_times = []
    for kk in np_keys:
        if st.session_state[kk]:
            unix_times.append(st.session_state[kk]["unix_time"])
        else:
            unix_times.append(-1)

    latest_unixtime_inx = np.argmax(unix_times)

    return np_keys[latest_unixtime_inx]


labels = {
        0: "background",
        1: "subcutaneous_fat",
        3: "muscle",
        2: "intraabdominal_visceral_fat",
        4: "thoracic_visceral_fat",
        5: "intermuscular_fat"
}


st.title("Body Composition Analysis")

cont1 = st.container(border=True)

with cont1:

    input_path_img = st.file_uploader('Upload image files')
    input_path_segm = st.file_uploader('Upload segmentation files')
    input_path_ts = st.file_uploader('Upload TS files')

    if (not input_path_img) or (not input_path_segm) or (not input_path_ts):
        st.write("upload all files")



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


    
  
    cont2 = st.container(border=True)

    with cont2:

        num_slices_img = data_img.shape[2]
        slice_index = st.slider("Select slice index", 0, num_slices_img - 1, int(num_slices_img / 2))  # Default to the middle slice

        col1, col2, col3= st.columns(3)

        

        with col1:
            colormap1 = st.selectbox("Select Colormap Img", ["gray", "viridis", "plasma", "inferno", "magma", "cividis"])
            img_colored = cm.get_cmap(colormap1)(data_img[:, :, slice_index] / np.max(data_img))
            value = streamlit_image_coordinates(
                (img_colored[:,:,:3]*255).astype(np.uint8), 
                key="numpy1",
                use_column_width="always",
                click_and_drag=True)

            # st.write(st.session_state[latest_inx()])
            lat_inx = st.session_state[latest_inx()]
            if lat_inx:
                scaled_inx_x = int(np.floor(lat_inx["x1"] * data_img.shape[1] / lat_inx["width"]))
                scaled_inx_y = int(np.floor(lat_inx["y1"] * data_img.shape[0] / lat_inx["height"]))
                st.write("pixel value: " + str(data_img[scaled_inx_y, scaled_inx_x, slice_index]) )

        with col2:
            colormap2 = st.selectbox("Select Colormap Segm", ["gray", "viridis", "plasma", "inferno", "magma", "cividis"])
            segm_colored = cm.get_cmap(colormap2)(data_segm[:, :, slice_index] / np.max(data_segm))
            value = streamlit_image_coordinates(
                (segm_colored[:,:,:3]*255).astype(np.uint8), 
                key="numpy2",
                use_column_width="always",
                click_and_drag=True)
            lat_inx = st.session_state[latest_inx()]
            if lat_inx:
                scaled_inx_x = int(np.floor(lat_inx["x1"] * data_img.shape[1] / lat_inx["width"]))
                scaled_inx_y = int(np.floor(lat_inx["y1"] * data_img.shape[0] / lat_inx["height"]))
                pixel_val = int(data_segm[scaled_inx_y, scaled_inx_x, slice_index])

                st.write("pixel type: ", labels[pixel_val] )

        with col3:
            colormap3 = st.selectbox("Select Colormap TS", ["gray", "viridis", "plasma", "inferno", "magma", "cividis"])
            ts_colored = cm.get_cmap(colormap3)(data_ts[:, :, slice_index] / np.max(data_ts))
            value = streamlit_image_coordinates(
                (ts_colored[:,:,:3]*255).astype(np.uint8), 
                key="numpy3",
                use_column_width="always",
                click_and_drag=True)
            lat_inx = st.session_state[latest_inx()]
            if lat_inx:
                scaled_inx_x = int(np.floor(lat_inx["x1"] * data_img.shape[1] / lat_inx["width"]))
                scaled_inx_y = int(np.floor(lat_inx["y1"] * data_img.shape[0] / lat_inx["height"]))
                st.write("pixel value: " + str(data_ts[scaled_inx_y, scaled_inx_x, slice_index]) )

                st.session_state["images_loaded"] = True


cont3 = st.container(border=True)

with cont3:
    if st.session_state["images_loaded"] and st.session_state["images_loaded"]==True:
        voxel_size = [1.95312, 1.95312, 3.0]
        voxel_volume = np.prod(voxel_size)
        st.write("Voxel volume is " + str(np.round(voxel_volume,2)) + " mm3 or " + str(np.round(1e-3*voxel_volume,4)) + " cm3")

        total_pxl = len(data_segm[data_segm>0].flatten())
        total_vol = total_pxl * voxel_volume
        st.write("Total body volume is " + str(np.round(total_vol,2)) + " mm3 or " + str(np.round(1e-6*total_vol,2)) + " liter")

        
        subcutaneous_fat_pxl = len(data_segm[np.where(data_segm==1)])
        subcutaneous_fat_vol = subcutaneous_fat_pxl * voxel_volume

        intraabdominal_visceral_fat_pxl = len(data_segm[np.where(data_segm==2)])
        intraabdominal_visceral_fat_vol = intraabdominal_visceral_fat_pxl * voxel_volume

        muscle_pxl = len(data_segm[np.where(data_segm==3)])
        muscle_vol = muscle_pxl * voxel_volume

        thoracic_visceral_fat_vxl = len(data_segm[np.where(data_segm==4)])
        thoracic_visceral_fat_vol  = thoracic_visceral_fat_vxl * voxel_volume

        intermuscular_fat_vxl = len(data_segm[np.where(data_segm==5)])
        intermuscular_fat_vol  = intermuscular_fat_vxl * voxel_volume


        fat_meas_df = pd.DataFrame(
            {
                "total_vol": [np.round(1e-6*total_vol,2)], 
                "subcutaneous_fat_vol": [np.round(1e-6*subcutaneous_fat_vol,2)],
                "intraabdominal_visceral_fat_vol": [np.round(1e-6*intraabdominal_visceral_fat_vol,2)],
                "muscle_vol": [np.round(1e-6*muscle_vol,2)],
                "thoracic_visceral_fat_vol": [np.round(1e-6*thoracic_visceral_fat_vol,2)],
                "intermuscular_fat_vol": [np.round(1e-6*intermuscular_fat_vol,2)],
            }
        ).T

        st.write(fat_meas_df)
        


    
#     Visceral Adipose Tissue (VAT)
# Abdominal Subcutaneous Adipose Tissue (ASAT)
# Fat Free Muscle Volume (FFMV)
# Muscle Fat Infiltration (MFI)
# Individual Muscle Measurements
# Liver PDFF
# Muscle Fat Fraction (MFF)

        # 0: "background",
        # 1: "subcutaneous_fat",
        # 3: "muscle",
        # 2: "intraabdominal_visceral_fat",
        # 4: "thoracic_visceral_fat",
        # 5: "intermuscular_fat"