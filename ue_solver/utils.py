# coding: utf-8

"""
created on Mon Jun 13
@author: msheehan
"""
from __future__ import absolute_import, division, print_function
from future.builtins.misc import input
import os




def check_savepath(savepath):
    save_results = True
    if not os.path.exists(os.path.dirname(savepath)):
        try:
            os.makedirs(os.path.dirname(savepath))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    # if file exists            
    elif os.path.exists(savepath): 
        # ask if user wants to rewrite
        rewrite = input("The file '{}' already exists. Would you like to write over it? (y/n)"
                        .format(os.path.relpath(savepath)))
        if rewrite == 'n':
            save_results = False

    return save_results
    