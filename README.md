**Project**: Dynamic Price Incentive for EV Decarbonization Management in Distribution Network 

**Class**:COMS 6998 MACHINE LEARNING & CLIMATE 

**Final Presentation**: https://youtu.be/ZjWD4cKksg0


## Github Structure

### 📌 ccem.py

- **Purpose**: Implements the Constrained Cross-Entropy Method (CEM) agent.
- **Functionality**:
  - Core of the safe deep RL algorithm for charging price optimization.
  - Selects charging price actions over a planning horizon to maximize reward (profit/social welfare) under safety constraints (cost limits).
  - Samples and evaluates action sequences using a learned dynamics model.
  - Filters out action sequences that violate cost thresholds.
  - Includes a tunable Lagrange multiplier `kappa` to penalize constraint violations (ensuring policy safety).
  - Can optionally learn `kappa` during training.


### 📌 env.py

- **Purpose**: Simulates the EV charging environment (grid + transport).
- **Functionality**:
  - Defines `Environment` class.
  - Integrates with a `pandapower` 33-bus network and Dijkstra-based routing.
  - Each step:
    - Generates new EV requests (via `ev_true`).
    - Computes travel/wait times and evaluates cost at each station.
    - Determines EV choices based on combined cost (price + time).
    - Updates power grid with charging loads and runs power flow.
    - Computes:
      - Reward (e.g., profit or social welfare)
      - Cost (penalty for unsafe conditions like overloads or voltage drops)
  - **Constraint features**:
    - Grid safety (line overloads/voltage drops)
    - Partial implementation for carbon intensity constraints.

## 📌 main.py

- **Purpose**: Orchestrates training and main execution.
- **Functionality**:
  - Entry point and training script.
  - Parses command-line arguments for RL configuration.
  - Initializes:
    - Environment (`Env`)
    - Dynamics model (`ProbEnsemble`)
    - Agent (`ConstrainedCEM`)
  - Training loop:
    - Uses `EnvSampler` for environment interaction.
    - Collects `(state, action, reward, cost, next state)` tuples.
    - Stores experiences in replay buffer.
    - Trains ensemble model after fixed steps.
    - Uses model for internal rollouts and safer planning.
  - Tracks:
    - Rewards and constraint violations.
    - Updates `kappa` in constraint-aware mode.
  - Solves bi-level pricing problem via safe RL.

## 📌 models.py

- **Purpose**: Defines probabilistic ensemble model of environment dynamics.
- **Functionality**:
  - `ProbEnsemble` class (inherits `nn.Module`).
  - Predicts:
    - Next state change (delta)
    - Reward
    - Cost
  - Uses:
    - Shared fully-connected layers.
    - Output heads:
      - `GaussianEnsembleLayer` for state/reward (mean + variance).
      - `LogisticEnsembleLayer` or Gaussian for cost (binary/continuous).
  - Ensemble captures model uncertainty, critical for safe RL.
  - Training:
    - Minimizes loss over batches (MSE for state/reward, custom for cost).
    - Adds regularization.
  - Enables uncertainty-aware planning and conservative decisions.

## 📌 obs_gene.py

- **Purpose**: Generates initial observation (grid + load setup).
- **Functionality**:
  - Creates `case33bw` network and modifies for EV stations.
  - Adds extra generator and modifies line capacities.
  - Adjusts base loads:
    - Reduces all buses slightly.
    - Increases load at EV stations (buses 31, 13, 19).
  - Runs power flow to collect:
    - Line loading metrics
    - Initial condition indicators
  - Returns `obs` list and reference values (e.g., base loads at stations).
  - Initializes the environment with realistic conditions before action begins.

## 📌 model_AMS
- **model_AMS is the saved RL model checkpoint achieving the best rewards within the cost threshold.**
  
## 📌 data
- **The EV data is available at: https://github.com/hongrongyang/Paper_data**
  -EV_data1 and EV_data2: EV charging station datasets from different regions.
  -usable_data: Cleaned dataset prepared for simulation.
  -CSs_load: Charging station power variation data for specific areas.

- **The charging demand data is provided by the State Grid Corporation of China, which cannot be disclosed without desensitization.**


