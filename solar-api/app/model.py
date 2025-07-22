# app/model.py
import torch
import torch.nn as nn
import joblib

class PatchTST(nn.Module):
    def __init__(self, input_dim=4, patch_size=12, d_model=64, n_heads=2, num_layers=2, output_len=24):
        super(PatchTST, self).__init__()
        self.patch_size = patch_size
        self.output_len = output_len
        self.embedding = nn.Linear(patch_size * input_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=n_heads)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.output_layer = nn.Linear(d_model, output_len)

    def forward(self, x):
        B, T, D = x.shape
        num_patches = T // self.patch_size
        x = x[:, :num_patches * self.patch_size, :]
        x = x.reshape(B, num_patches, self.patch_size * D)
        x = self.embedding(x)
        x = self.transformer(x)
        x = self.output_layer(x)
        return x.mean(dim=1)

def load_model_and_scaler():
    model = PatchTST()
    model.load_state_dict(torch.load("saved/model.pth", map_location="cpu"))
    model.eval()

    scaler = joblib.load("saved/scaler.pkl")

    return model, scaler
