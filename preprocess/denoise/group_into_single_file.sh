#!/bin/sh
for k in 5 7 9
do
    echo $k
    dir=denoised_k${k}
    echo Creating a single file with 1 b0 every 9 DWIs

    base=${dir}/denoised_k${k}
    fslmerge -t ${dir}/denoised_k${k}.nii.gz \
	     ${base}_n0000.nii.gz \
	     ${base}_n00{16..24}.nii.gz \
	     ${base}_n0001.nii.gz \
	     ${base}_n00{25..33}.nii.gz \
	     ${base}_n0002.nii.gz \
	     ${base}_n00{34..42}.nii.gz \
	     ${base}_n0003.nii.gz \
	     ${base}_n00{43..51}.nii.gz \
	     ${base}_n0004.nii.gz \
	     ${base}_n00{52..60}.nii.gz \
	     ${base}_n0005.nii.gz \
	     ${base}_n00{61..69}.nii.gz \
	     ${base}_n0006.nii.gz \
	     ${base}_n00{70..78}.nii.gz \
	     ${base}_n0007.nii.gz \
	     ${base}_n00{79..87}.nii.gz \
	     ${base}_n0008.nii.gz \
	     ${base}_n00{88..96}.nii.gz \
	     ${base}_n0009.nii.gz \
	     ${base}_n00{97..99}.nii.gz \
	     ${base}_n0{100..105}.nii.gz \
	     ${base}_n0010.nii.gz \
	     ${base}_n0{106..114}.nii.gz \
	     ${base}_n0011.nii.gz \
	     ${base}_n0{115..123}.nii.gz \
	     ${base}_n0012.nii.gz \
	     ${base}_n0{124..132}.nii.gz \
	     ${base}_n0013.nii.gz \
	     ${base}_n0{133..141}.nii.gz \
	     ${base}_n0014.nii.gz \
	     ${base}_n0{142..150}.nii.gz \
	     ${base}_n0015.nii.gz \
	     ${base}_n0{151..159}.nii.gz
done
