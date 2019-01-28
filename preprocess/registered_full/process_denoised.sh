#!/bin/sh

# Using the optimal parameters, this script does full registration of the
# denoised data for each filter width

# Registration parameters
b0cost=corratio
b0dof=12
dwicost=mutualinfo
sch3dof=${FSLDIR}/etc/flirtsch/sch3Dtrans_3dof
interp=sinc

for k in 5 7 9
do
    echo Working on filter width: ${k}
    
    echo Making output directory
    fnbase=../denoise/denoised_k${k}/denoised_k${k}
    outdir=denoised_k${k}_registered
    mkdir $outdir
    outfile=${outdir}/denoised_k${k}_registration.out

    echo b0 registration
    # Registering all b0s to n0008 with corratio cost function and 12 dof
    b0ref=${fnbase}_n0008.nii.gz
    cp $b0ref $outdir/denoised_k${k}_registered_n0008.nii.gz

    for num in 000{0..7} 0009 00{10..15}  # registering to 8
    do
    	input=${fnbase}_n${num}.nii.gz
    	output=${outdir}/denoised_k${k}_registered_n${num}.nii.gz
    	echo b0=${num}
    	flirt -cost $b0cost -interp $interp -dof $b0dof -in $input -ref $b0ref -out $output >> ${outfile}
    done

    echo Merging registered b0s into single 4D file
    fslmerge -t ${outdir}/denoised_k${k}_registered_b0_full.nii.gz ${outdir}/denoised_k${k}_registered_*.nii.gz

    echo Creating average b0 for DWI registration
    fslmaths ${outdir}/denoised_k${k}_registered_b0_full.nii.gz -Tmean ${outdir}/denoised_k${k}_registered_mean_b0.nii.gz

    echo Registering DWI volumes to mean registered b0
    for num in 00{16..99} 0{100..159}
    do
    	input=${fnbase}_n${num}.nii.gz
    	output=${outdir}/denoised_k${k}_registered_n${num}.nii.gz
    	echo dir=${num}
    	flirt -cost $dwicost -interp $interp -schedule ${sch3dof} -in $input -ref ${outdir}/denoised_k${k}_registered_mean_b0.nii.gz -out $output >> ${outfile}
    done

    echo Creating a single file with 1 b0 every 9 DWIs
    base=${outdir}/denoised_k${k}_registered
    fslmerge -t denoised_k${k}_registered.nii.gz \
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

    echo Done!
done
