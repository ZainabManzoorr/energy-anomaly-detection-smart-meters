import matplotlib.pyplot as plt


def plot_predictions(
        actual,
        predicted,
        appliance_name,
        n_points=500
):

    plt.figure(figsize=(12, 5))

    plt.plot(
        actual[:n_points],
        label="Actual"
    )

    plt.plot(
        predicted[:n_points],
        label="Predicted"
    )

    plt.title(
        f"{appliance_name} Prediction"
    )

    plt.xlabel("Time")

    plt.ylabel("Normalized Energy")

    plt.legend()

    plt.tight_layout()

    plt.show()