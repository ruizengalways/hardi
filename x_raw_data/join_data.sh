# using mrtrix3 instead of fsl because `fslmerge` changes the bit depth to 32

mrcat x3D_DWSE_100um_*.nii.gz raw_data.nii.gz
