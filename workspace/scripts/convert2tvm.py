import tvm
from tvm import relay
import onnx
import numpy as np

onnx_model_path = "/root/workspace/models/mnist_model.onnx"

onnx_model = onnx.load(onnx_model_path)

input_name = "input"
shape_dict = {input_name: (1, 1, 28, 28)}

mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

target = "llvm"

with tvm.transform.PassContext(opt_level=3):
    lib = relay.build(mod, target=target, params=params)

lib.export_library("/root/workspace/models/mnist_tvm.so")
with open("/root/workspace/models/mnist_tvm.json", "w") as f:
    f.write(mod.astext(show_meta_data=False))
with open("/root/workspace/models/mnist_tvm.params", "wb") as f:
    f.write(relay.save_param_dict(params))

