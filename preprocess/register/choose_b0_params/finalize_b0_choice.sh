#!/bin/sh

# After deciding to use the corratio_12 registration as the final b0,
# this script copies it to a new folder, groups all of the registered
# b0s together and generates an average b0 image to use for DWI
# registration

dir=../registered_b0
mkdir $dir

cp corratio_12/corratio_12_n*.nii.gz $dir
for n in 000{0..9} 00{10..15}
do
    mv ${dir}/corratio_12_n${n}.nii.gz ${dir}/registered_b0_n${n}.nii.gz
done

fslmerge -t ${dir}/registered_b0_full.nii.gz ${dir}/registered_b0_n*.nii.gz
fslmaths ${dir}/registered_b0_full.nii.gz -Tmean ${dir}/mean_registered_b0.nii.gz
