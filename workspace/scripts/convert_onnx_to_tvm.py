import tvm
from tvm import relay
import onnx
import os
from tvm.contrib import utils, ndk

MODEL_DIR = "/root/workspace/models"
ONNX_MODEL_PATH = os.path.join(MODEL_DIR, "mnist_model.onnx")

onnx_model = onnx.load(ONNX_MODEL_PATH)

input_name = "input"
shape_dict = {input_name: (1, 1, 28, 28)}

mod, params = relay.frontend.from_onnx(onnx_model, shape_dict)

target = "llvm"
with tvm.transform.PassContext(opt_level=3):
    lib = relay.build(mod, target=target, params=params)

output_dir = os.path.join(MODEL_DIR, "tvm_build")
os.makedirs(output_dir, exist_ok=True)
lib.export_library(os.path.join(output_dir, "deploy_lib.so"))

with open(os.path.join(output_dir, "model.json"), "w") as f:
    f.write(mod.astext())

param_path = os.path.join(output_dir, "model.params")
with open(param_path, "wb") as f:
    f.write(tvm.runtime.save_param_dict(params))

print(f"✅ TVM build completed. Files saved in {output_dir}")

