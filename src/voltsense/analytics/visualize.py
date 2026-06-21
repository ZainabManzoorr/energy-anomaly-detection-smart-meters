import matplotlib.pyplot as plt


class Visualizer:

    def plot_appliance_contribution(self, percentages):

        plt.figure(figsize=(10, 5))

        percentages.plot(kind="bar")

        plt.title("Appliance Energy Contribution")
        plt.ylabel("Percentage (%)")
        plt.tight_layout()

        plt.show()


    def plot_hourly_usage(self, hourly_usage):

        plt.figure(figsize=(10, 5))

        hourly_usage.sort_index().plot()

        plt.title("Hourly Energy Consumption Pattern")
        plt.xlabel("Hour")
        plt.ylabel("Average Usage")

        plt.tight_layout()
        plt.show()


    def plot_weekday_weekend(self, weekday, weekend):

        plt.figure(figsize=(6, 4))

        plt.bar(
            ["Weekday", "Weekend"],
            [weekday, weekend]
        )

        plt.title("Weekday vs Weekend Consumption")
        plt.ylabel("Average Usage")

        plt.tight_layout()
        plt.show()