# models/ — CLAUDE.md

## Purpose

ML model implementations. Phase 3 target: Mini GPT.

All models are implemented as Python modules, not notebooks. Training runs locally on CPU/GPU.

---

## Phase 3 — Mini GPT

### Goal

Implement a minimal transformer language model from scratch using PyTorch.
This is a learning exercise in transformer architecture — not a production LLM.

### Why

The eventual platform (upsc-agent) will need to understand transformer internals for:
- fine-tuning domain-specific models
- building embedding pipelines
- understanding attention-based retrieval
- evaluating LLM outputs

### Location

```
models/mini-gpt/
```

### Components to Build

```
models/mini-gpt/
├── tokenizer.py          # character-level or BPE tokenizer
├── embeddings.py         # token + positional embeddings
├── attention.py          # scaled dot-product attention, multi-head attention
├── transformer.py        # transformer block (attention + FFN + layer norm)
├── model.py              # full GPT model assembly
├── train.py              # training loop with loss tracking
├── sample.py             # inference / text generation / sampling strategies
├── config.py             # model hyperparameters (n_layers, n_heads, d_model, etc.)
└── __init__.py
```

### Dataset

Start with **Tiny Shakespeare** — small, fits in memory, fast to train on CPU.

```bash
# Download
wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt -O datasets/tinyshakespeare.txt
```

### Implementation Order

1. `config.py` — define hyperparameters as a dataclass
2. `tokenizer.py` — character-level tokenizer (encode/decode)
3. `embeddings.py` — token embedding + positional embedding
4. `attention.py` — single-head attention → multi-head attention
5. `transformer.py` — transformer block with residual connections and layer norm
6. `model.py` — stack transformer blocks into GPT
7. `train.py` — training loop, cross-entropy loss, AdamW optimizer
8. `sample.py` — autoregressive text generation

### Target Config (CPU-trainable)

```python
n_layers    = 4
n_heads     = 4
d_model     = 128
d_ff        = 512
context_len = 64
vocab_size  = (character-level, ~65 for Shakespeare)
batch_size  = 32
lr          = 3e-4
```

### Run Training

```bash
PYTHONPATH=. .venv/bin/python models/mini-gpt/train.py
```

### Run Sampling

```bash
PYTHONPATH=. .venv/bin/python models/mini-gpt/sample.py --prompt "To be or not"
```

---

## Tests

```
tests/unit/models/mini-gpt/     # shape tests, forward pass, no GPU required
tests/integration/models/       # full train loop on tiny batch
```

Unit tests must pass on CPU without a dataset — use random tensors to verify tensor shapes and forward pass.

---

## Core Module Usage in Models

Use `core/` for logging and config where appropriate:

```python
from core.logging.logger import logger

logger.info("training_started", n_layers=config.n_layers, dataset="tinyshakespeare")
logger.info("epoch_complete", epoch=epoch, loss=loss.item())
```

Do not use `core/database` or `core/redis` inside model training — those are for services.

---

## Engineering Rules for models/

- No Jupyter notebooks — train scripts only
- All components must be individually importable and testable
- Forward pass must be verifiable with random tensors (unit test)
- Config is a dataclass, not scattered constants
- Log training progress via structlog, not print statements
- Save checkpoints to `datasets/` or a dedicated `checkpoints/` dir (gitignored)
