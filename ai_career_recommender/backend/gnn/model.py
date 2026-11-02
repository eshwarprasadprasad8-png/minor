import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

class GraphSAGEModel(nn.Module):
    def __init__(self, in_channels=64, hidden_channels=48, out_channels=32, dropout=0.1):
        super(GraphSAGEModel, self).__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)
        self.dropout = dropout

    def forward(self, x, edge_index):
        # Layer 1
        h = self.conv1(x, edge_index)
        h = F.relu(h)
        h = F.dropout(h, p=self.dropout, training=self.training)
        
        # Layer 2 - 32-dim inductive embedding
        out = self.conv2(h, edge_index)
        # L2 normalize embeddings
        out = F.normalize(out, p=2, dim=-1)
        return out

    def decode(self, z, edge_label_index):
        # Link prediction dot product
        src, dst = edge_label_index
        return (z[src] * z[dst]).sum(dim=-1)

