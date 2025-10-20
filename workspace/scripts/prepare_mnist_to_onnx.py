#!/usr/bin/env python3
# 간단한 MNIST 작은 모델을 만들고 ONNX로 내보내는 스크립트
import torch
import torch.nn as nn
import torch.onnx
import os

MODEL_DIR="/root/workspace/models"
os.makedirs(MODEL_DIR, exist_ok=True)

class SimpleMNIST(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)
    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleMNIST().eval()
dummy = torch.randn(1,1,28,28)
onnx_path = os.path.join(MODEL_DIR, "mnist_model.onnx")
torch.onnx.export(model, dummy, onnx_path, input_names=["input"], output_names=["output"], opset_version=11)
print("Saved ONNX model to", onnx_path)

