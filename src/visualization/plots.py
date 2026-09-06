import matplotlib.pyplot as plt

def save_bar(series, title, xlabel, ylabel, path):
    fig,ax=plt.subplots(figsize=(8,5))
    series.plot(kind='bar',ax=ax)
    ax.set_title(title); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    fig.tight_layout(); fig.savefig(path,dpi=160); plt.close(fig)
