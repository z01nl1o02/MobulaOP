# Use ROIAlign operator
import mxnet as mx
import numpy as np
import sys
sys.path.append('../') # Add MobulaOP path
import mobula_op

ctx = mx.gpu()
dtype = np.float32
N, C, H, W = 2, 3, 4, 4

data = mx.nd.array(np.arange(N*C*H*W).astype(dtype).reshape((N,C,H,W)),ctx=ctx)
rois = mx.nd.array(np.array([[0, 1, 1, 3, 3]], dtype = dtype),ctx=ctx)

data.attach_grad()
with mx.autograd.record():
    # mx.nd.NDArray and mx.sym.Symbol are both available as the inputs.
    output = mobula_op.operator.ROIAlign(data = data, rois = rois, pooled_size = (2,2), spatial_scale = 1.0, sampling_ratio = 1)

output.backward()

mx.nd.waitall()
print (output.asnumpy(), data.grad.asnumpy())