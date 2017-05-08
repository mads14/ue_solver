# coding: utf-8

"""
created on Mon Jun 13
@author: msheehan
"""
from __future__ import absolute_import, division, print_function
from future.builtins.misc import input
import os




def check_savepath(savepath):
    if not os.path.exists(os.path.dirname(savepath)):
        try:
            os.makedirs(os.path.dirname(savepath))
            save_res = True
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    # if directory exists            
    else: 
        # ask if user wants to rewrite
        rewrite = input("The file '{}' already exists. Would you like to write over it? (y/n)"
                        .format(os.path.relpath(savepath)))
        if rewrite == 'n':
            save_res = False
        else:
        	save_res = True
    return save_res
    