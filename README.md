# ROS2 Nav2 Assignment — Testbed-T1.0.0

## Overview
Manual Nav2 navigation stack for the Testbed-T1.0.0 robot using ROS2 Humble + Gazebo.

## Packages
- `testbed_description` — URDF, meshes, RViz configs
- `testbed_gazebo` — Gazebo worlds, models, spawn launch files
- `testbed_bringup` — Full simulation bringup + pre-built map
- `testbed_navigation` — Map loading, AMCL localization, Nav2 navigation

## Setup

### Prerequisites
- Ubuntu 22.04
- ROS2 Humble
- Gazebo 11

### Build
```bash
mkdir -p ~/assignment_ws/src
cd ~/assignment_ws/src
git clone <this-repo-url>
cd ~/assignment_ws
colcon build
source install/setup.bash
```

### Environment (~/.bashrc)
```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=1
export OGRE_RTT_MODE=Copy
unset CYCLONEDDS_URI
unset RMW_IMPLEMENTATION
```

## Launch (in order)

### Terminal 1 — Simulation
```bash
ros2 launch testbed_bringup testbed_full_bringup.launch.py
```

### Terminal 2 — Localization
```bash
ros2 launch testbed_navigation localization.launch.py
```
Wait for: `Managed nodes are active`

### Terminal 3 — Navigation
```bash
ros2 launch testbed_navigation navigation.launch.py
```

## Send a Nav Goal
In RViz, use the **Nav2 Goal** button to send a navigation goal.
Or via terminal:
```bash
ros2 topic pub /goal_pose geometry_msgs/PoseStamped \
  "{header: {frame_id: 'map'}, pose: {position: {x: 2.0, y: 1.0, z: 0.0}, orientation: {w: 1.0}}}"
```

## Known Issues & Fixes
- **CycloneDDS participant exhaustion on VirtualBox**: Use default Fast DDS (unset RMW_IMPLEMENTATION)
- **Map not loading**: Ensure `maps/` is listed in `testbed_bringup/CMakeLists.txt` install() call
- **Fixed Frame in RViz**: Set to `map` only after localization is active
