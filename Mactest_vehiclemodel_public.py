"""
Usage Restriction and Declaration:

1. This software is licensed under a reciprocal open-source agreement. Any user of this software must open-source their
   own program that utilizes it. Failure to comply may result in legal action.

2. The original author of this software is Sean Zhao. Proper attribution should be given in any use of this software,
   including but not limited to research papers, software projects, or demonstrations.

By using this software, you agree to these terms.
"""

from vehiclemodel_public_wrapper import VehicleModelPublic
import numpy as np


def main():
    """
    Main function to demonstrate the usage of the VehicleModelPublic wrapper.
    """
    try:
        # 1. Create an instance of the wrapper class
        #    Adjust the library path based on your environment
        env = VehicleModelPublic("./libmycontroller.dylib")

        # 2. Call initial() to set up the initial state
        #    - sped = 1.0 (throttle input)
        #    - delta = 0.1 (steering angle, radians)
        #    - v_ini = 10.0 (initial velocity, m/s)
        initial_obs = env.initial(sped=1.0, delta=0.1, v_ini=10.0)
        print("Initial observation:", initial_obs)

        # Variables for simulation loop
        total_reward = 0  # Accumulate rewards over steps
        done = False      # Simulation termination condition
        max_steps = 100   # Maximum simulation steps

        # 3. Loop to simulate multiple steps
        for i in range(max_steps):
            if done:
                print(f"Simulation ended at step {i + 1}")
                break

            # Example actions: sped and delta
            # Replace with your RL algorithm's outputs or control logic
            sped = 1.0
            delta = 0.05

            # Call step() to simulate the next step
            obs = env.step(sped=sped, delta=delta)
            print(f"Step {i + 1}, observation={obs}")

            # Calculate reward (example: penalize large yaw rates)
            reward = -np.abs(obs[2])  # Example reward based on yaw angle
            total_reward += reward

            # Example done condition (if speed drops below a threshold)
            if obs[3] < 0.1:  # Assuming obs[3] is velocity in x-direction
                print("Vehicle stopped. Terminating simulation.")
                done = True

        # 4. Print summary
        print("Simulation completed.")
        print(f"Total reward: {total_reward:.2f}")

    except Exception as e:
        # Catch and print any exceptions during the simulation
        print(f"An error occurred: {e}")

    finally:
        # 5. Terminate the model
        if 'env' in locals():
            env.terminate()
            print("Model terminated successfully.")


if __name__ == "__main__":
    main()
