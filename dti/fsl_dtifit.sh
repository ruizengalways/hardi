#!/bin/sh

# Using denoised k7 mask for comparison

# Global variables
mask=../preprocess/mask/denoised_k7_mask.nii.gz
bvecs=../preprocess/registered_full/bvecs_raw
bvals=../preprocess/registered_full/bvals_raw

# Raw paths
data=../preprocess/registered_full/raw_registered.nii.gz
out=raw/raw

echo Fitting raw
dtifit -k $data -o $out -m $mask -r $bvecs -b $bvals -V --sse --save_tensor >> ${out}.out

for k in 5 7 9
do
    # Denoised paths
    data=../preprocess/registered_full/denoised_k${k}_registered.nii.gz
    out=denoised_k${k}/denoised_k${k}

    echo Fitting k${k}
    dtifit -k $data -o $out -m $mask -r $bvecs -b $bvals -V --sse --save_tensor >> ${out}.out

done
