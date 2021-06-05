#!/bin/bash

# maxVal returns the larger of two given values
maxVal(){
	arg1=$1
    if (( $(bc <<< "$1 > $2") ))
	then
        local maxValue=$1
    else
        local maxValue=$2
    fi
	echo "$maxValue"
}

# Set counter to 1 and remove old log files
count=1
rm -r mesh/blockMeshLogs/*

# Loop through combinations of the triangle points and Reynolds number
for x1 in 15 17 19
do
	for x2 in 15 17 19 21 23 25
	do
		for x3 in 21 23 25
		do
			for y1 in 21 23 25
			do
				for y2 in 15 17 19
				do
					for y3 in 21 23 25
					do
						for Re in 200 400 600
						do
							# hVol and lVol are the outer height and length of the mesh
							hVol=40
							lVol=60
							echo "count: $count; x1: $x1; x2: $x2; x3: $x3; y1: $y1; y2: $y2; y3: $y3; Re: $Re;";
							count=$(($count+1))

							# Delete old mesh files from constant/polyMesh folders
							rm -r mesh/constant/polyMesh
							rm -r simple_laminar/constant/polyMesh

							# Set values in blockMeshDict

							sed -i "19s/.*/hVol $hVol;/" mesh/system/blockMeshDict
							sed -i "20s/.*/lVol $lVol;/" mesh/system/blockMeshDict
							sed -i "21s/.*/x1 $x1;/" mesh/system/blockMeshDict
							sed -i "22s/.*/y1 $y1;/" mesh/system/blockMeshDict
							sed -i "24s/.*/x2 $x2;/" mesh/system/blockMeshDict
							sed -i "25s/.*/y2 $y2;/" mesh/system/blockMeshDict
							sed -i "27s/.*/x3 $x3;/" mesh/system/blockMeshDict
							sed -i "28s/.*/y3 $y3;/" mesh/system/blockMeshDict

							sed -i "30s/.*/nBlock1XCells $(echo "2*$(maxVal $x1 $x2)/1" | bc);/" mesh/system/blockMeshDict
							sed -i "31s/.*/nBlock1YCells $(echo "2*($y1 - $y2)/1" | bc);/" mesh/system/blockMeshDict

							sed -i "32s/.*/nBlock2XCells $(echo "2*($lVol-$(maxVal $x2 $x3))/1" | bc);/" mesh/system/blockMeshDict
							sed -i "33s/.*/nBlock2YCells $(echo "2*($y3 - $y2)/1" | bc);/" mesh/system/blockMeshDict

							sed -i "34s/.*/nBlock3XCells $(echo "2*$(maxVal $x1 $x2)/1" | bc);/" mesh/system/blockMeshDict
							sed -i "35s/.*/nBlock3YCells $(echo "2*($hVol-$(maxVal $y1 $y3))/1" | bc);/" mesh/system/blockMeshDict

							sed -i "36s/.*/nBlock4XCells $(echo "2*($x3 - $x1)/1" | bc);/" mesh/system/blockMeshDict
							sed -i "37s/.*/nBlock4YCells $(echo "2*($hVol-$(maxVal $y1 $y3))/1" | bc);/" mesh/system/blockMeshDict

							sed -i "38s/.*/nBlock5XCells $(echo "2*($lVol-$(maxVal $x2 $x3))/1" | bc);/" mesh/system/blockMeshDict
							sed -i "39s/.*/nBlock5YCells $(echo "2*($hVol-$(maxVal $y1 $y3))/1" | bc);/" mesh/system/blockMeshDict

							sed -i "40s/.*/nBlock6XCells $(echo "2*$(maxVal $x1 $x2)/1" | bc);/" mesh/system/blockMeshDict
							sed -i "41s/.*/nBlock6YCells $(echo "2*$y2/1" | bc);/" mesh/system/blockMeshDict
							sed -i "42s/.*/nBlock7XCells $(echo "2*($lVol-$(maxVal $x2 $x3))/1" | bc);/" mesh/system/blockMeshDict
							sed -i "43s/.*/nBlock7YCells $(echo "2* $y2/1" | bc);/" mesh/system/blockMeshDict

							# Run blockMesh and save log in file
							cd mesh
							blockMesh > "blockMeshLogs/log_x1-${x1}_y1-${y1}_x2-${x2}_y2-${y2}_x3-${x3}_y3-${y3}.txt"
							cd ..

							# Copy new mesh to simple_laminar folder
							cp -r mesh/constant/polyMesh simple_laminar/constant

							# Change directory to simple_laminar folder
							cd simple_laminar

							echo -e "Remove folders from previous run.\n"
							rm -r processor*
							rm -r 0.* 1* 2* 3* 4* 5* 6* 7* 8* 9*
							rm log*

							echo -e "\nSet magUInf.\n"
							sed -i "78s/.*/        magUInf     $(python -c "Re=$Re; nu=0.00001; Dhyd=0.1; U=Re*nu/Dhyd; print U;"); /" system/controlDict

							echo -e "Set inlet velocity.\n"
							sed -i "27s/.*/        value           uniform ($(python -c "Re=$Re; nu=0.00001; Dhyd=0.1; U=Re*nu/Dhyd; print U;") 0 0); /" 0/U # Dhyd = 4*A/U; U = Re*nu/Dhyd;

							echo -e "Decompose case.\n"
							decomposePar >> logSimpleFoam

							echo -e "Renumber mesh for speedup.\n"
							mpirun -np 4 renumberMesh -overwrite -parallel >> logSimpleFoam

							echo -e "Run simpleFoam.\n"
							mpirun -np 4 simpleFoam -parallel >> logSimpleFoam

							echo -e "Reconstruct case.\n"
							reconstructPar >> logSimpleFoam

							echo -e "Copy results into C_D folder.\n"
							cd postProcessing/forces/*/.
							cp forceCoeffs.dat ../../../C_D/
							cd ../../..
							rm -r postProcessing/forces/
							mv "C_D/forceCoeffs.dat" "C_D/x1-${x1}_y1-${y1}_x2-${x2}_y2-${y2}_x3-${x3}_y3-${y3}_Re-${Re}.dat"

							echo -e "Copy residuals into residuals folder.\n"
							cd postProcessing/residuals/*/.
							cp residuals.dat ../../../residuals/
							cd ../../..
							rm -r postProcessing/residuals/
							mv "residuals/residuals.dat" "residuals/x1-${x1}_y1-${y1}_x2-${x2}_y2-${y2}_x3-${x3}_y3-${y3}_Re-${Re}.dat"
							rm -r postProcessing

							echo -e "Calculation done.\n"
							cd ..
						done
					done
				done
			done
		done
	done
done
