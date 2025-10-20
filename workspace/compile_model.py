# workspace/compile_model.py
import tvm
from tvm import relay
import onnx
from tvm.contrib import graph_executor

# 1. ONNX 모델 로드
onnx_model = onnx.load("/root/workspace/models/mnist_model.onnx")

# 2. Relay 변환
mod, params = relay.frontend.from_onnx(onnx_model, shape={"input": (1, 1, 28, 28)})

# 3. VTA 타겟 지정
target = tvm.target.Target("llvm")
with tvm.transform.PassContext(opt_level=3):
    lib = relay.build(mod, target=target, params=params)

# 4. 결과 저장
lib.export_library("/root/workspace/mnist_vta.so")

