import torch
import torch.nn as nn


class MNISTNet(nn.Module):
    def __init__(self, conv1_channels, conv2_channels):
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(1, conv1_channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(conv1_channels),
            nn.MaxPool2d(2),
            nn.Conv2d(conv1_channels, conv2_channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(conv2_channels),
            nn.MaxPool2d(2),
        )

        self.flatten = nn.Flatten()

        self.classifier = nn.Linear(conv2_channels * 7 * 7, 10)

    def forward(self, x):
        x = self.features(x)
        x = self.flatten(x)
        x = self.classifier(x)
        return x

