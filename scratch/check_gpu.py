import subprocess, sys
result = subprocess.run([sys.executable, "-c",
    "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'none')"
], capture_output=True, text=True)
print(result.stdout or result.stderr)
