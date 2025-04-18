### 📅 Week 8 (2025.3.27)

Sorry for the late update — our group officially resumed the project after the midterm, as the weeks leading up to spring break were quite busy.

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

## 🔒 Constraint Summary Table (CS / DSO / Grid Constraints)

### 🧾 CS Constraints (Charging Station)
| Constraint No. | Name                          | Description                                                                 |
|----------------|-------------------------------|-----------------------------------------------------------------------------|
| (29)           | CS Profit Definition          | Defines net profit of CS as revenue minus electricity purchase cost.       |
| (30)           | CS Revenue from EV Users      | Total revenue from EVs based on charging power and incentive price.        |
| (31)           | CS Purchase Cost              | Total cost of electricity purchased by CS over time.                        |
| (32)           | CS Pricing Composition        | Breaks down charging price into power cost, service fee, and incentive fee.|
| (33)           | CS Incentive Price Bound      | Enforces upper and lower bounds on incentive pricing.                      |

### 🏢 DSO Constraints (Distribution System Operator)
| Constraint No. | Name                          | Description                                                                 |
|----------------|-------------------------------|-----------------------------------------------------------------------------|
| (34)           | DSO Profit Definition         | Net profit as revenue from EVs minus cost of main and distributed power.   |
| (35)           | Main Grid Purchase Cost       | Calculates cost of purchasing electricity from the main grid.              |
| (36)           | Distributed Source Cost       | Calculates cost of purchasing electricity from distributed sources.        |
| (37)           | CS Load Aggregation           | Ensures total charging load equals sum of supply from main and distributed sources. |

### ⚡ Grid Constraints (Power Flow & Physical Feasibility)
| Constraint No. | Name                          | Description                                                                 |
|----------------|-------------------------------|-----------------------------------------------------------------------------|
| (38)           | Power Balance Equation        | Enforces conservation of active and reactive power across the network.     |
| (39)           | Voltage Drop Model            | Models voltage drop along lines based on line parameters and power flow.   |
| (40)           | SOCP Relaxation               | Linearized cone constraint for optimization feasibility and convexity.     |
| (41)           | Voltage Bound Constraint      | Enforces upper and lower voltage limits at all nodes.                      |
| (42)           | Line Current Limit            | Restricts maximum current flow on each distribution line.                  |
| (43)           | Line Utilization Constraint   | Limits the ratio of actual power flow to line capacity to prevent overload.|

### ✅ Weekly Progress Update

This week, we mainly focused on **reviewing the original implementation**, re-setting the environment, and understanding key constraints in the CMDP optimization model.

We did not add new modules, but we have begun preparing for next week’s extension:  
> Incorporating **carbon flow modeling and constraints** into the EV–CS–DSO–Grid optimization architecture.

To support this, we surveyed related research in **carbon-aware power dispatch and optimization**.

#### 🔍 Related Research Surveyed (not limited to):
| Topic                    | Recommended Study                                                                 |
|--------------------------|------------------------------------------------------------------------------------|
| Low-carbon dispatch      | Wang et al. (IEEE TSG): *Low-carbon economic dispatch with carbon pricing*       |
| DRL + Carbon coordination| *Safe Multi-agent RL for Carbon-aware Energy Management*, NeurIPS workshop       |
| Carbon trading modeling  | Zhang et al., *Incorporating Carbon Trading into Smart Grid Dispatch Optimization*, Applied Energy |

We plan to start formulating carbon emission factors and budget constraints next week.




-------
### 📅 Week 9 (2025.4.3)

### ✅ Weekly Progress Update

This week, our main focus was on implementing the **carbon flow network** within the existing CMDP optimization framework.  
To improve the environmental sustainability and policy alignment of our original model—designed for EV load scheduling and distribution grid congestion management—we proposed an extension that incorporates **carbon emission modeling and constraints**.

This enhancement supports national carbon neutrality targets (e.g., dual-carbon policy) and can align with external mechanisms such as **carbon trading markets (ETS)**.

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

