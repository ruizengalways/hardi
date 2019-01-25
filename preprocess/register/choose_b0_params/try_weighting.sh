# corratio cost function with 12 dof worked best. Here, I am looking
# at whether adding weighting makes it any better

fnbase=../../denoise/denoised_k7/denoised_k7

# Looking at n0 and n8 as references
for n in 0 8
do
    reference=${fnbase}_n0008.nii.gz
    weight=${fnbase}_n000${n}.nii.gz    

    outdir=${cost}_${dof}_weighted_n${n}
    mkdir $outdir
    cp $reference $outdir/${cost}_${dof}_n0008.nii.gz  # copying reference image into "registered" folder

    interp=sinc  # using sinc interpolation for all registrations

    if [ n -eq 0 ]
    then
	for num in 000{1..9} 00{10..15}  # iterating over all other b0 volumes
	do

	    input=${fnbase}_n${num}.nii.gz
	    output=${outdir}/${cost}_${dof}_n${num}.nii.gz

	    echo $cost dof=${dof} b0=${num}
	    flirt -cost $cost -interp $interp -dof $dof -refweight $weight -in $input -ref $reference -out $output
	done
    fi

    if [ n -eq 8 ]
    then
	for num in 000{0..7} 0009 00{10..15}  # iterating over all other b0 volumes
	do

	    input=${fnbase}_n${num}.nii.gz
	    output=${outdir}/${cost}_${dof}_n${num}.nii.gz

	    echo $cost dof=${dof} b0=${num}
	    flirt -cost $cost -interp $interp -dof $dof -refweight $weight -in $input -ref $reference -out $output
    fi
done


