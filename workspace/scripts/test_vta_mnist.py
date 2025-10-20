import tvm
from tvm import relay, autotvm
from tvm.contrib import graph_executor
import onnx
import numpy as np
import os

MODEL_PATH = "/root/workspace/models/mnist_model.onnx"

onnx_model = onnx.load(MODEL_PATH)

target = tvm.target.Target("vta")
shape_dict = {"input": (1, 1, 28, 28)}
mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

with tvm.transform.PassContext(opt_level=3):
    lib = relay.build(mod, target=target, params=params)

dev = tvm.vta.get_dev()
module = graph_executor.GraphModule(lib["default"](dev))

input_data = np.random.randn(1, 1, 28, 28).astype("float32")
module.set_input("input", input_data)

module.run()
output = module.get_output(0).asnumpy()

print("shape:", output.shape)
print(output[0][:5])

