"""
Usage Restriction and Declaration:

1. This software is licensed under a reciprocal open-source agreement. Any user of this software must open-source their
   own program that utilizes it. Failure to comply may result in legal action.

2. The original author of this software is Sean Zhao. Proper attribution should be given in any use of this software,
   including but not limited to research papers, software projects, or demonstrations.

By using this software, you agree to these terms.
"""

import ctypes
import numpy as np


class VehicleModelPublic:
    """
    Encapsulates vehiclemodel_public.so / .dylib / .dll into a Python class,
    providing initial(), step(), and terminate() interfaces for use in RL.
    """

    def __init__(self, lib_path: str):
        # 1. Load the dynamic library
        self._lib = ctypes.CDLL(lib_path)

        # 2. Define the input structure (corresponding to ExtU_vehiclemodel_public_T in C)
        class ExtU_vehiclemodel_public_T(ctypes.Structure):
            _fields_ = [
                ("sped", ctypes.c_double),
                ("delta", ctypes.c_double),
                ("V_ini", ctypes.c_double),
            ]

        # 3. Define the output structure (corresponding to ExtY_vehiclemodel_public_T in C)
        class ExtY_vehiclemodel_public_T(ctypes.Structure):
            _fields_ = [
                ("X", ctypes.c_double),
                ("Y", ctypes.c_double),
                ("yaw", ctypes.c_double),
                ("Vx", ctypes.c_double),
                ("Vy", ctypes.c_double),
                ("r", ctypes.c_double),
            ]

        # 4. Bind to global variables in the library (vehiclemodel_public_U / vehiclemodel_public_Y)
        self._input_struct = ExtU_vehiclemodel_public_T.in_dll(self._lib, "vehiclemodel_public_U")
        self._output_struct = ExtY_vehiclemodel_public_T.in_dll(self._lib, "vehiclemodel_public_Y")

        # 5. Declare the return types for library functions
        self._lib.vehiclemodel_public_initialize.restype = None
        self._lib.vehiclemodel_public_step.restype = None
        self._lib.vehiclemodel_public_terminate.restype = None

        # Optional: Define storage for the previous simulation output if needed
        self.last_output = None

        # Mark whether initialization is complete
        self._initialized = False

    def initial(self, sped: float, delta: float, v_ini: float):
        """
        Initialize the model: call vehiclemodel_public_initialize,
        and set the initial input values (sped, delta, V_ini).

        sped: Represents throttle/brake input. When positive, it indicates throttle depth;
              when negative, it indicates brake depth. Recommended range: [-1, 1], but values
              outside this range are allowed.
        delta: Represents the front wheel steering angle, in radians.
        """
        # Call the initialization function in the C library
        self._lib.vehiclemodel_public_initialize()
        self._initialized = True

        # Set the input values
        self._input_struct.sped = sped
        self._input_struct.delta = delta
        self._input_struct.V_ini = v_ini

        # Optionally call step() to immediately advance the simulation
        # Note: In RL scenarios, initial observation might be required before stepping
        self._lib.vehiclemodel_public_step()  # Optional: advance the simulation by one step
        obs = self._get_current_observation()
        return obs  # Return the initial observation (optional)

    def step(self, sped: float, delta: float):
        """
        Update the input: sped, delta,
        call vehiclemodel_public_step(),
        and return the new state information (X, Y, yaw, Vx, Vy, r).

        Note:
        - The time step for each simulation step is 0.01 seconds.
        - sped: Represents throttle/brake input. When positive, it indicates throttle depth;
                when negative, it indicates brake depth. Recommended range: [-1, 1], but values
                outside this range are allowed.
        - delta: Represents the front wheel steering angle, in radians.
        """
        if not self._initialized:
            raise RuntimeError("Please call initial() to complete initialization first.")

        # 1. Update the input values (e.g., RL actions mapped to sped and delta)
        self._input_struct.sped = sped
        self._input_struct.delta = delta
        # V_ini is usually set only during initialization; modify here if necessary.

        # 2. Call the step function
        self._lib.vehiclemodel_public_step()

        # 3. Read and return the output
        obs = self._get_current_observation()
        return obs

    def terminate(self):
        """
        Terminate the model by calling vehiclemodel_public_terminate()
        """
        if self._initialized:
            self._lib.vehiclemodel_public_terminate()
            self._initialized = False

    def _get_current_observation(self):
        """
        Read the current observation (X, Y, yaw, Vx, Vy, r) from self._output_struct,
        and convert it to a Python-friendly format (e.g., numpy array).
        """
        out = self._output_struct
        obs = np.array([out.X, out.Y, out.yaw, out.Vx, out.Vy, out.r], dtype=np.float32)
        return obs
