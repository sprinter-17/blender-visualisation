# blender-visualisation

These python scripts are used to create an animation in Blender representing the results of a simulation in CDF.

The process happens in 3 steps.

1. Run convert_netcdf.py to extract the positions of the beads at each frame from the netCDF4 file. The output should be written to a text file:

python3 convert_netcdf.py >> data/output.dat

2. Open Blender, delete the default cube then go to the scripting tab. Open create_animation.py file and change the line that opens the input file to use the file created in step 1. Run the script.

3. Position camera, lighting and set materials to achieve the desired look.

4. Render the animation
