#!/bin/sh

base=choose_diff_params

for weighting in w nw
do
    for dof in 3 6 9 12
    do
	newfn=${base}_${weighting}_dof${dof}.sh
	cp ${base}.sh $newfn
	echo "dof=${dof}" | cat - ${newfn} > temp && mv temp $newfn
	echo "weighting=${weighting}" | cat - ${newfn} > temp && mv temp $newfn
	echo "#!/bin/sh" | cat - ${newfn} > temp && mv temp $newfn	
    done
done
