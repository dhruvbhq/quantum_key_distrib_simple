# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:36:15 2019

File containing the instantiation
of the noiseless QKD experiment class,
and executing the experiment.

@author: DHRUV BHATNAGAR
"""
import qkd_bb84_base as bb
import qkd_experiment_base as expt
      
def main():
    
    SIZE_TX = 500
    e1 = expt.qkd_experiment(SIZE_TX)
    e1.execute()    

if __name__ == '__main__':
    main()
