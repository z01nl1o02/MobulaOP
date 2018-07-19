# MobulaOP-windows

fork from [MobulaOP](https://github.com/wkcn/MobulaOP) to work under windows

# system
* win10 64bits
* vs2015
* cuda 8.0
* cmake 3.9.1

# usage

1. rename all cpp to cu   
   MobulaOp/mobula_op/cp_cpp2cu.py   

2. call cmake gui to create configuration files for vs2015 64bits   
   MobulaOp/mobula_op/CMakeLists.txt

3. build mobula_op_gpu.dll with vs2015   

4. copy mobula_op_gpu.dll to MobulaOP/mobula_op/build/   
   reference mobula_op/func.py for reason

5. verification   
   python MobulaOP\examples\ROIAlignOP_GPU.py 



