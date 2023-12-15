#!/bin/bash
#PBS -l walltime=60:00:00,select=1:ncpus=20:mem=128gb
#PBS -N fmriprep
#PBS -A st-ipor-1

#PBS -o /scratch/st-ipor-1/parsadlr/Brain-Graph/log/output.txt
#PBS -e /scratch/st-ipor-1/parsadlr/Brain-Graph/log/error.txt
 
################################################################################

 
cd $PBS_O_WORKDIR

module unuse /arc/software/spack/share/spack/lmod/linux-centos7-x86_64/Core
module use /arc/software/spack-0.14.0-110/share/spack/lmod/linux-centos7-x86_64/Core

#module load openmpi/3.1.5
#module load openblas
module load miniconda3
module load apptainer
source ~/.bashrc

cd /scratch/st-ipor-1/parsadlr/Brain-Graph/
conda activate Brain-Graph

#User inputs:
bids_root_dir=/scratch/st-ipor-1/parsadlr/Brain-Graph/Data/Raw/THINGS-fMRI
out_dir=/scratch/st-ipor-1/parsadlr/Brain-Graph/Data/preprocessed_denoised
subj=01
nthreads=40
mem=120 #gb

#Begin:
#Convert virtual memory from gb to mb
mem=`echo "${mem//[!0-9]/}"` #remove gb at end
mem_mb=`echo $(((mem*1000)-5000))` #reduce some memory for buffer space during pre-processing

FMRIPREP=/project/st-ipor-1/parsadlr/my_images/fmriprep.simg
FS_LICENSE=/scratch/st-ipor-1/parsadlr/Brain-Graph/license/license.txt

#Run fmriprep
singularity run \
  $FMRIPREP \
  $bids_root_dir $out_dir \
  participant \
  --participant-label $subj \
  --task-id things \
  --output-spaces T1w func \
  --bold2t1w-dof 9 \
  --fs-license-file /scratch/st-ipor-1/parsadlr/Brain-Graph/license/license.txt \
  --bids-filter-file /scratch/st-ipor-1/parsadlr/Brain-Graph/filtercfg.json \
  --fs-no-reconall \
  --nthreads $nthreads \
  --stop-on-first-crash \
  --mem_mb $mem_mb \
  --verbose \
  --use-aroma \
  -w /scratch/st-ipor-1/parsadlr/Brain-Graph/fmriprep_wdir
