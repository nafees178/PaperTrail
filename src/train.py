import torch
import torch.nn as nn
import torch.optim as optim
import hydra
from omegaconf import DictConfig, OmegaConf
import wandb

from dataset import get_dataloaders
from model import MNISTNet
from utils import (set_seed,count_parameters,print_model_summary)


def train(model, train_loader, criterion, optimizer, device):
    model.train()

    running_loss = 0.0

    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    return running_loss / len(train_loader)


def test(model, test_loader, device):
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            predictions = torch.argmax(outputs, dim=1)

            correct += (predictions == labels).sum().item()
            total += labels.size(0)

    accuracy = 100 * correct / total

    return accuracy

def run_experiment(cfg):
    set_seed(cfg.seed)
    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print(f"Using device: {device}")

    wandb.init(
        project="digitsRecognizer",
        config=OmegaConf.to_container(
            cfg,
            resolve=True,
            throw_on_missing=True,
        ),
    )

    train_loader, test_loader = get_dataloaders(
        batch_size=cfg.training.batch_size
    )

    model = MNISTNet(cfg.model.conv1_channels, cfg.model.conv2_channels).to(device)
    num_params = count_parameters(model)

    print(f"Trainable Parameters: {num_params:,}")
    print_model_summary(model)

    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(
        model.parameters(),
        lr=cfg.training.learning_rate
    )
    accuracy = 0.0
    for epoch in range(cfg.training.epochs):

        train_loss = train(
            model,
            train_loader,
            criterion,
            optimizer,
            device,
        )

        test_accuracy = test(
            model,
            test_loader,
            device,
        )
        accuracy = test_accuracy

        print(
            f"Epoch [{epoch+1}/{cfg.training.epochs}] "
            f"| Loss: {train_loss:.4f} "
            f"| Test Accuracy: {test_accuracy:.2f}%"
            f"| Parameters: {num_params:,}"
        )

        wandb.log(
            {
                "Epoch": epoch + 1,
                "Train Loss": train_loss,
                "Test Accuracy": test_accuracy,
                "Parameters": num_params,
            }
        )
    wandb.finish()

    return accuracy, num_params

@hydra.main(version_base=None, config_path="../configs", config_name="config")
def main(cfg: DictConfig):
    accuracy, params = run_experiment(cfg)

    print(f"Final Accuracy: {accuracy:.2f}%")
    print(f"Final Parameters: {params:,}")

if __name__ == "__main__":
    main()