# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/43_tabular.learner.ipynb (unless otherwise specified).

__all__ = ['TabularLearner', 'tabular_learner']

# Cell
from ..basics import *
from .core import *
from .model import *

# Cell
class TabularLearner(Learner):
    "`Learner` for tabular data"
    def predict(self, row):
        tst_to = self.dls.valid_ds.new(pd.DataFrame(row).T)
        tst_to.process()
        tst_to.conts = tst_to.conts.astype(np.float32)
        dl = self.dls.valid.new(tst_to)
        inp,preds,_,dec_preds = self.get_preds(dl=dl, with_input=True, with_decoded=True)
        i = getattr(self.dls, 'n_inp', -1)
        b = (*tuplify(inp),*tuplify(dec_preds))
        full_dec = self.dls.decode((*tuplify(inp),*tuplify(dec_preds)))
        return full_dec,dec_preds[0],preds[0]

# Cell
@delegates(Learner.__init__)
def tabular_learner(dls, layers=None, emb_szs=None, config=None, n_out=None, y_range=None, **kwargs):
    "Get a `Learner` using `dls`, with `metrics`, including a `TabularModel` created using the remaining params."
    if config is None: config = tabular_config()
    if layers is None: layers = [200,100]
    to = dls.train_ds
    emb_szs = get_emb_sz(dls.train_ds, {} if emb_szs is None else emb_szs)
    if n_out is None: n_out = get_c(dls)
    assert n_out, "`n_out` is not defined, and could not be infered from data, set `dls.c` or pass `n_out`"
    model = TabularModel(emb_szs, len(dls.cont_names), n_out, layers, **config)
    return TabularLearner(dls, model, **kwargs)

# Cell
@typedispatch
def show_results(x:Tabular, y:Tabular, samples, outs, ctxs=None, max_n=10, **kwargs):
    df = x.all_cols[:max_n]
    for n in x.y_names: df[n+'_pred'] = y[n][:max_n].values
    display_df(df)