#Testing as a entire function
import pandas as pd

def calculate_pest_emissions(pest_name, amount):
    #pesticide_quantity_df = pesticide_quantity_df

    # Emission factors
    EF_pest_soil = 0.9
    EF_pest_air = 0.1

    # Initialize an empty list to store the results
    results = []

    # Iterate through the DataFrame rows
    #for index, row in pesticide_quantity_df.iterrows():
    #pest_name = row['pesticide']
    #pest_quantity = row['value']
        
    # Calculate emissions
    pest_em_soil = amount * EF_pest_soil
    pest_em_air = amount * EF_pest_air

    # Append the results as a dictionary
    results.append({
        'pesticide_name': pest_name,
        'pest_em_soil': pest_em_soil,
        'pest_em_air': pest_em_air
    })

    # Convert the results list to a DataFrame
    df_emissions = pd.DataFrame(results)
    df_emissions.set_index('pesticide_name', inplace=True)
    return df_emissions
   
calculate_pest_emissions('DDT', amount=1)
