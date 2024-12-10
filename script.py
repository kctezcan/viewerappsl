import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO  # Import BytesIO
import os
import tempfile  # Import tempfile for temporary file handling


file1 = "/Users/kctezcan/Downloads/toKerem/test123.nii"

img = nib.load(file1)  # Load the image from the temporary file
# Get the image data
data = img.get_fdata()

datac = data[:,:,114:456-114]

np.save("./.static/subj1_data", datac)

np.percentile()
