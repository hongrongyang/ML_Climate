### 📅 Week 8 (2025.3.27)

Sorry for the late update — our group officially resumed the project after the midterm, as the weeks leading up to spring break were quite busy.

After careful discussion and planning, we decided to **extend our project** by incorporating **additional carbon flow constraints** into the original EV–CS–DSO–Grid coupled optimization framework.

Our project builds upon Hongrong's previous work:  
**Dynamic Incentive Pricing on Charging Stations for Real-Time Congestion Management in Distribution Network**,  
which proposed a **dynamic incentive pricing strategy** to influence EV users to adjust their charging behavior in real time.

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

---

### 📘 DSO & Grid Constraints Summary

#### ⚡ (34) DSO Profit Formula

\[
\Pi_t^{DSO} = \sum_{n \in B} \sum_{j \in H_n} \left( C_{n,j,t}^{CS,P} - \lambda_{n,t}^{DSO,M} P_{n,j,t}^{CS,M} - \lambda_{n,t}^{DSO,D} P_{n,j,t}^{CS,D} \right)
\]

- \( \Pi_t^{DSO} \): DSO’s net profit at time \( t \);
- \( C_{n,j,t}^{CS,P} \): Revenue from EV users;
- \( \lambda^{DSO,M/D}_{n,t} \): Electricity purchase price from main grid or distributed generators;
- \( P^{CS,M/D}_{n,j,t} \): Power purchased by the CS from those sources.

#### ⚡ (35)(36) Power Purchase Costs

\[
C_{n,j,t}^{DSO,M} = \lambda_{n,t}^{DSO,M} \cdot P_{n,j,t}^{CS,M} \cdot \Delta t
\]

\[
C_{n,j,t}^{DSO,D} = \lambda_{n,t}^{DSO,D} \cdot P_{n,j,t}^{CS,D} \cdot \Delta t
\]

#### ⚡ (37) EV Charging Revenue

\[
C_{n,j,t}^{CS,P} = \sum_{i=1}^{N_{n,j,t}^{EV}} p_{n,i,t}^{EV} \cdot P_{n,i,t}^{EV} \cdot \Delta t
\]

---

#### 🧠 DSO Constraint Summary Table

| Type                | Description                                                 | Purpose                                                   |
|---------------------|-------------------------------------------------------------|------------------------------------------------------------|
| Economic Constraint | Ensures revenue minus cost equals DSO profit                | Helps DSO maximize net revenue or social welfare          |
| Cost Disaggregation | Distinguishes between main-grid and distributed supply cost | Enables flexible procurement strategy                     |
| Pricing Structure   | Links EV payment, CS purchase cost, and DSO pricing policy  | Supports boundary-aware incentive pricing optimization    |

---

### ⚡ Grid Constraints (Power Flow Equations)

#### (38) Power Balance

\[
\begin{cases}
\sum_{mn \in L} (P_{mn,t} - r_{mn} l_{mn,t}) - \sum_{nq \in L} P_{nq,t} = \sum_{j \in H_n} P_{n,j,t}^{CS} + P_n^O - P_n^{DG} \\
\sum_{mn \in L} (Q_{mn,t} - x_{mn} l_{mn,t}) - \sum_{nq \in L} Q_{nq,t} = Q_{n,t}
\end{cases}
\]

#### (39) Voltage Drop Equation

\[
v_{n,t} = v_{m,t} + 2(P_{mn,t} r_{mn} + Q_{mn,t} x_{mn}) - l_{mn,t}(r_{mn}^2 + x_{mn}^2)
\]

#### (40) SOCP Constraint (Relaxation)

\[
\left\|
\begin{bmatrix}
2P_{mn,t} \\
2Q_{mn,t} \\
l_{mn,t} - v_{n,t}
\end{bmatrix}
\right\|_2 \leq l_{mn,t} + v_{m,t}
\]

#### (41)(42)(43) Operational Bounds

- Voltage:  
\[
V_{\min}^2 \leq v_{n,t} \leq V_{\max}^2
\]
- Current:
\[
0 \leq l_{mn,t} \leq I_{\max}^2
\]
- Line Utilization:
\[
\phi_{mn,t} = \frac{P_{mn,t}}{P^{L}_{mn}} \leq \phi^{\max}_{mn,t}, \quad \forall (m,n) \in L
\]

---

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

### 📅 Week 9 (2025.4.3)

