import pandapower.networks as nw
import pandapower as pp
import pandas as pd
import numpy as np
import torch as T

# Set pandas display option to prevent line wrapping
pd.set_option('display.expand_frame_repr', False)

# Define carbon intensity factors for different energy sources (kg CO2/MWh)
CO2_INTENSITY = {
    'coal': 900,
    'gas': 450,
    'nuclear': 12,
    'wind': 0
}

def obs():
    # Load the case33bw network
    net = pp.networks.case33bw()
    net1 = net

    # Add a static generator (sgen) at bus 5 with 3 MW output
    pp.create_sgen(net1, 5, p_mw=3)

    # Modify line parameters (maximum current in kA)
    net1.line.iloc[9, 9] = 6.6    # CS2 line
    net1.line.iloc[17, 9] = 6.2 # CS3 line
    net1.line.iloc[27, 9] = 15.6 # CS1 line

    # Assign carbon intensity to generators (coal-based)
    for gen in net1.gen.itertuples():
        net1.gen.at[gen.Index, 'co2_intensity'] = CO2_INTENSITY['coal']

    # Assign carbon intensity to external grid (assumed value)
    net1.ext_grid['co2_intensity'] = 700  # External grid carbon intensity (kg CO2/MWh)

    # Store original load values for nodes 31, 13, and 19
    origin_p31 = net1.load.iloc[30, 2]  # Load at node 31
    origin_p13 = net1.load.iloc[12, 2]  # Load at node 13
    origin_p19 = net1.load.iloc[18, 2]  # Load at node 19

    # Adjust load values: scale all loads by 0.9 and add 0.225 MW to nodes 31, 13, 19
    for i in range(0, 32):
        net1.load.iloc[i, 2] = net1.load.iloc[i, 2] * 0.9
    net1.load.iloc[30, 2] += 0.225  # Node 31
    net1.load.iloc[12, 2] += 0.225  # Node 13
    net1.load.iloc[18, 2] += 0.225  # Node 19

    # Run power flow calculation with numba disabled to avoid warning
    pp.runpp(net1, numba=False)

    # Initialize list to store carbon intensities for all nodes
    carbon_intensities = []

    # Get power output from generators, external grid, and static generators
    gen_power = net1.res_gen.p_mw.values  # Generator active power output
    ext_grid_power = net1.res_ext_grid.p_mw.values  # External grid active power output
    sgen_power = net1.res_sgen.p_mw.values if not net1.res_sgen.empty else [0]  # Static generator output

    # Calculate total injected power
    total_injection = sum(gen_power) + sum(ext_grid_power) + sum(sgen_power)

    # Calculate power contribution ratios for each source (system-wide, for other nodes)
    gen_ratio = np.array(gen_power) / total_injection if sum(gen_power) > 0 else np.array([0])
    ext_grid_ratio = np.array(ext_grid_power) / total_injection if sum(ext_grid_power) > 0 else np.array([0])
    sgen_ratio = np.array(sgen_power) / total_injection if sum(sgen_power) > 0 else np.array([0])

    # Get carbon intensity factors for each source
    gen_carbon = np.array(net1.gen.co2_intensity.values) if not net1.gen.empty else np.array([0])
    ext_grid_carbon = np.array(net1.ext_grid.co2_intensity.values) if not net1.ext_grid.empty else np.array(
        [0])
    sgen_carbon = np.array([CO2_INTENSITY['coal']]) if not net1.res_sgen.empty else np.array(
        [0])  # Assume sgen is coal-based

    # Define assumed alpha values for nodes 31, 13, 19 (0-based indices 30, 12, 18)
    # Sources: gen (G), sgen (S), ext_grid (E)
    alpha = np.zeros((len(net1.bus), 3))  # [alpha_gen, alpha_sgen, alpha_ext_grid] for each node
    # Default: use system-wide ratios for all nodes
    for bus_idx in range(len(net1.bus)):
        alpha[bus_idx, 0] = gen_ratio[0] if len(gen_ratio) > 0 else 0  # gen
        alpha[bus_idx, 1] = sgen_ratio[0] if len(sgen_ratio) > 0 else 0  # sgen
        alpha[bus_idx, 2] = ext_grid_ratio[0] if len(ext_grid_ratio) > 0 else 0  # ext_grid

    # Override alpha for target nodes (assumed values)
    alpha[30, 1] = 0.7  # Node 31: more from sgen (bus 5, 900 kg CO2/MWh)
    alpha[30, 2] = 0.3  # Node 31: less from ext_grid (bus 0, 700 kg CO2/MWh)
    alpha[12, 1] = 0.2  # Node 13: less from sgen
    alpha[12, 2] = 0.8  # Node 13: more from ext_grid
    alpha[18, 1] = 0.5  # Node 19: balanced
    alpha[18, 2] = 0.5  # Node 19: balanced

    # Compute carbon intensities for all nodes
    source_carbon = np.array([gen_carbon[0] if len(gen_carbon) > 0 else 0,
                              sgen_carbon[0] if len(sgen_carbon) > 0 else 0,
                              ext_grid_carbon[0] if len(ext_grid_carbon) > 0 else 0])

    for bus_idx in range(len(net1.bus)):
        # Explicitly handle bus 0, which has no load (slack bus connected to main grid)
        if bus_idx == 0:
            carbon_intensities.append(0)  # Set to 0 since bus 0 has no load; won't affect weighted CI
            continue
        node_carbon = np.sum(alpha[bus_idx] * source_carbon)
        carbon_intensities.append(node_carbon)

    # Compute weighted system carbon intensity using alpha (via node-specific CI)
    total_load = sum(net1.load.p_mw.values)
    weighted_system_carbon_intensity = 0

    for load_idx, load_row in net1.load.iterrows():
        bus_idx = load_row['bus']  # Get the bus number from the load row
        # Map bus number to 0-based index (bus 1 -> index 0 in carbon_intensities)
        carbon_idx = bus_idx  # Since carbon_intensities is indexed by bus number (0 to 32)
        load_fraction = load_row['p_mw'] / total_load if total_load > 0 else 0
        weighted_system_carbon_intensity += load_fraction * carbon_intensities[carbon_idx]

    # Get adjusted load values
    p31 = net1.load.iloc[30, 2]  # Load at node 31
    p13 = net1.load.iloc[12, 2]  # Load at node 13
    p19 = net1.load.iloc[18, 2]  # Load at node 19

    # print(carbon_intensities)
    # Construct observation vector with node-specific carbon intensities
    obs = [
        net1.res_line.iloc[9, 13] * 100,  # CS2 line loading percentage
        net1.res_line.iloc[17, 13] * 100,  # CS3 line loading percentage
        net1.res_line.iloc[27, 13] * 100,  # CS1 line loading percentage
        15, 15, 15, 67.5,  # Other parameters
        weighted_system_carbon_intensity/300
    ]

    # Return results
    return (
        obs, net1, origin_p31, origin_p13, origin_p19,
        p31, p13, p19,
        weighted_system_carbon_intensity
    )

# Run the function and print results
result = obs()
obs_values, net1, origin_p31, origin_p13, origin_p19, p31, p13, p19, system_carbon_intensity = result

# Print node-specific carbon intensities
print("Node-Specific Carbon Intensities (kg CO2/MWh):")
print(f"weighted_system_carbon_intensity: {system_carbon_intensity:.2f}")

