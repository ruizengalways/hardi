rawdata=../../x_raw_data/raw_data.nii.gz

for k in 5 7 9
do
    echo $k
    denoised=denoised_k${k}/denoised_k${k}.nii.gz
    out=denoised_k${k}/noise_k${k}.nii.gz
    fslmaths $rawdata -sub $denoised $out
done

    
