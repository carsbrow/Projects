
import pandas as pd
import numpy as np 
import drugs

drug_data = drugs.get_report()

drug_data = pd.DataFrame(drug_data)

drug_data.head().to_csv('/Users/carsonbrown/Desktop/CS Projects/Projects/Drug-use Map/drug_data_head.csv', index=False)

