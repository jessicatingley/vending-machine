# Mechatronics Final Project - Vending Machine System

## Course: MCE433 – Musa Jouaneh  
**T.A.**: Jacob Travisino  
**By**: Jessica Tingley and Betty Hasse

---

## Overview

This project involves the creation of a mechatronic system that mimics the functionality of a vending machine. The system features an aluminum dispensing coil connected to a NEMA 17 Bipolar Stepper motor, which is driven by an Arduino, A4988 Stepper Driver, and other components like a proximity sensor and a GUI for control. The vending machine allows for dispensing products in controlled quantities, tracks inventory, and provides alerts when the machine is empty and needs restocking.

<p align="center">
  <img src="docs/figures/IMG_5515.gif" alt="Vending in Action">
</p>
<p align="center">
  <em>Figure 1: Vending machine dispensing.</em>
</p>

### System Features
- **Stepper Motor**: Operates the dispensing coil to move products towards or away from the dispensing area.
- **Infrared Proximity Sensor**: Detects when the coil is empty and triggers an alert.
- **GUI**: Displays control buttons for dispensing and restocking, tracks inventory, and records product dispensing data.
- **LED & Buzzer**: Notify users when the machine is empty and requires restocking.
- **CSV Logging**: Tracks and stores dispensing data including product count and dispensing time.

---

## Components

- **Arduino Mega**
- **NEMA 17 Bipolar Stepper Motor**
- **A4988 Stepper Driver**
- **EK 1254 Proximity Sensor**
- **LED**
- **Buzzer**
- **Button**

---

## System Approach

### Hardware Setup
1. **Step 1**: Code was first written to control the stepper motor, tested with a prototype of the dispensing coil.
2. **Step 2**: The infrared sensor was positioned in the dispensing area, avoiding detection of the coil itself while ensuring it triggers when the coil is empty.
3. **Step 3**: 3D-printed mounts were designed for the stepper motor, coil, and Arduino.
4. **Step 4**: All components were mounted onto a wooden base and wired for operation.

### Software Implementation
- **State Machine**: A state machine was implemented to manage different states such as "Idle," "Dispensing," "Reloading," "Empty," and "Reset."
- **Stepper Motor Control**: A PWM signal was sent to the stepper motor to control dispensing and reloading actions.
- **GUI**: A Python-based graphical user interface (GUI) was developed to interact with the user, control dispensing, restocking, and display charts of the machine's performance.

---

## System States

1. **Idle**: The machine is waiting for user input. The system checks for the proximity sensor, button presses, and commands to transition to other states.
2. **Dispensing**: The machine dispenses a number of products based on the user's selection and updates the product count.
3. **Reloading**: The machine reverses the direction of the stepper motor to restock the coil.
4. **Empty**: The sensor detects that the coil is empty. An LED and buzzer are activated to notify the user.
5. **Reset**: The machine checks the proximity sensor to ensure the coil is no longer empty before allowing dispensing to resume.

---

## GUI Features

- **Control Buttons**: Options for dispensing different quantities and restocking the machine.
- **Inventory Tracking**: Displays a live graph and updates based on dispensing activity.
- **CSV Logging**: Records data on the number of products dispensed, product count, and timestamp to ensure proper data recovery in case of a system reset.
- **Communication with Arduino**: The GUI communicates with the Arduino via serial to track and control system states.

---

## Conclusion

This project successfully demonstrates a mechatronic vending machine system that integrates hardware and software to provide a complete solution for controlled product dispensing and inventory tracking. Challenges encountered during the project, such as hardware failures and code complexity, were overcome with guidance from the Professor and Teaching Assistant.

---

## Circuit Diagram

<p align="center">
  <img src="/docs/figures/circuit.jpg" alt="Circuit diagram.">
</p>


---

## State Transition Diagram

<p align="center">
  <img src="/docs/figures/sm.jpg" alt="State diagram.">
</p>


