# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 12:40:46 2019

File to define the basic, noiseless BB84 QKD experiment

@author: DHRUV BHATNAGAR
"""
import qkd_bb84_base as bb
import random


class qkd_experiment:
    
    def __init__(self, SIZE_TX):
        #SIZE_TX represents size of sequences taken by Alice (a.k.a. s_length)        
        self.SIZE_TX = SIZE_TX
        
    def build_phase(self):
        
        # instantiating the classes for Alice, Bob, classical and quantum channels
        self.a0 = bb.alice_con(self.SIZE_TX)
        self.b0 = bb.bob_con(self.SIZE_TX)
        self.c_c = bb.c_channel()       
        self.q_c = bb.q_channel()
        
    def run_phase(self):
        
        # Generating Alice's qubits, measuring them after transmitting to Bob
        self.a0.seq_init_alice()
        self.a0.generate_qubit_stream()
        
        self.q_c.get_state(self.a0.return_state())
        self.q_c.corrupt_state()

        self.b0.seq_init_bob()
        self.b0.obtain_state(self.q_c.put_state())
        self.b0.meas_qubit_stream_bob()
        
    def key_generation_phase(self):
       
        # Generating the key based on measurement basis used.
        self.c_c.get_basis_seq(self.b0.basis_seq_b)
        self.a0.key_gen_alice(self.c_c.put_basis_seq())
        self.a0.print_key_alice()
        self.c_c.ch_reset()
    
        self.c_c.get_basis_seq(self.a0.basis_seq_a)
        self.b0.key_gen_bob(self.c_c.put_basis_seq())
        self.b0.print_key_bob()
        self.c_c.ch_reset()
        
    def validation_phase(self):
    
        # key validation phase
        self.c_c.get_check_bits(self.b0.pre_key_check())
        self.key_efficiency, self.calc_perc_error = self.a0.key_check(self.c_c.put_check_bits())
        self.a0.print_rem_key_alice()
        self.b0.print_rem_key_bob()
        print("Key efficiency obtained is ", self.key_efficiency, "%")
        print("Qubit error-rate calculated by Alice is ", self.calc_perc_error, "%")
        
        self.c_c.ch_reset()
        
    def execute(self):

        # Executing the experiment in the correct order
        self.build_phase()
        self.run_phase()
        self.key_generation_phase()
        self.validation_phase()
