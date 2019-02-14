#!/bin/sh

echo "Swapping raw data"
input=../../x_raw_data/raw_data_in_order.nii.gz
output=data/raw.nii.gz

fslswapdim $input -x z y $output

for k in 5 7 9
do
    echo "Swapping $k"
    input=../../preprocess/denoise/denoised_k${k}/denoised_k${k}_true_order.nii.gz
    output=data/denoised_k${k}.nii.gz

    fslswapdim $input -x z y $output
done    

echo "Swapping mask"
input=../../preprocess/mask/denoised_k7_mask.nii.gz
output=data/mask.nii.gz

fslswapdim $input -x z y $output
