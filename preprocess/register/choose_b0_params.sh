# This script sweeps through some tunable registration parameters to
# choose the best way to register the b0s together. I am tuning everything
# to the k7 filter width. I imagine the optimal parameters are not
# very sensitive to the filter width. 

fnbase=../denoise/denoised_k7/denoised_k7

# choosing the 8th b0 as reference, the first 1-3ish
# have a structure that does not appear in the others
reference=${fnbase}_n0008.nii.gz

# Making b0_param_sweep folder if it does not exist
if [ ! -d b0_param_sweep ]
then
    mkdir b0_param_sweep
fi


for cost in corratio mutualinfo  # trying two cost functions
do
    for dof in 3 6 9 12  # trying different degrees of freedom
    do
	outdir=b0_param_sweep/${cost}_${dof}
	mkdir $outdir
	cp $reference $outdir/${cost}_${dof}_n0008.nii.gz  # copying reference image into "registered" folder

	interp=sinc  # using sinc interpolation for all registrations

	for num in 000{0..7} 0009 00{10..15}  # iterating over all other b0 volumes
	do

	    input=${fnbase}_n${num}.nii.gz
	    output=${outdir}/${cost}_${dof}_n${num}.nii.gz

	    if [ $dof -eq 3 ]  # need special schedule for dof=3
	    then
		echo $cost dof=${dof} b0=${num}
		sch=${FSLDIR}/etc/flirtsch/sch3Dtrans_3dof

		flirt -cost $cost -interp $interp -schedule $sch -in $input -ref $reference -out $output
	    else  # all other dofs
		echo $cost dof=${dof} b0=${num}

		flirt -cost $cost -interp $interp -dof $dof -in $input -ref $reference -out $output
	    fi
	    
	done
    done
done
