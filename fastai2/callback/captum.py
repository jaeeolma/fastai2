# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/73_callback.captum.ipynb (unless otherwise specified).

__all__ = ['CaptumCallback']

# Cell
import tempfile
from ..basics import *
from ..learner import Callback

# Cell
from captum.attr import IntegratedGradients
from captum.attr import visualization as viz
from matplotlib.colors import LinearSegmentedColormap

# Cell
class CaptumCallback(Callback):
    "Captum Callback for Resnet Interpretation"
    def __init__(self):
        pass

    def after_fit(self):
        self.integrated_gradients = IntegratedGradients(self.model)

    def visualize(self,inp_data,n_steps=200,cmap_name='custom blue',colors=None,N=256,methods=['original_image','heat_map'],signs=["all", "positive"],outlier_perc=1):
        dl = self.dls.test_dl([inp_data],with_labels=True, bs=1)
        self.enc_inp,self.enc_preds= dl.one_batch()
        dec_data=dl.decode((self.enc_inp,self.enc_preds))
        self.dec_img,self.dec_pred=dec_data[0][0],dec_data[1][0]
        self.colors = [(0, '#ffffff'),(0.25, '#000000'),(1, '#000000')] if colors is None else colors
        self.attributions_ig = self.integrated_gradients.attribute(self.enc_inp.to(self.dl.device), target=self.enc_preds, n_steps=200)
        default_cmap = LinearSegmentedColormap.from_list(cmap_name,
                                                 self.colors, N=N)
        _ = viz.visualize_image_attr_multiple(np.transpose(self.attributions_ig.squeeze().cpu().detach().numpy(), (1,2,0)),
                             np.transpose(self.dec_img.numpy(), (1,2,0)),
                             methods=methods,
                             cmap=default_cmap,
                             show_colorbar=True,
                             signs=signs,
                             outlier_perc=outlier_perc, titles=[f'Original Image - ({self.dec_pred})', 'IG'])