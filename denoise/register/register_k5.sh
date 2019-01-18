reference=../split_k5/denoised_k5_x3D_DWSE_100um_TR1000_b0_rep08.nii.gz
cp $reference registered_k5/denoised_k5_registered_b0_rep08.nii.gz

for num in {1..7} 9
do
    echo $num
    input=../split_k5/denoised_k5_x3D_DWSE_100um_TR1000_b0_rep0${num}.nii.gz
    output=registered_k5/denoised_k5_registered_b0_rep0${num}.nii.gz

    flirt -in $input -ref $reference -out $output -interp sinc -sincwidth 7 -sincwindow hanning
done

for num in {10..16}
do
    echo $num
    input=../split_k5/denoised_k5_x3D_DWSE_100um_TR1000_b0_rep${num}.nii.gz
    output=registered_k5/denoised_k5_registered_b0_rep${num}.nii.gz


    flirt -in $input -ref $reference -out $output -interp sinc -sincwidth 7 -sincwindow hanning
done

echo "Joining images"
mrcat registered_k5/*.nii.gz registered_k5/denoised_k5_registered_b0s.nii.gz

echo "Averaging"
python average_b0_k5.py

echo "Registering diffusion weighted"

reference=registered_k5/denoised_k5_averaged_registered_b0.nii.gz

for num in {1..9}
do
    echo $num
    input=../split_k5/denoised_k5_x3D_DWSE_100um_TR1000_dir00${num}.nii.gz
    output=registered_k5/denoised_k5_registered_dir00${num}.nii.gz

    flirt -in $input -ref $reference -out $output -interp sinc -sincwidth -sincwindow hanning
done
for num in {10..99}
do
    echo $num
    input=../split_k5/denoised_k5_x3D_DWSE_100um_TR1000_dir0${num}.nii.gz
    output=registered_k5/denoised_k5_registered_dir0${num}.nii.gz

    flirt -in $input -ref $reference -out $output -interp sinc -sincwidth -sincwindow hanning
done
for num in {100..144}
do
    echo $num
    input=../split_k5/denoised_k5_x3D_DWSE_100um_TR1000_dir${num}.nii.gz
    output=registered_k5/denoised_k5_registered_dir${num}.nii.gz

    flirt -in $input -ref $reference -out $output -interp sinc -sincwidth -sincwindow hanning
done

echo "Joining all images"
mrcat $reference registered_k5/denoised_k5_registered_dir*.nii.gz denoised_k5_registered_all.nii.gz
