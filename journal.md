

# 🌍 Project Overview: Dynamic Price Incentive for EV Decarbonization Management in Distribution Network

Our project is to optimize dynamic price incentives for electric vehicle (EV) charging to simultaneously maximize social welfare, maintain grid safety, and manage carbon emissions. Building on a DRL-based pricing framework that models the price–demand relationship through EV user behavior at charging stations, the project extends the model by adding system carbon intensity as a new state variable and introducing penalty terms for carbon limit violations. The oringal framework that formulates the pricing problem as a limited Markov Decision Process (CMDP), capturing the implicit relationship between price and demand for charging of EVs through user decision modeling. To solve this, a safe deep reinforcement learning framework is proposed and the Adaptive Model Based Safe DRL (AMSDRL) algorithm is developed. The state variables in original framework only include the distribution of electric vehicles in the charging stations and the operational status of the grid.

To improve the environmental accountability and policy relevance of this framework, we extend the system by introducing a **carbon flow layer**. Specifically, we:

- Assign **carbon emission factors** to different energy sources (e.g., grid-supplied coal power, distributed solar);
- Model **carbon emissions at the node level**, tracking the CO₂ output associated with electricity procurement;
- Embed **carbon budgets or carbon pricing mechanisms** as either constraints or cost terms in the CMDP.

By integrating carbon-aware decision signals into the state, reward, and constraint space of the reinforcement learning controller, we aim to design a DRL-based policy that coordinates EV load, grid safety, and environmental sustainability in a holistic and scalable way.

The objective of this extension is to align the system with national and regional **carbon neutrality goals**, such as China's dual-carbon policy or emission trading systems (ETS) in the US and EU. However, to simplify verification, we impose a carbon intensity limit to constrain system emissions and evaluate whether the model performs effectively in the case study.


Sorry for the late update — our group officially resumed the project after the midterm, as the weeks leading up to spring break were quite busy. 

So Let's start with our project !!

-------

#### 📅 Week 8 (2025.3.27)
After careful discussion and planning, we decided to **extend our project** by incorporating **additional carbon flow constraints** into the original EV–CS–DSO–Grid coupled optimization framework.

Our project builds upon Hongrong's previous work:  
 - **Dynamic Incentive Pricing on Charging Stations for Real-Time Congestion Management in Distribution Network**, which proposed a **dynamic incentive pricing strategy** to influence EV users to adjust their charging behavior in real time.

In this framework, the pricing problem is formulated as a **constrained Markov decision process (CMDP)** that integrates:
- Real-time EV behavior and user cost models;
- Grid-side physical constraints (power flow, voltage, current, congestion);
- Queueing, driving, and charging costs at charging stations.

A key aspect lies in the **Grid and DSO integration**:
- Charging stations report real-time load and status to the **Distribution System Operator (DSO)**;
- The DSO observes grid conditions and broadcasts **time-varying incentive prices** to affect EVs' decisions;
- Power flow equations (linearized SOCP) and operational constraints are embedded within the CMDP;
- The DSO aims to **maximize total social welfare**, balancing economic revenue, grid reliability, and service quality.

In the original paper, Hongrong develops a flow-based CMDP framework with multiple constraint formulations, including:
[Please Reference: https://ieeexplore.ieee.org/abstract/document/10298595]

##### 🔒 Constraint Summary Table (CS / DSO / Grid Constraints)
| Constraint No. | Name                          | Description                                                                 |
|----------------|-------------------------------|-----------------------------------------------------------------------------|
| (29)           | CS Profit Definition          | Defines net profit of CS as revenue minus electricity purchase cost.       |
| (30)           | CS Revenue from EV Users      | Total revenue from EVs based on charging power and incentive price.        |
| (31)           | CS Purchase Cost              | Total cost of electricity purchased by CS over time.                        |
| (32)           | CS Pricing Composition        | Breaks down charging price into power cost, service fee, and incentive fee.|
| (33)           | CS Incentive Price Bound      | Enforces upper and lower bounds on incentive pricing.                      |

##### 🏢 DSO Constraints (Distribution System Operator)
| Constraint No. | Name                          | Description                                                                 |
|----------------|-------------------------------|-----------------------------------------------------------------------------|
| (34)           | DSO Profit Definition         | Net profit as revenue from EVs minus cost of main and distributed power.   |
| (35)           | Main Grid Purchase Cost       | Calculates cost of purchasing electricity from the main grid.              |
| (36)           | Distributed Source Cost       | Calculates cost of purchasing electricity from distributed sources.        |
| (37)           | CS Load Aggregation           | Ensures total charging load equals sum of supply from main and distributed sources. |

##### ⚡ Grid Constraints (Power Flow & Physical Feasibility)
| Constraint No. | Name                          | Description                                                                 |
|----------------|-------------------------------|-----------------------------------------------------------------------------|
| (38)           | Power Balance Equation        | Enforces conservation of active and reactive power across the network.     |
| (39)           | Voltage Drop Model            | Models voltage drop along lines based on line parameters and power flow.   |
| (40)           | SOCP Relaxation               | Linearized cone constraint for optimization feasibility and convexity.     |
| (41)           | Voltage Bound Constraint      | Enforces upper and lower voltage limits at all nodes.                      |
| (42)           | Line Current Limit            | Restricts maximum current flow on each distribution line.                  |
| (43)           | Line Utilization Constraint   | Limits the ratio of actual power flow to line capacity to prevent overload.|

##### ✅ Weekly Progress Update

This week, we mainly focused on **reviewing the original implementation**, re-setting the environment, and understanding key constraints in the CMDP optimization model.

We did not add new modules, but we have begun preparing for next week’s extension:  
> Incorporating **carbon flow modeling and constraints** into the EV–CS–DSO–Grid optimization architecture.

To support this, we surveyed related research in **carbon-aware power dispatch and optimization**.

##### 🔍 Related Research Surveyed (not limited to):
| Topic                                   | Recommended Study |
|----------------------------------------|-------------------|
| Coordinated Power and Transportation Operation | T. Qian et al. (2020), *Enhanced coordinated operations of electric power and transportation networks via EV charging services*, IEEE TSG |
| MARL for V2V Charging Coordination      | J. Fan et al. (2023), *MARL for decentralized EV charging coordination with V2V exchange*, IECON 2023 |
| DRL-based EV Driving                    | H. Cha et al. (2023), *Operation strategy of EV aggregators in integrated power and transportation systems*, IEEE Access |
| Bi-level DRL for PEV Guidance           | Q. Xing et al. (2023), *Bi-level DRL for PEV decision-making in transportation-electrification systems*, Frontiers in Energy Research |
| Offline/Online DRL for Carbon Scheduling| V. Chifu et al. (2024), *Smart scheduling of EVs for demand response using DQL*, arXiv: [2401.02653](https://arxiv.org/abs/2401.02653) |
| Safe DRL under Model Uncertainty        | Y. Ma et al. (2022), *Conservative and adaptive penalty for model-based safe RL*, AAAI 2022 |

We plan to start formulating carbon emission factors and budget constraints next week.



-------
### 📅 Week 9 (2025.4.3)

##### ✅ Weekly Progress Update

This week, our main focus was on implementing the **carbon flow network** within the existing CMDP optimization framework.  
To improve the environmental sustainability and policy alignment of our original model—designed for EV load scheduling and distribution grid congestion management—we proposed an extension that incorporates **carbon emission modeling and constraints**.

### 🔧 Core Dimensions of the Proposed Extension

#### 1. Carbon Flow Modeling: Power → Carbon
- Assign a **carbon intensity factor** to each type of electricity source (e.g., grid supply, distributed energy), denoted as \( \rho_{n,t}^{CO2} \), representing CO₂ emissions per kWh.
- Introduce a **carbon budget variable** to dynamically track total emissions across buses and time periods.

#### 2. Carbon Budget Constraints & Cost Mechanisms
- Set a **global carbon constraint** (e.g., \( \sum CO_2 \leq \text{target}_t \)) to cap total emissions within the system.
- Alternatively, model emissions as a **penalty or tax term**, and embed it in the DSO or social welfare objective.
- Use a **shadow price of carbon** or ETS market price to represent marginal emission costs.

#### 3. Objective Function Enhancement: Economic + Environmental
- The original objective aimed to **maximize total social welfare**, combining: Charging station profit，EV user benefit and DSO net profit 
- We now formulate a **multi-objective optimization**, adjusting the goal as:
  - `Maximized Objective = Social Welfare – Carbon Cost × Total Emissions`

### 🧱 Implementation Building Blocks (not limited to):

| Component                        | Description                                                                                       |
|----------------------------------|---------------------------------------------------------------------------------------------------|
| Carbon Factor Definition         | Assign emission factor \( \rho_{n,t}^{CO2} \) to each energy source (e.g., grid, distributed, zero-emission). |
| Node-Level Carbon Flow Modeling  | Calculate emissions at each bus based on power consumption and source-specific emission factors. |
| Carbon Budget Constraint         | Add a system-wide constraint on total emissions to stay within a predefined carbon cap.          |
| Objective Function Penalty Term  | Introduce carbon tax or shadow price into the objective to penalize emissions.                   |
| Multi-objective Formulation      | Expand original goal to balance social welfare and environmental sustainability.                 |

### 🔄 Next Week Plan

Next week, we will focus on **integrating the carbon-aware mechanism with the DRL controller**, specifically:
- Expanding the state and reward space to include carbon cost and emission signals;
- Embedding carbon-aware safety constraints within the policy learning process;
- Evaluating trade-offs between economic efficiency and environmental impact via DRL simulations.


-------
### 📅 Week 10 (2025.4.10)

### ✅ Weekly Progress Update
This week, we focused on connecting our carbon-aware system with the DRL controller. The main goal was to ensure that the policy can make decisions not only based on user satisfaction and grid safety, but also by considering carbon emissions.

At a high level, we implemented three major enhancements:
- **State Representation Extension**  
  Incorporated carbon-related features—such as local emission factors and current carbon budget—into the agent’s state space.
- **Reward Signal Redesign**  
  Adjusted the reward function to reflect trade-offs between user satisfaction, network congestion, and environmental impact.
- **Safety Constraint Integration**  
  Treated the carbon budget as a cost constraint within the DRL framework, enabling safe policy learning under carbon limits.

### 🔄 Next Week Plan
Next week, we will begin full-scale integration and optimization of the **EV–CS–DSO–Grid–Carbon** system.  
The focus will shift to end-to-end coordination, global policy performance evaluation, and scenario-based analysis.


-------
### 📅 Week 11 (2025.4.17)

### ✅ Weekly Progress Update

This week, we conducted additional research on **carbon trading mechanisms and regional carbon emission profiles**.  
Our focus included:
- Carbon emission factors for various energy sources, including coal, wind, and hydro power;
- Carbon trading market structures in **multiple Chinese cities**, as well as in **New York and California (USA)**.

These insights are intended to inform how we define and implement carbon flow constraints more realistically and policy-aligned within our system.

### 🔄 Next Week Plan

Next week, we will begin **full-scale integration and optimization** of the complete **EV–CS–DSO–Grid–Carbon** system.

We plan to focus on:
- End-to-end coordination of all modules;
- Global policy evaluation under different scenarios;
- Finalizing experimental design and running initial simulations.

We aim to complete most of the work by the end of the weekend and next week, and generate preliminary results for evaluation.
