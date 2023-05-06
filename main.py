import time
from tunisianet import main_tunisianet
from scoop import main_scoop 
from mytek import main_mytek
from zoom import main_zoom
from skymil import main_skymil


start_time = time.time()


print("run")
print("tunisianet")
main_tunisianet()
print("scoop")
main_scoop()
print("mytek")
main_mytek()
print("zoom")
main_zoom()
print("skymil")
main_skymil()


end_time = time.time()
print(f"Execution time: {(end_time - start_time)/3600} seconds")
