##  For Windows

import numpy as np
from vehiclemodel_public_wrapper import VehicleModelPublic  # 假设你的类定义保存为 `vehiclemodel.py`，导入即可

# 动态库路径（请根据实际路径替换）
dll_path = "\vehiclemodel2.dll"

# 创建模型实例并初始化
model = VehicleModelPublic(lib_path=dll_path, v_ini=10.0)  # 设置初始速度 V_ini 为 10.0

# 初始化模型，设置初始输入
initial_obs = model.initial(sped=1.0, delta=0.0)
print("Initial Observation:", initial_obs)

# 进行多次 step 验证
steps = 10
print("Starting multi-step validation...")
for step in range(steps):
    # 设置输入，模拟速度和转向角变化
    sped = 1.0 + 0.1 * step  # 模拟速度逐步递增
    delta = 0.01 * step      # 模拟转向角逐步递增

    # 调用 step 函数，并获取新的状态
    obs = model.step(sped=sped, delta=delta)

    # 输出当前 step 的输入和输出
    print(f"Step {step + 1}:")
    print(f"  Inputs - sped: {sped:.2f}, delta: {delta:.2f}")
    print(f"  Outputs - X: {obs[0]:.2f}, Y: {obs[1]:.2f}, yaw: {obs[2]:.2f}, "
          f"Vx: {obs[3]:.2f}, Vy: {obs[4]:.2f}, r: {obs[5]:.2f}")

# 终止模型
model.terminate()
print("Multi-step validation complete.")
