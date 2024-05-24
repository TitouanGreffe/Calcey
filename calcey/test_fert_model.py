import pandas as pd

# Define the function to calculate emissions
def calculate_emissions(user_input_fert_kg_N, user_input_fert_kg_P):
    # Create dataframe for generic fertilizer content
    data_fertilizer_content = {
        'fertilizer_type': ['Ammonium Sulphate', 'Ammonium chloride', 'Calcium Ammonium Nitrate', 
                            'Calcium Nitrate', 'Urea', 
                            'Single superphosphate SSP 14%', 'Rock Phosphate (powder/granular)', 
                            'Potassium chloride (powder/granular)', 'Potassium Sulphate', 
                            'NPK 15-15-15', 'NPK 10-26-26'],
        'fert_N_content_%': [0.206, 0.250, 0.260, 0.155, 0.460, 0.000, 0.000, 0.000, 0.000, 0.150, 0.100],
        'fert_P2O5_content_%': [0.000, 0.000, 0.000, 0.000, 0.000, 0.140, 0.180, 0.000, 0.000, 0.150, 0.221],
        'fert_K2O_content_%': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.60, 0.50, 0.15, 0.26]
    }
    df_fertilizer_content = pd.DataFrame(data_fertilizer_content)

    def calculate_individual_nutrient_contents(user_input_fert_type, user_input_fert_quantity_kg):
        fert_row = df_fertilizer_content[df_fertilizer_content['fertilizer_type'] == user_input_fert_type]
        
        if fert_row.empty:
            raise ValueError(f"Fertilizer type '{user_input_fert_type}' not found in the DataFrame.")
        
        nutrient_content_N = fert_row['fert_N_content_%'].values[0]
        nutrient_content_P = fert_row['fert_P2O5_content_%'].values[0]
        nutrient_content_K = fert_row['fert_K2O_content_%'].values[0]
        
        user_input_fert_kg_N = user_input_fert_quantity_kg * nutrient_content_N
        user_input_fert_kg_P = user_input_fert_quantity_kg * nutrient_content_P
        user_input_fert_kg_K = user_input_fert_quantity_kg * nutrient_content_K
        
        return user_input_fert_kg_N, user_input_fert_kg_P, user_input_fert_kg_K

    # Emission factors
    EF_N2O_fert = 0.022
    EF_NH3_syn_fert = 0.12
    EF_NH3_org_fert = 0.24
    EF_NO3_fert = 1.33
    EF_NOx_fert = 0.012
    EF_P_fert = 0.05

    Emission_kg_N2O = user_input_fert_kg_N * EF_N2O_fert
    Emission_syn_kg_NH3 = user_input_fert_kg_N * EF_NH3_syn_fert
    Emission_org_kg_NH3 = user_input_fert_kg_N * EF_NH3_org_fert
    Emission_kg_NH3 = Emission_syn_kg_NH3 + Emission_org_kg_NH3
    Emission_kg_NO3 = user_input_fert_kg_N * EF_NO3_fert
    Emission_kg_NOx = ((user_input_fert_kg_N - Emission_kg_NH3 * 17 / 14) * EF_NOx_fert) * 14 / 17
    Emission_kg_P = user_input_fert_kg_P * EF_P_fert
    
    emissions_data = {
        'Emission_kg_N2O': [Emission_kg_N2O],
        'Emission_kg_NH3': [Emission_kg_NH3],
        'Emission_kg_NO3': [Emission_kg_NO3],
        'Emission_kg_NOx_N': [Emission_kg_NOx],
        'Emission_kg_P': [Emission_kg_P]
    }
    
    return pd.DataFrame(emissions_data)


calculate_emissions(user_input_fert_kg_N=1, user_input_fert_kg_P=5)