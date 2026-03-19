import torch

print(f'Device available : {"cuda" if torch.cuda.is_available() else "cpu"}')
