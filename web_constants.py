import os
import re

DATA_DIR = 'data'
DATA_META_FILE = os.path.join(DATA_DIR, 'meta.tsv')
CHROMOSOME_BANDS_FILE = os.path.join(DATA_DIR, 'chromosome_bands.tsv')


OBJ_STORE_URL = "https://mutation-signature-explorer.obj.umiacs.umd.edu/"

SIGS_DIR = os.path.join(DATA_DIR, 'sigs')
SIGS_FILE = os.path.join(SIGS_DIR, 'signatures.tsv')
SIGS_META_FILE = os.path.join(SIGS_DIR, 'signatures_meta.tsv')
SIGS_PER_CANCER_TYPE_FILE = os.path.join(SIGS_DIR, 'per_cancer_type.json')

SSM_FILE_PREFIX = 'ssm'
DONOR_FILE_PREFIX = 'donor'

# Regular Expressions
CHROMOSOME_RE = r'^(X|Y|M|[1-9]|1[0-9]|2[0-2])$'
PROJ_RE = r'^[A-Z0-9]+-[A-Z0-9]+-[A-Z]+$'
EXTRACT_PROJ_RE = r'^(?:ssm|donor)\.([A-Z0-9]+-[A-Z0-9]+-[A-Z]+)\.tsv$'

# Column names for mutation tables
VAR = 'Variant Base'
REF = 'Reference Base'
SAMPLE = 'Sample'
FPRIME = "5' Flanking Bases"
TPRIME = "3' Flanking Bases"
POS = 'Position'
CHR = 'Chromosome'
MUT_DIST = 'Distance to Previous Mutation'
NEAREST_MUT = 'Distance to Nearest Mutation'
CAT = 'Category'
CAT_INDEX = 'Category Index'
COHORT = 'Cohort'

MUT_DIST_ROLLING_MEAN = 'Rolling Mean of 6 Mutation Distances'
KATAEGIS = 'Kataegis'

# Column names for donor clinical data tables
TOBACCO_BINARY = 'Tobacco Binary'
TOBACCO_INTENSITY = 'Tobacco Intensity'
ALCOHOL_BINARY = 'Alcohol Binary'
ALCOHOL_INTENSITY = 'Alcohol Intensity'

CLINICAL_VARIABLES = [TOBACCO_BINARY, TOBACCO_INTENSITY, ALCOHOL_BINARY]

CHROMOSOMES = {
  '1': 249250621,
  '2': 243199373,
  '3': 198022430,
  '4': 191154276,
  '5': 180915260,
  '6': 171115067,
  '7': 159138663,
  '8': 146364022,
  '9': 141213431,
  '10': 135534747,
  '11': 135006516,
  '12': 133851895,
  '13': 115169878,
  '14': 107349540,
  '15': 102531392,
  '16': 90354753,
  '17': 81195210,
  '18': 78077248,
  '19': 59128983,
  '20': 63025520,
  '21': 48129895,
  '22': 51304566,
  'X': 155270560,
  'Y': 59373566,
  'M': 16571
}