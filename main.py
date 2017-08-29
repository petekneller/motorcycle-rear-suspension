import matplotlib.pyplot as plot
import math
import numpy as np

swingarm_length = 500
swingarm_angle_from_horz_full_shock_extension = -30
shock_spring_rate = 1000 / (2.2 * 25.4) # 1000 lbs/in -> kg/mm

# angle between swingarm and the line between swingarm pivot and lower susp. mount. This needs to be factored into the angle between swingarm and upper pivot
swingarm_pivot_vert_to_lower_mount = 50.0
swingarm_pivot_horz_to_lower_mount = 200.0
swingarm_lower_mount_included_angle = math.atan(swingarm_pivot_vert_to_lower_mount / swingarm_pivot_horz_to_lower_mount) * 180 / math.pi
swingarm_pivot_to_lower_mount = math.sqrt(swingarm_pivot_vert_to_lower_mount ** 2 + swingarm_pivot_horz_to_lower_mount ** 2)

# calculate angle between suspension mounts at resting position
swingarm_pivot_to_upper_mount = 200.0
upper_mount_to_lower_mount_resting = 270.0

def angleBetweenMountsResting():
    a = upper_mount_to_lower_mount_resting
    b = swingarm_pivot_to_upper_mount
    c = swingarm_pivot_to_lower_mount
    alpha = math.acos((b**2) + (c**2) - (a**2) / (2*b*c))
    return alpha

swingarm_upper_mount_angle_from_horz = swingarm_angle_from_horz_full_shock_extension + swingarm_lower_mount_included_angle + angleBetweenMountsResting()

# included angle between mounts to length of shock
def distanceBetweenMounts(includedAngle):
    b = swingarm_pivot_to_upper_mount
    c = swingarm_pivot_to_lower_mount
    alpha = includedAngle
    a = math.sqrt((b**2) + (c**2) - (2*b*c * cos(alpha*math.pi/180)))
    return a

# value ranges
swingarm_angle = np.linspace(-30, 30)
wheel_vertical = np.sin(swingarm_angle * math.pi / 180) * swingarm_length
wheel_compression = wheel_vertical + abs(min(wheel_vertical))
upper_mount_lower_mount_included_angle = np.ones(len(swingarm_angle)) * (swingarm_upper_mount_angle_from_horz - swingarm_lower_mount_included_angle) - swingarm_angle
shock_length = map(lambda(x): distanceBetweenMounts(x), upper_mount_lower_mount_included_angle)
shock_compression = np.ones(len(swingarm_angle)) * upper_mount_to_lower_mount_resting - shock_length
shock_load = np.ones(len(swingarm_angle)) * shock_spring_rate * shock_compression


if (__name__ == "__main__"):
  plot.figure(0)

  plot.plot(swingarm_angle, wheel_compression)
  plot.plot(swingarm_angle, upper_mount_lower_mount_included_angle)
  plot.plot(swingarm_angle, shock_length)
  plot.plot(swingarm_angle, shock_compression)
  plot.plot(swingarm_angle, shock_load)
