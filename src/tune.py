import hydra
import optuna

from copy import deepcopy
from omegaconf import DictConfig

from train import run_experiment


def objective(trial, cfg):

    cfg = deepcopy(cfg)

    cfg.training.learning_rate = trial.suggest_float(
        "learning_rate",
        1e-4,
        1e-2,
        log=True,
    )

    cfg.training.batch_size = trial.suggest_categorical(
        "batch_size",
        [32, 64, 128],
    )

    cfg.model.conv1_channels = trial.suggest_categorical(
        "conv1_channels",
        [4, 8, 12],
    )

    cfg.model.conv2_channels = trial.suggest_categorical(
        "conv2_channels",
        [8, 12, 16],
    )

    accuracy, params = run_experiment(cfg)

    if params > 10000:
        raise optuna.TrialPruned(
            "Parameter limit exceeded."
        )

    return accuracy


@hydra.main(
    version_base=None,
    config_path="../configs",
    config_name="config",
)
def main(cfg: DictConfig):

    study = optuna.create_study(
        direction="maximize"
    )

    study.optimize(
        lambda trial: objective(trial, cfg),
        n_trials=20,
    )

    print("=" * 40)
    print("BEST RESULT")
    print("=" * 40)

    print(f"Best Accuracy : {study.best_value:.2f}%")

    print()

    print("Best Parameters")

    for key, value in study.best_params.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()