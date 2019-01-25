# This script sweeps through some tunable registration parameters
# to choose the best way to register the DWIs together. I am using
# the denoised data with the k7 filter width. 

fnbase=../../denoise/denoised_k7/denoised_k7
reference=../registered_b0/mean_registered_b0.nii.gz 

cost=mutualinfo  # not looking at corratio, we know the contrast is different
interp=sinc
sch=${FSLDIR}/etc/flirtsch/sch3Dtrans_3dof


if [ $dof -eq 3 ]
then
    dofarg="-schedule ${sch}"
else
    dofarg="-dof ${dof}"
fi

if [ $weighting = w ]
then
    weightarg="-refweight ${reference}"
elif [ $weighting = nw ]
then
     weightarg=""
fi
    
outdir=dof${dof}_${weighting}
mkdir $outdir
    
for num in 00{16..99} 0{100..159}  # iterating over all diffs
do
    echo "weighting=${weighting}, dof=${dof}, diff=${num}"
    input=${fnbase}_n${num}.nii.gz
    output=${outdir}/${outdir}_n${num}.nii.gz

    flirt -cost $cost -interp $interp ${dofarg} ${weightarg} -in $input -ref $reference -out $output
done
