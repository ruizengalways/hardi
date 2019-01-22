# Splits denoised images into individual volumes for registration

for k in 5 7 9
do
    input=denoised_k${k}/denoised_k${k}.nii.gz
    base=denoised_k${k}/denoised_k${k}_n
    fslsplit $input $base -t
done
