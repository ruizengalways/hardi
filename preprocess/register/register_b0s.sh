# This script registers all b0s to a reference

for k in 5 7 9
do
    echo $k
    fnbase=../denoise/denoised_k${k}/denoised_k${k}
    refnum=8
    reference=${fnbase}_n000${refnum}.nii.gz  # registering all to refnum b0
    cp $reference k${k}/registered_k${k}_n000${refnum}.nii.gz

    cost=corratio
    interp=sinc
    dof=6
    
    for num in 000{0..7} 0009 00{10..15}  # iterating over other 15 b0s
    do
	echo k=${k}, b0=$num
	input=${fnbase}_n${num}.nii.gz
	output=k${k}/registered_k${k}_n${num}.nii.gz
	flirt -cost $cost -interp $interp -dof $dof -in $input -ref $reference -out $output
    done

    # Merges registered b0s into a single 4D file
    fslmerge -t k${k}/registered_k${k}_b0.nii.gz k${k}/registered_k${k}_n000{0..9}.nii.gz k${k}/registered_k${k}_n00{10..15}.nii.gz

    # Saves registered, averaged b0 data
    fslmaths k${k}/registered_k${k}_b0.nii.gz -Tmean k${k}/mean_registered_k${k}_b0.nii.gz

    # Calculates mean and std RMSE of registrations
    python rmse.py $k $refnum comparison_stats/b0s_k_${k}_ref${refnum}_${cost}_${interp}_dof${dof}_noweight.txt
    
done
