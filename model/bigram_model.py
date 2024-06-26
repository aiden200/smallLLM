import torch
import torch.nn as nn
import torch.nn.functional as F
from src.transformer_blocks import PositionalEncoding, Transformer_block


class BigramModel(nn.Module):    
    def __init__(self, vocab_size, embed_size, block_size, attention_heads, dropout, device):
        super().__init__()

        self.block_size = block_size  # block size is maximum length
        self.device = device
        self.token_embedding_table = nn.Embedding(vocab_size, embed_size)
        # for each char, add positional encoding to embed
        self.pe = PositionalEncoding(embed_size)
        self.tb = Transformer_block(embed_size, block_size, attention_heads, dropout, device)
        self.lm_head = nn.Linear(embed_size, vocab_size)

    def forward(self, idx, targets=None):
        # Embedding
        tok_embeddings = self.token_embedding_table(
            idx)  # (B, T, E) T here is the block_size

        # Positional Encoding
        # (T, E), B gets broadcasted from pe + x
        x = self.pe(tok_embeddings)

        x = self.tb(x)

        logits = self.lm_head(x)  # (B, T, V)

        # C is vocab size
        B, T, C = logits.shape

        if targets == None:
            loss = None
        else:
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)

            loss = F.cross_entropy(logits, targets)

            logits = logits.view(B, T, C)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            # predictions

            # don't let it go over max length
            idx_trimmed = idx[:, -self.block_size:]

            logits, loss = self(idx_trimmed)

            last_char_logits = logits[:, -1, :]  # last character

            # Probabilities across all chars
            probs = F.softmax(last_char_logits, dim=1)

            # (B,1) Not the highest prob but sample from probabilities
            idx_next = torch.multinomial(probs, num_samples=1)

            # We add to the time (B, T +1)
            idx = torch.cat((idx, idx_next), dim=1)

        return idx  # We return (B, T + max_new_tokens)


