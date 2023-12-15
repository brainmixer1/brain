import numpy as np
import numpy.ma as ma 
import pickle
import pandas as pd
import os 
import nibabel as nib
import os 
import matplotlib.pyplot as plt

#%%

def get_mask(subject, mask_name='all'): 

    if mask_name=='all':

        mask = np.zeros(nib.load('../Data/denoised_reformatted/ROIs_resampled_space-T1w/sub-0{}/varea/sub-0{}_resampled_varea_resampled.nii.gz'.format(subject, subject)).get_fdata().astype(np.float32).shape)
        masks_path = '../Data/denoised_reformatted/ROIs_resampled_space-T1w/sub-0{}'.format(subject)
        masks_subdirs = [name for name in os.listdir(masks_path) if os.path.isdir(os.path.join(masks_path, name))]    
        for subdir in masks_subdirs: 
            mask_files = [name for name in os.listdir(os.path.join(masks_path, subdir)) if os.path.isfile(os.path.join(masks_path, subdir, name))] 
            for mask_file in mask_files:
                if mask_file!='.DS_Store':
                    # print('mask file: ', mask_file, 'number of voxels: ', np.sum((nib.load(os.path.join(masks_path, subdir, mask_file)).get_fdata().astype(np.float32))>0))
                    mask = mask + nib.load(os.path.join(masks_path, subdir, mask_file)).get_fdata().astype(np.float32)

        mask[mask>0] = 1

    return mask