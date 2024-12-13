import matplotlib.pyplot as plt
import random

def plot_success_rate(results):
    """
    Plot a pie chart for success/failure rate.
    """
    successes = results.count(0)
    failures = len(results) - successes
    labels = ['Success', 'Failure']
    sizes = [successes, failures]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#F44336'])
    plt.title("Success Rate")
    plt.savefig("success_rate_pie_chart.png")
    plt.show()


if __name__ == "__main__":
    success = []
    for i in range(1000):
        r = random.randint(1, 100)
        if r <= 41:
            success.append(0)
        else:
            success.append(1)

    plot_success_rate(success)
