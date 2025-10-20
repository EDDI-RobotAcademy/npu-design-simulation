# compile_onnx_tvm.py
import onnx
import tvm
from tvm import relay
from tvm.contrib import utils
import numpy as np
import os
import json

onnx_path = "lenet_mnist.onnx"
input_name = "input"
shape_dict = {input_name: (1,1,28,28)}
target = "llvm"

model = onnx.load(onnx_path)
mod, params = relay.frontend.from_onnx(model, shape_dict)

with tvm.transform.PassContext(opt_level=3):
    lib = relay.build(mod, target=target, params=params)

out_dir = "tvm_build"
os.makedirs(out_dir, exist_ok=True)
lib.export_library(os.path.join(out_dir, "deploy_lib.tar"))
open(os.path.join(out_dir, "deploy_graph.json"), "w").write(lib.get_graph_json())
with open(os.path.join(out_dir, "deploy_param.params"), "wb") as f:
    f.write(relay.save_param_dict(lib.get_params()))

print("TVM artifacts saved to", out_dir)

