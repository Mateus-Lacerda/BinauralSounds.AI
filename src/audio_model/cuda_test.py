import torch
import os

def test_cuda():
    print("Versão do PyTorch:", torch.__version__)

    is_cuda_available = torch.cuda.is_available()
    if is_cuda_available:
        os.environ["CUDA_AVAILABLE"] = "True"
        print("CUDA disponível:", is_cuda_available)

    else:
        os.environ["CUDA_AVAILABLE"] = "False"
        print("CUDA disponível:", is_cuda_available)

if __name__ == "__main__":
    test_cuda()