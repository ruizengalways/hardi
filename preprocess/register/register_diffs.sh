# This script registers all diffs to the mean registered b0

for k in 5 7 9
do
    echo $k
    fnbase=../denoise/denoised_k${k}/denoised_k${k}
    reference=k${k}/mean_registered_k${k}_b0.nii.gz  # registering all to mean b0

    cost=mutualinfo
    interp=sinc
    dof=9
    
    for num in 00{16..99} 0{100..159}  # iterating over all diffs
    do
	echo k=${k}, diff=$num
	input=${fnbase}_n${num}.nii.gz
	output=k${k}/registered_k${k}_n${num}.nii.gz
	flirt -cost $cost -interp $interp -dof $dof -in $input -ref $reference -out $output
    done

    # Merges registered volumes into a single 4D file
    fslmerge -t k${k}/registered_k${k}_full.nii.gz k${k}/registered_k${k}_n*.nii.gz

    # Calculates mean and std MI of registrations
    python mutualinfo.py $k 1024 comparison_stats/diffs_k${k}_${cost}_${interp}_dof${dof}_noweight.txt
    
done
