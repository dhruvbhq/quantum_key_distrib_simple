# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 17:16:56 2019

BB84 QKD with Eavesdropping

@author: DHRUV BHATNAGAR
"""


import qkd_bb84_base as bb
import qkd_experiment_base as expt
import numpy as np
import random

class eve_q_channel(bb.q_channel):
    
    def corrupt_state(self):
        self.temp_st_mtx = self.st_mtx_in
        self.length = np.shape(self.temp_st_mtx[0])[0] 
        # Eve generates a random binary sequence
        # and according to the result, measures
        # the incoming qubits in the standard or 
        # the Hadamard basis, and returns the 
        # collapsed state
        
        self.basis_seq_e = np.random.randint(2, size=self.length)
        
        for i in range(self.length):
            st = self.temp_st_mtx[:,i]
            print("In Eve: input state: ", st)
            if(self.basis_seq_e[1] == 0):
                print("Measurement basis: 0/1")
            else:
                print("Measurement basis: +/-")
            if(self.basis_seq_e[1] == 0):
                res = self.meas_single_qubit_e(st)
                if(res==0):
                    self.temp_st_mtx[:,i] = np.array([1,0])
                    print("Returned state: ", self.temp_st_mtx[:,i])
                    print("---------------------------------------")
                else:
                    self.temp_st_mtx[:,i] = np.array([0,1])
                    print("Returned state: ", self.temp_st_mtx[:,i])
                    print("---------------------------------------")


                    
            else:
                st = self.hadamard_e(st)
                res = self.meas_single_qubit_e(st)
                if(res==0):
                    self.temp_st_mtx[:,i] = self.hadamard_e(np.array([1,0]))
                    print("Returned state: ", self.temp_st_mtx[:,i])
                    print("---------------------------------------")


                else:
                    self.temp_st_mtx[:,i] = self.hadamard_e(np.array([0,1]))
                    print("Returned state: ", self.temp_st_mtx[:,i])
                    print("---------------------------------------")

        self.out_st_mtx = self.temp_st_mtx
                
    
    def meas_single_qubit_e(self, state_vec):
        a = np.square(np.absolute(state_vec[0]))
        print("In Eve: probability of |0> or |+>", a)
        thres = 10**(-3)
        if(np.absolute(a-0) < thres):
            res = 1
        elif(np.absolute(a-1) < thres):
            res = 0
        elif(random.random() < a):
            res = 0
        else:
            res = 1
        return res        
            
    def hadamard_e(self, state_vec):
        k = 1.0/np.sqrt(2.0)
        H = np.array([[k,k],[k,(-1*k)]])
        return np.matmul(H, state_vec)
                
        
class eve_qkd_experiment(expt.qkd_experiment):
    
    def build_phase(self):
        super().build_phase()
        q_c_e = eve_q_channel()
        
        # Polymorphism!
        self.q_c = q_c_e

        
def main():
    
    SIZE_TX = 200

    e1 = eve_qkd_experiment(SIZE_TX)
    e1.execute()

if __name__ == '__main__':
    main()

