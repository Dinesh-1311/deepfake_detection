# backend/model/architecture.py
import torch.nn as nn

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)

class CRNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)

class Wav2VecClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(768, 256),   # net.0
            nn.ReLU(),             # net.1
            nn.Identity(),         # net.2 (to skip and match index)
            nn.Linear(256, 64),    # net.3
            nn.ReLU(),             # net.4
            nn.Identity(),         # net.5
            nn.Linear(64, 1),      # net.6
            nn.Sigmoid()           # net.7
        )

    def forward(self, x):
        return self.net(x)


MODEL_PATHS = {
    "cnn": "backend/model/cnn_full.pt",
    "crnn": "backend/model/crnn_full.pt",
    "wav2vec": "backend/model/wav2vec_mlp.pt"
}
