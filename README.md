# README

# High Accuracy Vehicle Dynamic Model

This repository provides a **high-accuracy vehicle dynamic model** based on a 3-DOF vehicle body model (longitudinal, lateral, and yaw dynamics) and a **high-fidelity tire model**, validated to produce results **nearly identical to Carsim** under the same specifications.

The model is built in Simulink and compiled into a shared library (`libmycontroller.dylib`). It supports both conventional vehicle control and advanced drift control applications. Python wrapper classes and test scripts are included, enabling seamless interaction with the model through Python. This makes it particularly suitable for reinforcement learning experiments, control algorithm development, or other research scenarios.

**The model's responses have been rigorously tested by the authors’ team, demonstrating almost identical results to Carsim for vehicles of matching specifications.**

> Note: A future update will add support for custom vehicle parameters and adjustable road-friction coefficients to further enhance model fidelity.
> 

---

## Project Structure

- **`libmycontroller.dylib`**
    
    The compiled shared library produced by Simulink Coder. It implements all the core vehicle dynamics. MacOS `.dylib` is shown here; on other systems, you might have `.so` (Linux) or `.dll` (Windows).
    
- **`vehiclemodel_public_wrapper.py`**
    
    A Python wrapper class (`VehicleModelPublic`) that loads and calls the functions from `libmycontroller.dylib`. It provides:
    
    - **`initial(sped, delta, v_ini)`**: Initializes the model and sets initial inputs.
    - **`step(sped, delta)`**: Steps the simulation by one time increment, returning updated vehicle states.
    - **`terminate()`**: Terminates the model, releasing any resources.
- **`test_vehiclemodel_public.py`**
    
    A demonstration script showing how to instantiate `VehicleModelPublic` and call its methods. By running this script, you can observe the vehicle states (`X, Y, yaw, Vx, Vy, r`) updating over multiple simulation steps.
    

---

## Inputs and Outputs

### Inputs

1. **`sped`**
    - Represents throttle/brake input.
    - **Positive**: throttle depth.
    - **Negative**: brake depth.
    - **Recommended range**: , but values outside this range are permissible.
        
        −1,1-1, 1
        
2. **`delta`**
    - Represents the front wheel steering angle, in **radians**.
    - Positive values typically correspond to turning left or right, depending on your coordinate convention.
3. **`V_ini`**
    - Represents the initial velocity. In many reinforcement learning applications, you can treat this as the starting speed of the vehicle.

### Outputs

The model outputs six state variables after each step:

- **`X`** : Vehicle’s global position.
    
    xx
    
- **`Y`** : Vehicle’s global position.
    
    yy
    
- **`yaw`** : Vehicle’s yaw angle (orientation).
- **`Vx`** : Longitudinal velocity in the vehicle frame.
- **`Vy`** : Lateral velocity in the vehicle frame.
- **`r`** : Yaw rate  in radians per second.
    
    ψ˙\dot{\psi}
    

---

## Quick Start

1. **Install prerequisites**
    
    Make sure you have Python 3.x installed. If you are on Mac, place `libmycontroller.dylib` in the same directory or in a location discoverable by the operating system’s dynamic linker.
    
2. **Run the test script**
    
    ```bash
    python test_vehiclemodel_public.py
    
    ```
    
    You should see console outputs showing the evolving vehicle states.
    
3. **Customize**
    - Modify the initial values (`sped`, `delta`, `V_ini`) in `test_vehiclemodel_public.py` to experiment with different inputs.
    - Integrate the Python class in your RL environment by importing `vehiclemodel_public_wrapper`.

---

## Future Developments

- **Adjustable Vehicle Parameters**: In a future release, the model will allow specifying vehicle mass, wheelbase, tire parameters, etc.
- **Road Surface Variations**: We plan to add functionality to adjust road friction coefficients, enabling more realistic driving scenarios across diverse surfaces.

---

## Citation

If you use this model in your research or applications, please consider citing the following paper:

> S. Zhao, J. Zhang, C. He, X. Hou and H. Huang, ["Adaptive Drift Control of Autonomous Electric Vehicles After Brake System Failures,"](https://ieeexplore.ieee.org/abstract/document/10195855) in IEEE Transactions on Industrial Electronics, vol. 71, no. 6, pp. 6041-6052, June 2024, doi: 10.1109/TIE.2023.3294594.
> 

Thank you for supporting our work!

## Usage Restriction and Declaration

1. **Reciprocal Open-Source License**
    
    This software is licensed under a reciprocal open-source agreement. Any user of this software **must** open-source their own program that utilizes it.
    
2. **Attribution**
    
    The original author of this software is **Shiyue** **Sean Zhao**. Proper attribution should be given in any use of this software, including (but not limited to) research papers, software projects, or demonstrations.
    

By using this software, you agree to these terms.

---

## Contact

If you have questions or run into any issues:

- Feel free to open a GitHub issue (if hosted on GitHub).
- Or reach out to the author(s) via the contact information in this repository (if provided).

We welcome contributions and feedback to help improve this High Accuracy Vehicle Dynamic Model. Enjoy exploring the dynamics!
