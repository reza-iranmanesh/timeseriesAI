# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/008_learner.ipynb (unless otherwise specified).

__all__ = ['load_learner_all']

# Cell
from fastai2.learner import *
from .imports import *

# Cell
@patch
def save_all(self:Learner, path='export', dls_fname='dls', model_fname='model', learner_fname='learner'):

    path = Path(path)
    if not os.path.exists(path): os.makedirs(path)

    # Save the dls
    torch.save(self.dls, path/f'{dls_fname}.pth')

    # Saves the model along with optimizer
    self.model_dir = path
    self.save(model_fname)

    # Export learn without the items and the optimizer state for inference
    self.export(path/f'{learner_fname}.pkl')

    print(f'Learner saved:')
    print(f"path          = '{path}'")
    print(f"dls_fname     = '{dls_fname}'")
    print(f"model_fname   = '{model_fname}.pth'")
    print(f"learner_fname = '{learner_fname}.pkl'")


def load_learner_all(path='export', dls_fname='dls', model_fname='model', learner_fname='learner', cpu=True):
    path = Path(path)
    learn = load_learner(path/f'{learner_fname}.pkl', cpu=cpu)
    learn.load(f'{model_fname}')
    dls = torch.load(path/f'{dls_fname}.pth')
    learn.dls = dls
    return learn

# Cell
@patch
@delegates(subplots)
def plot_metrics(self: Recorder, nrows=None, ncols=None, figsize=None, **kwargs):
    metrics = np.stack(self.values)
    names = self.metric_names[1:-1]
    n = len(names) - 1
    if nrows is None and ncols is None:
        nrows = int(math.sqrt(n))
        ncols = int(np.ceil(n / nrows))
    elif nrows is None: nrows = int(np.ceil(n / ncols))
    elif ncols is None: ncols = int(np.ceil(n / nrows))
    figsize = figsize or (ncols * 6, nrows * 4)
    fig, axs = subplots(nrows, ncols, figsize=figsize, **kwargs)
    axs = [ax if i < n else ax.set_axis_off() for i, ax in enumerate(axs.flatten())][:n]
    for i, (name, ax) in enumerate(zip(names, [axs[0]] + axs)):
        ax.plot(metrics[:, i], color='#1f77b4' if i == 0 else '#ff7f0e', label='valid' if i > 0 else 'train')
        ax.set_title(name if i > 1 else 'losses')
        ax.legend(loc='best')
    plt.show()