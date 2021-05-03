# drugML

Contains the Scraper and CNN model for the drugML project.

## Quick Start

In the drugML folder:

Create virtual environment

Activate virtual environment
 - ```pip install -r requirements.txt```

In the ```src/``` folder are the CNN model and the scraper, instructions below.

## Model

```src/model/CNN``` contains three scripts.
 - ```cnn.py```
 - ```cnn-tuner.py```
 - ```cnn-test.py```
 
```cnn.py``` is a standalone CNN that does 1 full set of training and validates. It is meant to be used for testing.
 - Run with ```py cnn.py```

```cnn-tuner.py``` uses keras-tuner to find an optimal model for the network, for use in the backend of the drugML application.
 - Run with ```py cnn-tuner.py```
 - The model can be saved by uncommenting the following lines:
    ```
    # Uncomment to save
    # best_model.save(f'logs\\models\\best-{TIME}-acc-{(accuracy * 100):.2f}.model')
    ```
   which will save the .model folder into ```src/model/CNN/logs/models```. This can then be used in drugML-app-backend for the application model.

```cnn-test.py``` is used for extra validation testing.
 - Run with ```py cnn-test.py```

## Scraper

The script inside ```src/scraper/``` provides functionality to scrape PubChem for molecular properties. The current properties that it is set up to collect are

```
Name
PubChem CID
Molecular Weight
Hydrogen Bond Donor Count
Hydrogen Bond Acceptor Count
Topological Polar Surface Area
Heavy Atom Count
Formal Charge
Complexity
Melting Point
Boiling Point
Solubility
logP
Density
pH
pKa
Dissociation Constant
Collision Cross Section
```

```scrape_targets.txt``` is used to give the molecules whose properties are to be scraped. It should contain lines following the pattern 

```{MOLECULE_NAME},{PUBCHEM_CID}```

Ex. ```scrape_targets.txt```
```
diclofenac,3033
etodolac,3308
fenoprofen,3342
flurbiprofen,3394
indomethacin,3715
ketorolac,3826
mefenamic acid,4044
meloxicam,54677470
nabumetone,4409
oxaprozin,4614
piroxicam,54676228
sulindac,1548887
tolmetin,5509
celecoxib,2662
buprenorphine,644073
hydrocodone,5284569
hydromorphone,5284570
meperidine,4058
methadone,4095
oxymorphone,5284604
pentazocine,441278
tapentadol,9838022
tramadol,33741
butorphanol,5361092
nalbuphine,5311304
amitriptyline,2160
imipramine,3696
venlafaxine,5656
carbamazepine,2554
gabapentin,3446
pregabalin,5486971
topiramate,5284627
milnacipran,65833
methocarbamol,4107
carisoprodol,2576
chlorzoxazone,2733
cyclobenzaprine,2895
metaxalone,15459
```

Run with ```py main.py```

Output is contained into the file located at ```src/scraper/files/scraped_data.csv```.

## Requirements
Note: kerastuner module is called keras-tuner

```Python 3.6``` - ```Python 3.8```

Python module dependencies be found in ```requirements.txt```