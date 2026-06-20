import torch
import torch.nn as nn
import torch.nn.functional as F


class NILMLSTM(nn.Module):

    def __init__(self, input_size, hidden_size=64):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            batch_first=True
        )

        self.attention = nn.Linear(hidden_size, 1)

        self.fc = nn.Linear(hidden_size, 9)

    def forward(self, x):

        out, _ = self.lstm(x)

        # attention weights over time
        attn_weights = torch.softmax(
            self.attention(out),
            dim=1
        )

        # weighted sum of all timesteps
        context = torch.sum(attn_weights * out, dim=1)

        return self.fc(context)