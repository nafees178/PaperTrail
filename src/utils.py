import random
import numpy as np
import torch
from torchinfo import summary


def count_parameters(model):
    return sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )


def print_model_summary(model):
    summary(
        model,
        input_size=(1, 1, 28, 28),
        col_names=(
            "input_size",
            "output_size",
            "num_params",
            "trainable",
        ),
    )

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)

    torch.manual_seed(seed)

    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False