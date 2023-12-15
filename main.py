import numpy as np
import numpy.ma as ma 
import pickle
import pandas as pd
import os 
import nibabel as nib
import os 
import matplotlib.pyplot as plt
import utils 

#%%

for subject in [3]: 

    mask = utils.get_mask(subject=subject)
    n_total = 12*10*92
    fmri = np.zeros((n_total,int(np.sum(mask)),11))
    annotations = pd.DataFrame(index=range(n_total),columns=['type', 'label', 'file'])

    fmri_path = '../Data/preprocessed_denoised_copy/preprocessed_denoised/fmriprep/sub-{:02d}'.format(subject) 
    event_path = '../Data/Raw/THINGS-fMRI/sub-{:02d}'.format(subject) 

    ind = 0 

    for ses in range(1,13):
        for run in range(1,11): 
            fmri_file = 'sub-{:02d}_ses-things{:02d}_task-things_run-{}_space-T1w_desc-AROMAnonaggr_bold.nii.gz'.format(subject, ses, run)
            fdata =  nib.load(os.path.join(fmri_path, 'ses-things{:02d}'.format(ses), 'func', fmri_file)).get_fdata().astype(np.float32)
            event_file = 'sub-{:02d}_ses-things{:02d}_task-things_run-{:02d}_events.tsv'.format(subject, ses, run)
            event = pd.read_csv(os.path.join(event_path, 'ses-things{:02d}'.format(ses), 'func', event_file), sep='\t')

            fdata = fdata[mask>0]

            for trial in range(92):

                fmri[ind] = fdata[:,trial*3:trial*3+11]

                annotations.loc[ind, 'type'] = event.loc[trial, 'trial_type']
                annotations.loc[ind, 'label'] = event.loc[trial, 'category_nr']
                annotations.loc[ind, 'file'] = event.loc[trial, 'file_path']

                ind = ind+1 

            print('run {}'.format(run))

        print('session {} completed!'.format(ses))
    
    annotations.to_csv('../Data/denoised_reformatted/sub-{:02d}/sub-{:02d}_annotations.csv'.format(subject, subject))
    np.save('../Data/denoised_reformatted/sub-{:02d}/sub-{:02d}_fdata.npy'.format(subject, subject), fmri)





# %%
