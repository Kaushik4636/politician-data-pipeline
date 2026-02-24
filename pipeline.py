import pandas as pd
import numpy as np

def run_pipeline(df):
    # 1. Standardize Strings & Handle Categorical Nulls
    cat_cols = ['name', 'party', 'state']
    for col in cat_cols:
        df[col] = df[col].astype(str).str.strip().str.title().replace('Nan', 'Unknown')

    # 2. Comprehensive Word-to-Number Mapping
    word_map = {
        'zero': 0, 'none': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'fifteen': 15, 
        'twenty': 20, 'forty': 40, 'sixty': 60, 'eighty': 80,
        'two thousand nineteen': 2019, 'two thousand fourteen': 2014, 'two thousand nine': 2009
    }
    
    num_cols = ['age', 'years_in_office', 'approval_rating', 
                'criminal_cases', 'total_assets_crore', 'election_year']

    # 3. Numeric Conversion and Imputation
    for col in num_cols:
        # Convert to lowercase string to match word_map, then to numeric
        df[col] = pd.to_numeric(df[col].astype(str).str.lower().replace(word_map), errors='coerce')
        
        # Strategic Imputation
        if col == 'criminal_cases':
            df[col] = df[col].fillna(0)
        elif col in ['election_year', 'years_in_office']:
            # Fill with most common value (mode)
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 0)
        else:
            # Fill with median for stats accuracy
            df[col] = df[col].fillna(df[col].median())

    # 4. Logical Correction (Integrity Check)
    # A politician cannot have more experience than their adult life (Age - 18)
    df['years_in_office'] = np.where(df['years_in_office'] > (df['age'] - 18), 
                                     df['age'] - 18, df['years_in_office'])
    df['years_in_office'] = df['years_in_office'].clip(lower=0)

    # 5. Performance Score Calculation
    df['performance_score'] = (
        (df['approval_rating'] * 0.5) + 
        (df['years_in_office'] * 0.2) - 
        (df['criminal_cases'] * 0.3)
    ).round(2)

    return df