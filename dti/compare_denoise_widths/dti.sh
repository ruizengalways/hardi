#!/bin/sh

# Using denoised k7 mask for comparison

# Global variables
mask=../../preprocess/mask/denoised_k7_mask.nii.gz
bvecs=../../preprocess/registered_full/bvecs_raw
bvals=../../preprocess/registered_full/bvals_raw

# Raw paths
# data=../../x_raw_data/raw_data_in_order.nii.gz
# out=raw/raw
# mkdir raw

# echo Fitting raw
# dtifit -k $data -o $out -m $mask -r $bvecs -b $bvals -V  >> ${out}.out

for k in 5 7 9
do
    # Denoised paths
    data=../../preprocess/denoise/denoised_k${k}/denoised_k${k}.nii.gz
    out=denoised_k${k}/denoised_k${k}
    mkdir denoised_k${k}

    echo Fitting k${k}
    dtifit -k $data -o $out -m $mask -r $bvecs -b $bvals -V >> ${out}.out
done
