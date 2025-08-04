import torch

# Change this to your actual model path
path = "backend/model/wav2vec_mlp.pt"

state_dict = torch.load(path, map_location="cpu")

print("=== Saved Keys in State Dict ===")
for key in state_dict.keys():
    print(f"- {key}")
