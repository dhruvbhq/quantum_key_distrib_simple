# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 12:42:18 2019

@author: DHRUV BHATNAGAR
"""

import qkd_bb84_base as bb
import qkd_experiment_base as expt
import numpy as np
import random

class noisy_alice_con(bb.alice_con):
    
    def __init__(self, s_length, P_H_FAIL):
        super().__init__(s_length)
        self.P_H_FAIL = P_H_FAIL
    
    def hadamard_alice(self, state_vec):
        k = 1.0/np.sqrt(2.0)
        H = np.array([[k,k],[k,(-1*k)]])
        I = np.array([[0.0,1.0],[1.0, 0.0]])
        p = np.random.uniform(0.0, 1.0)
        if(p <= self.P_H_FAIL):
            return np.matmul(I, state_vec)
        else:            
            return np.matmul(H, state_vec)

class noisy_bob_con(bb.bob_con):
    
    def __init__(self, s_length, P_H_FAIL):
        super().__init__(s_length)
        self.P_H_FAIL = P_H_FAIL
    
    def hadamard_bob(self, state_vec):
        k = 1.0/np.sqrt(2.0)
        H = np.array([[k,k],[k,(-1*k)]])
        I = np.array([[0.0,1.0],[1.0, 0.0]])
        p = np.random.uniform(0.0, 1.0)
        if(p <= self.P_H_FAIL):
            return np.matmul(I, state_vec)
        else:            
            return np.matmul(H, state_vec)

class noisy_q_channel(bb.q_channel):
    
    def corrupt_state(self):
        self.temp_st_mtx = self.st_mtx_in
        self.length = np.shape(self.temp_st_mtx[0])[0] 
        inj_error_rate = 0.15*(1 + np.random.uniform(-0.25,0.25))
        self.cor = random.sample(range(1,self.length), np.floor(inj_error_rate*self.length).astype(int))
        for i in self.cor:
            self.temp_st_mtx[0,i], self.temp_st_mtx[1,i] = self.temp_st_mtx[1,i], self.temp_st_mtx[0,i]
            # this is an X error. 
            
        self.out_st_mtx = self.temp_st_mtx        
        
class noisy_qkd_experiment(expt.qkd_experiment):
    
    def __init__(self, SIZE_TX, P_H_FAIL):
        super().__init__(SIZE_TX)
        self.P_H_FAIL = P_H_FAIL
    
    def build_phase(self):
        super().build_phase()
        q_c_n = noisy_q_channel()
        a0_n = noisy_alice_con(self.SIZE_TX, self.P_H_FAIL)
        b0_n = noisy_bob_con(self.SIZE_TX, self.P_H_FAIL)
        
        # Polymorphism!
        self.q_c = q_c_n
        self.a0 = a0_n
        self.b0 = b0_n
        
def main():
    
    SIZE_TX = 1000
    P_H_FAIL = 0.05
    e1 = noisy_qkd_experiment(SIZE_TX, P_H_FAIL)
    e1.execute()
    

if __name__ == '__main__':
    main()
