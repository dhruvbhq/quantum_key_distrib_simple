# -*- coding: utf-8 -*-
"""

Project Title: 
-----------------------------------------------------------
Simulation of BB84 Quantum Key distribution protocol using
object oriented programming
-----------------------------------------------------------
This file contains class and method definitions
for basic, noiseless BB84 QKD.
This file can be imported to another file
in the same directory.
-----------------------------------------------------------
@author: DHRUV BHATNAGAR
-----------------------------------------------------------
"""

#Import necessary libraries
import numpy as np
import random

class alice_con:
    
    def __init__(self, s_length):
        self.s_length = s_length
        self.state_matrix = np.zeros((2,self.s_length))
        self.key_arr = np.empty(1)
        
    def seq_init_alice(self):
        self.basis_seq_a = np.random.randint(low = 0, high = 2, size = self.s_length)
        self.states_seq_a = np.random.randint(low = 0, high = 2, size = self.s_length)
        
    def generate_qubit_stream(self):
        for i in range(self.s_length):
            basis = self.basis_seq_a[i]
            state = self.states_seq_a[i]
            #print("\n basis = ", basis, "\n state = ", state)
            ket0 = np.array([1.0, 0.0])
            ket1 = np.array([0.0, 1.0])
            k = 1.0/np.sqrt(2.0)
            H = np.array([[k,k],[k,(-1*k)]])           
            
            if(basis == 0 and state == 0):
                self.state_matrix[:,i] = ket0 
            elif(basis == 0 and state == 1):
                self.state_matrix[:,i] = ket1
            elif(basis == 1 and state == 0):
                self.state_matrix[:,i] = self.hadamard_alice(ket0)
            else:
                self.state_matrix[:,i] = self.hadamard_alice(ket1)
    
    def hadamard_alice(self, state_vec):
        k = 1.0/np.sqrt(2.0)
        H = np.array([[k,k],[k,(-1*k)]])
        return np.matmul(H, state_vec)     
    
    def key_gen_alice(self, bob_basis_seq):
        self.temp_key_arr = np.zeros(self.s_length)
        self.size_of_key = 0
        for i in range(self.s_length):
            if(self.basis_seq_a[i] == bob_basis_seq[i]):
                self.size_of_key += 1
                self.temp_key_arr[i] = self.states_seq_a[i]
        self.key_arr = self.temp_key_arr[:self.size_of_key].astype(int)
                
    def print_key_alice(self):
        print("Alice's full key ")
        for i in range(self.size_of_key):
            print(self.key_arr[i].astype(int), end='')
        print("\n Size of Alice's (full) key is: ", self.size_of_key+1)
        
    def key_check(self, check_bits_bob):
        self.size_of_check_bits = np.size(check_bits_bob)
        self.check_bits_alice = self.key_arr[:self.size_of_check_bits].astype(int)
        self.rem_key_alice = self.key_arr[self.size_of_check_bits:].astype(int)
        self.errors = 0        
        for i in range(self.size_of_check_bits):
            if(check_bits_bob[i] != self.check_bits_alice[i]):
                self.errors += 1
                print("Error detected in keys. Bob's bit: ", check_bits_bob[i], "Alice's bit: ", self.check_bits_alice[i], "No. of errors detected: ", self.errors)
        self.percent_error_rate = 100*(self.errors)/(self.size_of_check_bits)
        self.key_efficiency = 100.00*(self.size_of_key+1)/(self.s_length)
        print("Places in which check bits differ: ", np.bitwise_xor(self.check_bits_alice, check_bits_bob))
        return self.key_efficiency, self.percent_error_rate
        
    def print_rem_key_alice(self):
        print("Alice's remaining key is: ")
        for i in range(np.size(self.rem_key_alice)):
            print(self.rem_key_alice[i], end='')
        print("\n Size of Alice's remaining key is: ", np.size(self.rem_key_alice))
                
    def print_alice_info(self):
        print("stream length: ", self.s_length)
        print("bases random sequence: ", self.basis_seq_a)
        print("state random sequence: ", self.states_seq_a)
        print("\n")
        #print("\n state_matrix: ", self.state_matrix)
        
    def return_state(self):
        return self.state_matrix
        
class bob_con:
    
    def __init__(self, s_length):
        self.s_length = s_length
        self.size_of_key = 0     
        self.key_arr = np.empty(1)
        
    def obtain_state(self, state_matrix):
        self.state_matrix = state_matrix
        
    def seq_init_bob(self):
        self.basis_seq_b = np.random.randint(low = 0, high = 2, size = self.s_length)
        self.meas_seq_b = np.zeros(self.s_length)
        self.temp_meas_seq_b = np.zeros(self.s_length)
        
    def meas_qubit_stream_bob(self):
        for j in range(self.s_length):
            st = self.state_matrix[:,j]
            if(self.basis_seq_b[j] == 0):
                self.temp_meas_seq_b[j] = self.meas_single_qubit_bob(st)
            else:
                st = self.hadamard_bob(st)
                self.temp_meas_seq_b[j] = self.meas_single_qubit_bob(st)
        self.meas_seq_b = self.temp_meas_seq_b.astype(int)
                
        #return self.meas_seq_b.astype(int)
    
    def meas_single_qubit_bob(self, state_vec):
        a = np.square(np.absolute(state_vec[0]))
        thres = 10**(-3)
        if(np.absolute(a-0) < thres):
            res = 1
        elif(np.absolute(a-1) < thres):
            res = 0
        elif(np.random.uniform() < a):
            res = 0
        else:
            res = 1
        #print("values of a: ", a)
        return res
    
    def hadamard_bob(self, state_vec):
        k = 1.0/np.sqrt(2.0)
        H = np.array([[k,k],[k,(-1*k)]])
        return np.matmul(H, state_vec)
        
    def key_gen_bob(self, alice_basis_seq):
        self.temp_key_arr = np.zeros(self.s_length)
        for i in range(self.s_length):
            if(self.basis_seq_b[i] == alice_basis_seq[i]):
                self.size_of_key += 1
                self.temp_key_arr[i] = self.meas_seq_b[i]
        self.key_arr = self.temp_key_arr[:self.size_of_key].astype(int)

    def print_key_bob(self):
        print("Bob's full key ")
        for i in range(self.size_of_key):
            print(self.key_arr[i].astype(int), end='')
        print("\n Size of Bob's (full) key is: ", self.size_of_key+1)
        
    def pre_key_check(self):
        self.size_of_check_bits = np.ceil((self.size_of_key-1)/2).astype(int)
        self.check_bits = self.key_arr[:self.size_of_check_bits].astype(int)
        self.rem_key_bob = self.key_arr[self.size_of_check_bits:].astype(int)
        return self.check_bits
    
    def print_rem_key_bob(self):
        print("Bob's remaining key is: ")
        for i in range(np.size(self.rem_key_bob)):
            print(self.rem_key_bob[i], end='')
        print("\n Size of Bob's remaining key is: ", np.size(self.rem_key_bob))
        
class q_channel:
    
    # So that Alice can transmit qubits to Bob.
    def get_state(self, st_mtx):
        self.st_mtx_in = st_mtx
        
    def corrupt_state(self):
        self.temp_st_mtx = self.st_mtx_in
        # for now, the identity
        self.out_st_mtx = self.temp_st_mtx
    
    def put_state(self):
        return self.out_st_mtx
        
class c_channel:
    #so that Alice and Bob can publicly share bases sequences
    def get_basis_seq(self, basis_seq):
        self.basis_seq = basis_seq
        
    def put_basis_seq(self):
        return self.basis_seq
        
    #and so that they can validate their key
        
    def get_check_bits(self, check_bits):
        self.check_bits = check_bits
    
    def put_check_bits(self):
        return self.check_bits
    
    def ch_reset(self):
        self.basis_seq = []
        self.check_bits = []
    
