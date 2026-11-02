from json import load
from pathlib import Path
import pandas as pd
import logging
from tqdm import tqdm
from datetime import datetime
import pandera as pa
from pandera import Column, DataFrameSchema, Check
from concurrent.futures import ThreadPoolExecutor, as_completed
logging.basicConfig(level=logging.INFO)

#Constants
FORCE_KEYS = ['Fx_t', 'Fx_l', 'Fx_r', 'Fy_t', 'Fy_l', 'Fy_r', 'Fz_t', 'Fz_l', 'Fz_r']

#DIR
PROJECT_ROOT = Path(__file__).parents[2].resolve()
DATA_OUTPUT_DIR = PROJECT_ROOT / "data" / "computed_forces"
#Pydanic
#pandera
schema_dict = {key: Column(float) for key in FORCE_KEYS}
schema_dict['swing_id'] = Column(str)
schema_dict['Fz_l'] = Column(float,Check.ge(0.0))
schema_dict['Fz_r'] = Column(float,Check.ge(0.0))
computed_force_schema = DataFrameSchema(schema_dict)


def read_single_computed_force_json(path:str|Path)->pd.DataFrame:
    """Read a single computed force JSON file and return a DataFrame.
    Args:
        path (str): Path to the JSON file containing computed forces. 
    Return:
        pd.DataFrame: Dataframe with computed force and swing id
    """
    swing_id = Path(path).name.split("_")[0]
    with open(path, 'r') as f:
        data = load(f)

    forces_df = pd.DataFrame.from_dict(data['data']["forces"])
    forces_df = forces_df[FORCE_KEYS].astype(float)
    forces_df['swing_id'] = swing_id
    return forces_df


def create_computed_force_df(dir:str|Path,save_df=True)->pd.DataFrame:
    """Create a DataFrame of computed forces from a JSON file.

    Args:
        dir (str|Path): Path to the JSON file containing computed forces.
        save_df bool: Whether to save df as a parquet file.
    Return:
        pd.Dataframe: Dataframe with computed force and swing id
    """
    dir = Path(dir)

    all_computed_force_dfs = []
    files = list(dir.glob("*_computed_forces.json"))
    for file in tqdm(files,desc="Processing computed forces"):
        try:
            computed_force_df = read_single_computed_force_json(file)
            all_computed_force_dfs.append(computed_force_df)
        except Exception as e:
            logging.info(e)

    if not all_computed_force_dfs:
        raise RuntimeError("All files failed to process")
    
    stacked_computed_force_df = pd.concat(all_computed_force_dfs, ignore_index=True)

    #checking schema of df
    logging.info("Validating df schema")
    try:
        stacked_computed_force_df = computed_force_schema.validate(stacked_computed_force_df,lazy=True)
    except (pa.errors.SchemaError, pa.errors.SchemaErrors) as e:
        logging.error(f"Pandera validation failed: {e}\nbypassing saving, returning df")
        return stacked_computed_force_df

    if save_df:
        output_dir = DATA_OUTPUT_DIR / f"{dir.name}.parquet"

        if output_dir.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = DATA_OUTPUT_DIR / f"{dir.name}_{timestamp}.parquet"

        stacked_computed_force_df.to_parquet(output_dir)
        print(f"Dataset saved to {output_dir}")
        

    return stacked_computed_force_df


if __name__ == "__main__":
    dir = r"C:\Users\Marco Chow\Documents\GitHub\m2c-computed_forces\test_data\outputs\u2_011026_240fps_combinedModel"
    stacked_df = create_computed_force_df(dir, save_df=True)

