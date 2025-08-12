# backend/model/architecture.py
import torch
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
    
    
class Wav2VecLSTMClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(768, 128, num_layers=2, batch_first=True, bidirectional=True)
        self.classifier = nn.Sequential(
            nn.Linear(128 * 2, 64),
            nn.ReLU(),
            nn.Linear(64, 1)  # no Sigmoid here
        )

    def forward(self, x):
        lengths = torch.tensor([x.shape[0]])
        x = x.unsqueeze(0)  # add batch
        packed = nn.utils.rnn.pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        _, (hn, _) = self.lstm(packed)
        final = torch.cat((hn[-2], hn[-1]), dim=1)
        return self.classifier(final).squeeze()



MODEL_PATHS = {
    "cnn": "backend/model/cnn_full.pt",
    "crnn": "backend/model/crnn_full.pt",
    "lstm": "backend/model/wav2vec_lstm_balanced.pt",
    "wav2vec": "backend/model/wav2vec_mlp.pt"
}
