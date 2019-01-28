#!/bin/sh

# Using the optimal parameters, this script does full registration of the
# raw data

# Registration parameters
b0cost=corratio
b0dof=12
dwicost=mutualinfo
sch3dof=${FSLDIR}/etc/flirtsch/sch3Dtrans_3dof
interp=sinc

echo Making output directory
fnbase_raw=../../x_raw_data/x3D_DWSE_100um_TR1000
outdir_raw=raw_registered
mkdir $outdir_raw
outfile=${outdir_raw}/raw_registration.out

echo b0 registration
# Registering all b0s to rep09 with corratio cost function and 12 dof
b0ref_raw=${fnbase_raw}_b0_rep09.nii.gz
cp $b0ref_raw $outdir_raw/raw_registered_b0_n09.nii.gz

for num in 0{1..8} {10..16}  registering to 9
do
    input=${fnbase_raw}_b0_rep${num}.nii.gz
    output=${outdir_raw}/raw_registered_b0_n${num}.nii.gz
    echo b0=${num}
    flirt -cost $b0cost -interp $interp -dof $b0dof -in $input -ref $b0ref_raw -out $output >> ${outfile}
done

echo Merging registered b0s into single 4D file
fslmerge -t ${outdir_raw}/raw_registered_b0_full.nii.gz ${outdir_raw}/raw_registered_b0_n*.nii.gz

echo Creating average b0 for DWI registration
fslmaths ${outdir_raw}/raw_registered_b0_full.nii.gz -Tmean ${outdir_raw}/raw_registered_mean_b0.nii.gz

echo Registering DWI volumes to mean registered b0
for num in 00{1..9} 0{10..99} {100..144}
do
    input=${fnbase_raw}_dir${num}.nii.gz
    output=${outdir_raw}/raw_registered_dir_n${num}.nii.gz
    echo dir=${num}
    flirt -cost $dwicost -interp $interp -schedule ${sch3dof} -in $input -ref ${outdir_raw}/raw_registered_mean_b0.nii.gz -out $output >> ${outfile}
done

echo Creating a single file with 1 b0 every 9 DWIs
base=${outdir_raw}/raw_registered
fslmerge -t raw_registered.nii.gz \
	 ${base}_b0_n01.nii.gz \
	 ${base}_dir_n00{1..9}.nii.gz \
	 ${base}_b0_n02.nii.gz \
	 ${base}_dir_n0{10..18}.nii.gz \
	 ${base}_b0_n03.nii.gz \
	 ${base}_dir_n0{19..27}.nii.gz \
	 ${base}_b0_n04.nii.gz \
	 ${base}_dir_n0{28..36}.nii.gz \
	 ${base}_b0_n05.nii.gz \
	 ${base}_dir_n0{37..45}.nii.gz \
	 ${base}_b0_n06.nii.gz \
	 ${base}_dir_n0{46..54}.nii.gz \
	 ${base}_b0_n07.nii.gz \
	 ${base}_dir_n0{55..63}.nii.gz \
	 ${base}_b0_n08.nii.gz \
	 ${base}_dir_n0{64..72}.nii.gz \
	 ${base}_b0_n09.nii.gz \
	 ${base}_dir_n0{73..81}.nii.gz \
	 ${base}_b0_n10.nii.gz \
	 ${base}_dir_n0{82..90}.nii.gz \
	 ${base}_b0_n11.nii.gz \
	 ${base}_dir_n0{91..99}.nii.gz \
	 ${base}_b0_n12.nii.gz \
	 ${base}_dir_n{100..108}.nii.gz \
	 ${base}_b0_n13.nii.gz \
	 ${base}_dir_n{109..117}.nii.gz \
	 ${base}_b0_n14.nii.gz \
	 ${base}_dir_n{118..126}.nii.gz \
	 ${base}_b0_n15.nii.gz \
	 ${base}_dir_n{127..135}.nii.gz \
	 ${base}_b0_n16.nii.gz \
	 ${base}_dir_n{136..144}.nii.gz

echo Done!
