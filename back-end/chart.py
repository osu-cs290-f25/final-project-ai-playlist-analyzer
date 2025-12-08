def generate_mood_chart(playlist_id: int, playlist: dict, percentages: dict, static_dir: str = "static") -> str:
    import matplotlib.pyplot as plt
    import os

    # Directory to store charts
    mood_chart_imgs_dir = "mood_chart"  
    save_dir = os.path.join(static_dir, mood_chart_imgs_dir)

    # Make sure the folder exists
    os.makedirs(save_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 6))

    # Pie chart
    wedges, texts = ax.pie(
        percentages.values(),
        startangle=90,
        colors=plt.cm.Pastel1(range(len(percentages)))
    )

    # Legend labels with % values
    legend_labels = [f"{mood} ({value:.1f}%)" for mood, value in percentages.items()]

    ax.legend(
        wedges,
        legend_labels,
        title="Moods",
        loc="lower center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=2
    )

    ax.set_title("Correlated Moods", fontsize=16, fontweight="bold")

    # File output
    filename = f"chart_{playlist_id}.png"
    filepath = os.path.join(save_dir, filename)

    plt.tight_layout()
    plt.savefig(filepath)
    plt.close(fig)

    # Return URL path for template
    return f"/static/{mood_chart_imgs_dir}/{filename}"
