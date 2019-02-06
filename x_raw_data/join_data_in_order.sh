#!/bin/sh

echo Creating a single file with 1 b0 every 9 DWIs
base=x3D_DWSE_100um_TR1000
fslmerge -t raw_data_in_order.nii.gz \
	 ${base}_b0_rep01.nii.gz \
	 ${base}_dir00{1..9}.nii.gz \
	 ${base}_b0_rep02.nii.gz \
	 ${base}_dir0{10..18}.nii.gz \
	 ${base}_b0_rep03.nii.gz \
	 ${base}_dir0{19..27}.nii.gz \
	 ${base}_b0_rep04.nii.gz \
	 ${base}_dir0{28..36}.nii.gz \
	 ${base}_b0_rep05.nii.gz \
	 ${base}_dir0{37..45}.nii.gz \
	 ${base}_b0_rep06.nii.gz \
	 ${base}_dir0{46..54}.nii.gz \
	 ${base}_b0_rep07.nii.gz \
	 ${base}_dir0{55..63}.nii.gz \
	 ${base}_b0_rep08.nii.gz \
	 ${base}_dir0{64..72}.nii.gz \
	 ${base}_b0_rep09.nii.gz \
	 ${base}_dir0{73..81}.nii.gz \
	 ${base}_b0_rep10.nii.gz \
	 ${base}_dir0{82..90}.nii.gz \
	 ${base}_b0_rep11.nii.gz \
	 ${base}_dir0{91..99}.nii.gz \
	 ${base}_b0_rep12.nii.gz \
	 ${base}_dir{100..108}.nii.gz \
	 ${base}_b0_rep13.nii.gz \
	 ${base}_dir{109..117}.nii.gz \
	 ${base}_b0_rep14.nii.gz \
	 ${base}_dir{118..126}.nii.gz \
	 ${base}_b0_rep15.nii.gz \
	 ${base}_dir{127..135}.nii.gz \
	 ${base}_b0_rep16.nii.gz \
	 ${base}_dir{136..144}.nii.gz
