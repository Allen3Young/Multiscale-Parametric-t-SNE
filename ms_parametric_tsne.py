import numpy as np
from tqdm import tqdm
from parametric_tsne import ParametricTSNE, x2p


class MultiscaleParametricTSNE(ParametricTSNE):
    
    def __init__(self, n_components=2,
                n_iter=1000,
                early_exaggeration_epochs = 50,
                early_exaggeration_value = 4.,
                early_stopping_epochs = np.inf,
                early_stopping_min_improvement = 1e-2,
                nl1 = 500,
                nl2 = 500,
                nl3 = 2000,
                logdir=None, verbose=0):

        # Fake perplexity init.
        super().__init__(n_components=n_components,
                         perplexity=-1.0,       # !!!
                         n_iter=n_iter,
                         early_exaggeration_epochs=early_exaggeration_epochs,
                         early_exaggeration_value=early_exaggeration_value,
                         early_stopping_epochs=early_stopping_epochs,
                         early_stopping_min_improvement=early_stopping_min_improvement,
                         nl1 = nl1,
                         nl2 = nl2,
                         nl3 = nl3,
                         logdir=logdir, verbose=verbose)
    
    def _calculate_P(self, X, perplexity):
        # Compute multi-scale Gaussian similarities with exponentially growing perplexities
        N = X.shape[0]
        H = np.rint(np.log2(N/2))
        P = np.zeros((N, N))
        for h in tqdm(np.arange(1, H+1)):
            # Compute current perplexity P_ij
            perplexity = 2**h
            _P = x2p(X, perplexity)
            
            # make symmetric and normalize
            _P += _P.T
            _P /= 2
            _P = np.maximum(_P, 1e-8)

            P += _P
        
        return P/H      # Average across perplexities