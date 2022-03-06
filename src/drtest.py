"""Code here provide some useful tools for data processing, analysis and plotting.

Objects
-------
DataAnalysis

DataPlotting

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.animation as animation
import logging


DEBUG_LOG = True
STRM_LOG = True

logger = logging.getLogger('drtest_loggers')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


    
class DataAnalysis():
    """Provides useful tools for data analysis.
    
    Attributes
    ----------
    xdata : ndarray / array_like / list
        x axis data
    ydata : ndarray / array_like / list
    
    Methods
    -------
    data_reduction
        performs data reduction using several methods
    
    Layout
    ------
    I. Reduction tools
    
    II. Filters
    
    III. Analysis tools

    """
    def __init__(self, xdata:np.ndarray, ydata:np.ndarray) -> None:

        self.xdata = xdata
        self.ydata = ydata
    
    
    def data_reduction(self, method:str, reduction_factor:int) -> tuple:
            """Performs data reduction on xdata and ydata.

            Parameters
            ----------
            method : str
                specify the method performed for data reduction
                
                    Method I : 'decimate'
                        eliminates the last element in the subset i.e. the n-th element,
                        where n is the reduction factor value
                    Method II : 'average'
                        the resulting element represents an average of items in the set
                    Method III : 'max'
                        maximum value in set is retained  
                    Method IV :'min'
                        minimum value in set is retained                
                    Method V : 'min/max'
                        the min and max values in each successive set of n reduction points are retained

            reduction_factor : int
                describes the size of the subsets to which the data reduction method will be applied

            Returns
            -------
            tuple
                new x, y arrays, reduced with selected method

            Raises
            ------
            ValueError
                Raise if in 'min/max' method selected reduction factor is smaller than 2.
            ValueError
                Raise if method provided value is other than 'decimate', 'average', 'min', 'max', 'min/max'.
            TypeError
                Raise if specified method is not string type.
            """        
            if type(method) == str:
                
                # Method I: Decimate
                if method == 'decimate':
                    xreduced = self.xdata[::reduction_factor]
                    yreduced = self.ydata[::reduction_factor]
                    if STRM_LOG == True:
                        logger.info(f'Data was successfully reduced with the {method} method,' 
                                    + f'the new length of xarray and y array being {len(xreduced)}.')
                    return xreduced, yreduced

                # Method II: Substitute average
                elif method == 'average':
                    xsa = np.mean(self.xdata.reshape(-1, reduction_factor), axis=1)
                    ysa = np.mean(self.ydata.reshape(-1, reduction_factor), axis=1)
                    if STRM_LOG == True:
                        logger.info(f'Data was successfully reduced with the {method} method,'
                                    + f'the new length of xarray and y array being {len(xsa)}.')
                    return xsa, ysa
                
                # Method III: Minimum
                elif method == 'min':
                    xmin = np.amin(self.xdata.reshape(-1, reduction_factor), axis=1)
                    ymin = np.amin(self.ydata.reshape(-1, reduction_factor), axis=1)
                    if STRM_LOG == True:
                        logger.info(f'Data was successfully reduced with the {method} method,'
                                    + f'the new length of xarray and y array being {len(xmin)}.')
                    return xmin, ymin
                
                # Merhod IV: Maximum
                elif method == 'max':        
                    xmax = np.amax(self.xdata.reshape(-1, reduction_factor), axis=1)
                    ymax = np.amax(self.ydata.reshape(-1, reduction_factor), axis=1)
                    if STRM_LOG == True:
                        logger.info(f'Data was successfully reduced with the {method} method,'
                                    + f'the new length of xarray and y array being {len(xmax)}.')
                    return xmax, ymax
                
                # Method V: Min/Max
                elif method == 'min/max':
                    if reduction_factor >= 2:
                        xminvals = np.amin(self.xdata.reshape(-1, reduction_factor), axis=1)
                        xmaxvals = np.amax(self.xdata.reshape(-1, reduction_factor), axis=1)
                        yminvals = np.amin(self.ydata.reshape(-1, reduction_factor), axis=1)
                        ymaxvals = np.amax(self.ydata.reshape(-1, reduction_factor), axis=1)
        
                        xminmax = []
                        yminmax = []
                        for x, y in zip(xminvals, xmaxvals):
                            xminmax.append(x)
                            xminmax.append(y)
                        for m, n in zip(yminvals, ymaxvals):
                            yminmax.append(m)
                            yminmax.append(n)
                        if STRM_LOG == True:
                            logger.info(f'Data was successfully reduced with the {method} method,'
                                        + f'the new length of xarray and y array being {len(xminmax)}.')
                        return xminmax, yminmax
                    else:
                        # logging
                        if DEBUG_LOG == True:
                            logger.warning('In this method 2 values are kept. The reduction factor must be greater than 2.')
                        if STRM_LOG == True:
                            logger.info('In this method 2 values are kept. The reduction factor must be greater than 2.')
                        
                        raise ValueError("For this method the reduction factor must be greater than or equal to 2.")
                else:
                    raise ValueError("Available methods: 'deciamte', 'average', 'min', 'max', 'min/max'.")
            else:
                raise TypeError("Specified method has to be string type.")
            

class DataPlotting():
    """_summary_

    Parameters
    ----------
    DataAnalysis : class
        
    """


    def plot_multiple_methods(self, xdata:list, ydata:list, action:str, extension:str=None, rotation:bool=False):
        """_summary_

        Parameters
        ----------
        xdata : _type_
            _description_
        action : str
            _description_
        extension : str, optional
            _description_, by default None
        rotation : bool, optional
            _description_, by default False

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        TypeError
            _description_
        TypeError
            _description_
        ValueError
            _description_
        TypeError
            _description_
        """
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        zs = [round(i, 1) for i in range(0, 5)]
        
        for (xind, xarr), (yind, yarr) in zip(enumerate(xdata), enumerate(xdata)):
            ax.plot(xdata[xind], xdata[yind], zs[xind], zdir='y', color='black')
            
        ax.set_xlabel('Time (ms)', fontweight='bold', fontsize='medium')
        ax.set_zlabel('Voltage (mV)', fontweight='bold', fontsize='medium')
        
        if type(action) == str:
            if action == 'plot':
                    return plt.show()
            elif action == 'save':
                if type(extension) == str:
                    return plt.savefig(self.abf_file + extension)
                else:
                    raise TypeError("Specify figure extension.")
            elif action == 'save&plot':
                if type(extension) == str:
                    return plt.savefig(self.abf_file + extension), plt.show()
                else:
                    raise TypeError("Specify figure extension.")
            elif action != 'plot' and action != 'save' and action != 'save&plot':
                raise ValueError("Action can be 'plot', 'save' or 'save&plot'.")
        else:
            raise TypeError("Action was to be string type.")
        
                
    def plot_3D(self, action:str, extension:str=None, rotation:bool=False):
        """_summary_

        Parameters
        ----------
        action : str
            _description_
        extension : str, optional
            _description_, by default None
        rotation : bool, optional
            _description_, by default False

        Returns
        -------
        _type_
            _description_

        Raises
        ------
        TypeError
            _description_
        TypeError
            _description_
        ValueError
            _description_
        TypeError
            _description_
        """
        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        
        zs = [round(i, 1) for i in range(0, 5)]
    
        ax.plot(self.xdata, self.ydata, zs[3], zdir='y', color='black')
 
        ax.set_xlabel('Time (ms)', fontweight='bold', fontsize='medium')
        

        if type(action) == str:
            if action == 'plot':
                if rotation == True:
                    for angle in range(0, 360):
                        ax.view_init(25, angle)
                        plt.draw()
                        plt.pause(.001)
                else:
                    return plt.show()
            elif action == 'save':
                if type(extension) == str:
                    return plt.savefig(self.abf_file + extension)
                else:
                    raise TypeError("Specify figure extension.")
            elif action == 'save&plot':
                if type(extension) == str:
                    return plt.savefig(self.abf_file + extension), plt.show()
                else:
                    raise TypeError("Specify figure extension.")
            elif action != 'plot' and action != 'save' and action != 'save&plot':
                raise ValueError("Action can be 'plot', 'save' or 'save&plot'.")
        else:
            raise TypeError("Action was to be string type.")        
    
    
    
    
    
