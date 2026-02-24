import pandas as pd
import numpy as np

def run_pipeline(df):
    # 1. Clean Strings & Categorical Nulls
    cat_cols = ['name', 'party', 'state']
    for col in cat_cols:
        df[col] = df[col].astype(str).str.strip().str.title().replace('Nan', 'Unknown')

    # 2. Map word-based numbers
    word_map = {
        'zero': 0, 'none': 0, 'five': 5, 'ten': 10, 'fifteen': 15, 
        'twenty': 20, 'forty': 40, 'sixty': 60, 'eighty': 80,
        'two thousand nineteen': 2019, 'two thousand fourteen': 2014,
        'two thousand nine': 2009, 'two thousand twenty four': 2024
    }
    
    num_cols = ['age', 'years_in_office', 'approval_rating', 
                'criminal_cases', 'total_assets_crore', 'election_year']

    # 3. Process Numbers & Impute
    for col in num_cols:
        # Convert words/strings to actual numbers
        df[col] = pd.to_numeric(df[col].astype(str).str.lower().replace(word_map), errors='coerce')
        
        if col == 'criminal_cases':
            df[col] = df[col].fillna(0)
        elif col == 'approval_rating':
            # Keep as float
            df[col] = df[col].fillna(float(df[col].median()))
        elif col in ['election_year', 'years_in_office']:
            mode_val = df[col].mode()
            df[col] = df[col].fillna(mode_val[0] if not mode_val.empty else 0)
        else:
            df[col] = df[col].fillna(df[col].median())

    # 4. Logical Constraints
    df['years_in_office'] = np.where(df['years_in_office'] > (df['age'] - 18), 
                                     df['age'] - 18, df['years_in_office'])
    df['years_in_office'] = df['years_in_office'].clip(lower=0)

    # 5. Performance Score
    df['performance_score'] = (
        (df['approval_rating'] * 0.5) + 
        (df['years_in_office'] * 0.2) - 
        (df['criminal_cases'] * 0.3)
    ).round(2)

    return df