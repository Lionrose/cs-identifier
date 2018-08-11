# CS Pet Identifier (LITERALLY NO CODE WRITTEN BUT HERE'S THE DOCUMENTATION)

## Run with example data
```
python id.py example_input.txt
```

This will produce an output CSV file named "example_input_out.csv"

## Configure inputs
This script takes in two inputs:

1. Input file: Pet IDs separted by lines (e.g. example_input.txt).
2. Reference images:

   Must be **named by type** (see the names in the `reference_image` folder). 

   These images must have a **transparent background, and saved without items**. For example, 
   * DO: [Pet without items](https://www.chickensmoothie.com/pet/40773414&trans=1&noitems.jpg)
   
     ![https://www.chickensmoothie.com/pet/40773414&trans=1&noitems.jpg](https://www.chickensmoothie.com/pet/40773414&trans=1&noitems.jpg)

   * DO NOT: [Pet with items](https://www.chickensmoothie.com/pet/40773414&trans=1.jpg)
   
     ![https://www.chickensmoothie.com/pet/40773414&trans=1.jpg](https://www.chickensmoothie.com/pet/40773414&trans=1.jpg)

   Note that the URLs have `.jpg`, but the images are actually PNGS. I don't know why it's like this. ¯\\\_(ツ)_/¯
     
## Outputs
The output CSV file will be named `${INPUT_NAME}_out.csv`.

Each line contains the `ID` and `TYPE` separated by a comma

e.g.
```
40773414,E2BA461F667E5DB6881FBC1C3442CC86
51218734,8CF714DA1859489A09C1C3F374935782
```

---

## TMI
In case you're bored and want to see how this script works, read on.

The first thing this script does is read the reference images, and generate mini versions of the images (+ crops out the part that says `__'s pet`). This speeds things up a bit, and eases memory usage, but honestly I don't know if its significantly helpful. But its there in case you want to identify each pets on CS or something. 

These images are saved to a dictionary that maps `image_values -> PET_TYPE`. It is assumed that the image name is some form of `PET_TYPE.png` or `PET_TYPE` or `PET_TYPE.jpg`.

Next, it goes through the list of pets from the input list. Each pet's image is downloaded, does the same shrinking + croppying. If the new image is found in the dictionary, then it retrieves the pet type. If not found, then it saves the pet type as `UNKNOWN`.

