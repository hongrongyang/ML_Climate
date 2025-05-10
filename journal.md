## 🌍 Project Overview: Dynamic Price Incentive for EV Decarbonization Management in Distribution Network

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

- Hongrong: Focus on code revisit and environment setup and take responsibility for industry research.
- Dongbing: Focus on code revisit and environment setup with the help of Hongrong, take responsibility for industry research and rewrite the project memos.



-------
### 📅 Week 9 (2025.4.3)

##### ✅ Weekly Progress Update

This week, our main focus was on implementing the **carbon flow network** within the existing CMDP optimization framework.  
To improve the environmental sustainability and policy alignment of our original model—designed for EV load scheduling and distribution grid congestion management—we proposed an extension that incorporates **carbon emission modeling and constraints**.

The carbon intensity formulation aims to quantify how much carbon is emitted per unit of electricity (gCO₂/kWh) within a power distribution network.

- Equation (1): Total Injected Power: Calculates the total amount of electricity entering the system by summing the outputs of generators, static (renewable) sources, and external grid imports.

- Equation (2): Power Source Contribution Ratios: Determines how much each type of source (e.g., generator, solar, grid) contributes to the total power supply. These ratios are later used to weight carbon emissions.

- Equation (3): System-Wide Carbon Intensity: Computes the average carbon intensity of the system by combining each source's carbon footprint with its contribution ratio.

- Equation (4): Node-Level Assignment: Assumes the carbon intensity is uniformly spread across all buses (nodes) in the system. This simplifies the calculation by assigning the same carbon value to each node.

- Equation (5): Load-Weighted Carbon Intensity: Provides a refined system-wide carbon intensity that takes into account how much electricity is consumed at each node. Heavily loaded nodes have more influence on the average.

- Equation (6): Node-Specific Carbon Intensity: Further refines carbon intensity by considering how electricity from different sources is actually distributed to each node, using allocation factors.

### 🔄 Next Week Plan

Next week, we will focus on **integrating the carbon-aware mechanism with the DRL controller**, specifically:
- Expanding the state and reward space to include carbon cost and emission signals;
- Embedding carbon-aware safety constraints within the policy learning process;
- Evaluating trade-offs between economic efficiency and environmental impact via DRL simulations.


- Hongrong: Responsible for the derivation and explanation of the first four equations.
- Dongbing: Responsible for the last two equations and preparation of weekly project memos.

-------
### 📅 Week 10 (2025.4.10)

##### ✅ Weekly Progress Update
This week, we focused on coupling the carbon intensity modeling with the DRL controller to enable environmentally aware policy learning. The goal was to ensure the pricing agent not only optimizes for user welfare and grid safety, but also respects system-wide carbon emission limits.

At a high level, enhancements includes:
- CMDP-Based Policy Learning: We formulated the problem as a Constrained Markov Decision Process (CMDP), where the agent maximizes long-term reward while satisfying safety constraints on system cost (e.g., carbon violations).

- Adaptive Cost Scaling: Introduced an ensemble-based uncertainty-aware cost function. The scaling factor `β` is adaptively tuned to balance safety and exploration during training.

- Extended State and Reward Design: equations to reflect the multi-objective nature of the system.
  - Reward `r_t` = scaled social welfare  
  - Cost `c_t` = carbon intensity cost `c_t^ci` + grid congestion cost `c_t^g`  

- Carbon Constraint Cost Term: Triggers penalty when the system-wide carbon intensity `CI_sw` exceeds the target limit `CI_max`. This ensures carbon emissions are constrained in the policy decisions.

- Grid Congestion Cost Term: Penalizes violations on key transmission lines if the power flow exceeds allowed thresholds `ϕ_max`. Prevents the model from creating congestion while rebalancing EV loads.

##### 🔄 Next Week Plan
Next week, we will begin full-scale integration and optimization of the **EV–CS–DSO–Grid–Carbon** system.  
The focus will shift to end-to-end coordination, global policy performance evaluation, and scenario-based analysis.

- Hongrong: Responsible for the first four enhanvements.
- Dongbing: Responsible for the last two enhanvements and preparation of weekly project memos.


-------
### 📅 Week 11 (2025.4.17)

##### ✅ Weekly Progress Update

This week, we conducted additional research on **carbon trading mechanisms and regional carbon emission profiles**.  
Our focus included:
- Carbon emission factors for various energy sources, including coal, wind, and hydro power;
- Carbon trading market structures in **multiple Chinese cities**, as well as in **New York and California (USA)**.

We conduct our experiments on a machine with a 5.60 GHz CPU, NVIDIA RTX 4090 GPU, and 64 GB of RAM. The simulation environment integrates three core components: a real-world transportation network, a modified IEEE 33-bus power distribution system, and dynamic electric vehicle (EV) charging demand.

To better focus on carbon emission dynamics, we adopt a simplified network configuration. Specifically, we modify the standard IEEE 33-bus system by removing highly congested lines (e.g., 1–18, 9–10, and 27–28) and reducing topological complexity related to congestion.

Initial results from our integrated **EV–CS–DSO–Grid–Carbon** framework show that while the proposed method improves carbon-aware coordination, both the baseline and our method occasionally exceed the predefined carbon intensity limit.

##### 🔄 Next Week Plan

Next week, we will begin **full-scale integration and optimization** of the complete **EV–CS–DSO–Grid–Carbon** system.

We plan to focus on:
- End-to-end coordination of all modules;
- Global policy evaluation under different scenarios;
- Finalizing experimental design and running initial simulations.

We aim to complete most of the work by the end of the weekend and next week, and generate preliminary results for evaluation.

- Hongrong: Responsible for power distribution network and dynamic electric vehicle demand setup.
- Dongbing: Responsible for transportation network setup and preparation of weekly project memos.

-------
### 📅 Week 12 (2025.4.24)

##### ✅ Weekly Progress Update

This week, we began optimizing our system to further improve carbon-aware performance and overall policy robustness. Key optimization steps included:

- Hyperparameter tuning: in the DRL framework to improve convergence and reduce policy variance.
- Reward function refinement: to better balance social welfare, grid safety, and emission penalties.
- Adjustment of constraint weights: to more tightly enforce carbon intensity limits without compromising system feasibility.

Our updated results clearly highlight the benefit of carbon-aware control. At the carbon intensity threshold of 790 gCO₂/kWh, the control group—which lacks carbon constraints—frequently exceeds this limit, particularly at peak hours. In contrast, our proposed method successfully keeps carbon intensity below the threshold across nearly all time steps. This confirms the effectiveness of our dynamic pricing mechanism in guiding EV behavior toward decarbonization goals.

Additionally, we completed our final presentation slides and recorded a video demo to showcase the system workflow and results.

##### 🔄 Next Week Plan

Next week, we will further refine the system based on feedback received during the class presentation. Tasks will focus on enhancing visual clarity, strengthening the model, and polishing deliverables.

- Hongrong: Focus on final model optimization and slides (method section).
- Dongbing: Responsible for updating architecture figures, completing remaining slides, and writing the weekly project memo.

-------
### 📅 Week 13 (2025.5.1)

##### ✅ Weekly Progress Update

This week, we participated in the class presentation session and gained valuable insights from our classmates work and feedback. We are especially grateful to the professor for the constructive suggestions—such as clarifying the methodology and mathematical formulations in our final report, and explicitly explaining whether the pricing signal is modeled as discrete or continuous over time.

We truly appreciate this course for broadening our perspective on reinforcement learning and its applications.

##### 🔄 Next Week Plan

Next week, we will focus on organizing our code, refining visualizations, and summarizing key insights to complete the final project report.

- Hongrong: Attend class and organize our code
- Dongbing: Attend class and write the weekly project memo.

-------
### 📅 Week 14 (2025.5.8)

##### ✅ Weekly Progress Update

This marks the final weekly post for our project. In conclusion, our work extends a model-based safe deep reinforcement learning (DRL) framework for dynamic electric vehicle (EV) pricing by incorporating carbon intensity as a new optimization constraint. By embedding system-level carbon metrics into the CMDP formulation, the enhanced AMSDRL algorithm learns pricing policies that balance social welfare, grid safety, and carbon emissions.

Simulation results on a coupled transportation network and a modified IEEE 33-bus distribution system show that the proposed method effectively reduces carbon intensity violations, maintains grid stability, and improves EV load distribution. Compared to the baseline without carbon constraints, our method keeps carbon intensity below the defined threshold while achieving stable training performance and better environmental outcomes.

Throughout this course, we gained a deeper understanding of how machine learning can help address climate challenges across sectors like power systems, manufacturing, and buildings. Through both class readings and our independent research, we explored carbon emission and climate policy frameworks. These included emission levels of different power generation types (e.g., coal, wind, solar), and carbon trading mechanisms in different countries—particularly comparing the U.S. and China.

Given that our transportation network was based in Shenzhen, China, we also studied regional carbon constraints across Chinese provinces, with a special focus on Guangdong. We explored the province’s power dispatch system and the interaction mechanisms between the grid, generation, and end-users under carbon-aware regulations.

We’re extremely grateful to have taken **COMS 6998: Machine Learning and Climate** with **Professor Alp Kucukelbir** and all the brilliant classmates in this course. It’s been one of the most inspiring and practically relevant classes in the Columbia Computer Science Department. We highly recommend it to anyone interested in applying ML to real-world climate and energy challenges.

- Hongrong: Responsible for final report  
- Dongbing: Responsible for final report and weekly project memo
