# pip install tqdm

from time import sleep

from tqdm import tqdm
# from tqdm.notebook import tqdm  # inside a Jupyter notebook

values = range(10)
with tqdm(total=len(values)) as pbar:
    for i in values:
        pbar.write('processed: %d' %i)
        pbar.update(1)
        sleep(0.1)
