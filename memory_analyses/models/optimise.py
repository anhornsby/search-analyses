"""Optimisers for model estimations"""

from scipy.optimize import minimize

class ScipyMinimiser(object):
    """
    Minimise a function using scipy.optimise

    :param optimiser_args: A dictionary of arguments to pass to the Scipy optimiser. See
        scipy.optimise.minimise for more information.
    """

    def __init__(self, optimiser_args):
        super(ScipyMinimiser, self).__init__()
        self.optimiser_args = optimiser_args

    def minimise(self, func, args):
        """Minimise a function using the scipy minimiser"""

        #  minimise that function
        res = minimize(func,
                       args=args,
                       **self.optimiser_args)

        return res
   
