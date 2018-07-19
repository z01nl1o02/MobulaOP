cmake_minimum_required(VERSION 2.6)

project(mobula_op_gpu LANGUAGES CXX CUDA)

#find_package(CUDA REQUIRED)

set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} --expt-extended-lambda -gencode arch=compute_50,code=sm_50")


add_definitions(-DUSING_CUDA=1)
add_definitions(-DUSING_CBLAS=0)

include_directories (inc/ inc/op/ inc/context/)
file(GLOB_RECURSE CURRENT_HEADERS  inc/*.h inc/*.hpp inc/*.cuh)
file(GLOB_RECURSE CURRENT_SOURCES  src/*.cu) #don't use cpp

source_group("inc" FILES ${CURRENT_HEADERS}) 
source_group("src" FILES ${CURRENT_SOURCES}) 

#message(STATUS ${CURRENT_HEADERS}) 

add_library(mobula_op_gpu SHARED ${CURRENT_SOURCES})
set_target_properties(mobula_op_gpu PROPERTIES CUDA_SEPARABLE_COMPILATION ON)