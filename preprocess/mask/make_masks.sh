#!/bin/sh

input=../registered_full/raw_registered/raw_registered_mean_b0.nii.gz
output=raw.nii.gz

echo Making raw mask

bet $input $output -m -n

for k in 5 7 9
do
    echo Making k${k} mask
    input=../registered_full/denoised_k${k}_registered/denoised_k${k}_registered_mean_b0.nii.gz
    output=denoised_k${k}.nii.gz

    bet $input $output -m -n
done


