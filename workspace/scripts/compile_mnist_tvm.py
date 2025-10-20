import tvm
from tvm import relay
import onnx
import os

MODEL_DIR = "/root/workspace/models"
onnx_model_path = os.path.join(MODEL_DIR, "mnist_model.onnx")
target = "llvm"

print("[1] Load ONNX model")
onnx_model = onnx.load(onnx_model_path)

print("[2] Convert ONNX to Relay IR")
shape_dict = {"input": (1, 1, 28, 28)}
mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

print("[3] Compile with TVM")
target = tvm.target.Target("llvm")
with tvm.transform.PassContext(opt_level=3):
    lib = relay.build(mod, target=target, params=params)

output_path = os.path.join(MODEL_DIR, "mnist_model_tvm.so")
lib.export_library(output_path)
print(f"TVM compiled model saved at: {output_path}")

