import os
import pandas as pd
import tqdm
import random
from PIL import Image
from multiprocessing import Pool

from ancestree_utils import build_AncesTree

random.seed(10)
CSV_PATH  = '/path/to/dataset.csv'  # csv columns: it needs a 'filename' column with the relative path to the source images
SAVE_DIR = '/output/folder/'

def process_row(args):
    img_filename = args['filename']
    
    # creating folder based on source filename  (e.g.,  img: /dalle2/r006b0e4bt.jpg -> folder: /output/folder/dalle2/r006b0e4bt/ )
    img_save_dir = os.path.join(SAVE_DIR, img_filename.split('.')[0])
    
    # loading source
    img = Image.open(os.path.join(img_root, img_filename)).convert("RGB")
    
    # building tree for this source
    new_rows = build_AncesTree(depth=5,                      # total number of levels
                               branches=[4,2,2,2,2],         # number of branches for each level
                               img=img,                      # source image (root of the tree)
                               img_filename=img_filename,    # filename (relative path)
                               current_savedir=img_save_dir, # output folder (for this source)
                               out_basedir=SAVE_DIR,         # output folder (entire dataset)
                               save=True,                    # saving images
                               verbose=False)
    return new_rows


if __name__ == "__main__":
    
    img_root = os.path.dirname(CSV_PATH)
    table = pd.read_csv(CSV_PATH)
    table = table.head(3)

    out_table = []
    rows = table.to_dict(orient="records")
    with Pool(32) as pool:
        results = list(tqdm(pool.imap(process_row, rows), total=len(rows)))

    out_table = [r for log in results for r in log]

    # ---
    # Note: the root (source image) is NOT included in the output table!
    # ---

    log_df = pd.DataFrame(out_table)
    log_df.to_csv(os.path.join(SAVE_DIR, "custom_tree.csv"), index=False)
    print(log_df)