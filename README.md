# quantum_key_distrib_simple
## Project Title: Simulation of BB84 Quantum Key Distribution protocol using Python, in noiseless, noisy and eavesdropping cases. 
### Author: Dhruv Bhatnagar.

### File guide:
A) Files needed for noiseless QKD experiment:

A.1) qkd_bb84_base.py

A.2) qkd_experiment_base.py 

A.3) qkd_bb84_noiseless.py (contains main())

B) Files needed for noise model:
B.1) All files in A)

B.2) qkd_noise_model.py (contains main())

C) Eavesdropping
C.1) All files in A)

C.2) qkd_eavesdropping_2.py (contains main())

Sample output transcripts of the programs have also been uploaded for noiseless/noisy/eavesdropping cases.

### Brief summary:
1. This program simulates BB84 QKD using several classes for Alice, Bob, classical and quantum channels.
2. The basic experiment is noiseless, but existing base classes can be easily overridden (OOP) to implement custom noise models/eavesdropping.
3. The functionality to validate the key by comparing the first half of the key for bit errors has been implemented.
4. Measurement outcomes are implemented using numpy's random number generation.
5. Detailed transcripts print a summary of the results of the experiment.

### Overview of the code/classes:

#### qkd_bb84_base.py contains: 
-> class for ALice (alice_con) 

--> with relevant data attributes to store qubit states/key 

--> methods/functions to encode/measure qubits

--> key generation based on Bob's bases

--> method to apply hadamard quantum gate

-> class for Bob (bob_con) 

--> methods to obtain qubits transmitted by alice via the quantum channel

--> bases set generation (for measurement)

--> performing measurements using numpy's random number generating functions

--> method to apply Hadamard quantum gate

--> method to generate the key from qubits received from Alice via quantum channel

-> class for Quantum Channel (q_channel)

--> methods to get the quamtum state, corrupt it according to a desired noise model, and return the quantum state. 

--> (in the basic noiseless case, state corruption is just an identity).

-> class for Classical Channel (c_channel)

--> for sharing classical bits of measurement bases/part of key bits for validation.

#### qkd_experiment_base.py contains:
-> class for basic QKD experiment:

--> utilising objects of classes Bob, Alice, classical and quantum channels.

--> the experiment is divided into modular phases to build the objects,
    running the experiment for transmitting qubits from Alice to Bob, 
    key generation phase based on bases used by Alice and Bob;
    method to find the error rate in the generated key.
    
--> An execute function to execute the complete experiment.


#### qkd_bb84_noiseless.py contains:
-> execution of noiseless exeriment for 500 qubits transmitted by Alice. 

-> qubit error rate is 0 %; a transcript is generated.

#### qkd_noise_model.py contains:
-> Overridden classes for Alice and Bob having Hadamard gates with a failure rate.

-> Overridden class for (noisy) quantum channel, the noisy quantum channel randomly corrupts qubits by an X error.

-> The noisy_qkd_experiment class is suitably overriden (only where necessary) to implement this noisy experiment for 1000 qubits.

-> A transcript is generated.

#### qkd_eavesdropping_2.py contanins:
-> An eavesdropper's class (Eve) extended from the noiseless quantum channel

--> The eavesdropper demonstrated is capable of generating a basis set (either the standard basis or the Hadamard basis), and carrying out measurements of qubits transmitted by Alice

--> The eavesdropper returns collapsed states resulting from measurement to Bob.

--> The QKD experiment class is suitably extended to accommodate eavesdropping classes.

--> Executed for 200 qubits

--> A detailed transcript is generated.
