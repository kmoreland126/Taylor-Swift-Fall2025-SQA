import sys
import os
import random
import string
import logging
import statistics
import numpy as np
from builtins import ZeroDivisionError, TypeError, OverflowError, ValueError 
import pandas as pd
import shutil

# --- Fix for imports: Set up paths to the NESTED FAME-ML and empirical folders ---

# 1. Get the directory where fuzz_simple.py is located.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Define the path to the main project folder.
PROJECT_ROOT = os.path.join(current_dir, 'MLForensics-farzana')

# 3. Define the two subfolder paths:
PATH_FAME_ML = os.path.join(PROJECT_ROOT, 'FAME-ML')
PATH_EMPIRICAL = os.path.join(PROJECT_ROOT, 'empirical')

# 4. Add both target paths to the system path.
# This allows Python to find 'report.py' directly and 'frequency.py' directly.
if PATH_FAME_ML not in sys.path:
    sys.path.append(PATH_FAME_ML) 
if PATH_EMPIRICAL not in sys.path:
    sys.path.append(PATH_EMPIRICAL) 

# Attempt to import the required functions now that the paths are set.
try:
    # report.py is now on the path
    from report import Average, Median
    # frequency.py is now on the path
    from frequency import reportProportion
except ImportError as e:
    print(f"CRITICAL ERROR: Failed to import functions. Check paths: FAME-ML ({PATH_FAME_ML}), empirical ({PATH_EMPIRICAL})")
    print(f"Details: {e}")
    sys.exit(1)


# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger('FuzzEngine')

# --- Fuzzing Functions ---
# Note: We are now fuzzing a third method: reportProportion, which relies on file creation.

def create_fuzz_file(filename, content):
    """Creates a temporary file with malformed content."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

def generate_fuzz_data():
    """Generates various lists designed to break Average/Median."""
    return [
        # 1. Empty list (Expected ZeroDivisionError for Average, StatisticsError for Median)
        ([], ZeroDivisionError, statistics.StatisticsError),
        
        # 2. Non-numeric strings (Expected TypeError for both)
        ([1, 'a', 3], TypeError, TypeError),
        
        # 3. Mixed valid/invalid random data
        ([random.randint(1, 10), random.choice(string.ascii_letters), 5], TypeError, TypeError),
        
        # 4. Floating point NaN (Expected ValueError/StatisticsError)
        ([1.0, 2.0, np.nan], ValueError, statistics.StatisticsError),

        # 5. Valid Case: Normal data (Expected no error)
        ([1, 2, 3, 4], None, None), 
    ]

def fuzz_test_runner(func, data, expected_error):
    """Runs a single fuzz test and logs the result."""
    try:
        result = func(data)
        if expected_error:
            logger.error(f"BUG FOUND: {func.__name__}({data}) processed data but was expected to raise {expected_error.__name__}")
        else:
            logger.info(f"PASS: {func.__name__}({data}) = {result}")
            
    except Exception as e:
        if isinstance(e, expected_error):
            logger.info(f"PASS: {func.__name__}({data}) raised expected {expected_error.__name__}")
        else:
            logger.error(f"BUG FOUND: {func.__name__}({data}) raised UNEXPECTED {type(e).__name__}: {e}")

def fuzz_report_proportion(temp_dir, fuzz_content):
    """Fuzzes reportProportion, which needs file I/O."""
    
    logger.info(f"--- Fuzzing reportProportion with Malformed CSV ---")
    
    # reportProportion requires an input CSV with specific columns (e.g., 'REPO_FULL_PATH')
    # and an output path. We will generate both.
    
    FUZZ_IN_PATH = os.path.join(temp_dir, 'fuzz_in.csv')
    FUZZ_OUT_PATH = os.path.join(temp_dir, 'fuzz_out.csv')
    
    os.makedirs(temp_dir, exist_ok=True)
    create_fuzz_file(FUZZ_IN_PATH, fuzz_content)

    # Test 1: Malformed content (Expected pandas.errors.ParserError or KeyError)
    try:
        reportProportion(FUZZ_IN_PATH, FUZZ_OUT_PATH)
        logger.error(f"BUG FOUND: reportProportion processed malformed data without error/crash.")
    except pd.errors.ParserError:
        logger.info(f"PASS: reportProportion raised expected ParserError.")
    except KeyError as e:
        logger.info(f"PASS: reportProportion raised expected KeyError (due to missing required column: {e})")
    except Exception as e:
        logger.error(f"BUG FOUND: reportProportion raised UNEXPECTED {type(e).__name__}: {e}")

    # Test 2: Non-existent file path
    logger.info(f"--- Fuzzing reportProportion with non-existent file path ---")
    try:
        reportProportion('/nonexistent/path/fuzz.csv', FUZZ_OUT_PATH)
        logger.error(f"BUG FOUND: reportProportion did not crash on non-existent file.")
    except FileNotFoundError:
        logger.info(f"PASS: reportProportion raised expected FileNotFoundError.")
    except Exception as e:
        logger.error(f"BUG FOUND: reportProportion raised UNEXPECTED {type(e).__name__}: {e}")


# --- Main Execution ---
if __name__ == '__main__':
    
    fuzz_data_set = generate_fuzz_data()
    
    logger.info("====================================")
    logger.info("STARTING FUZZ TESTS")
    logger.info("====================================")

    # 1. Fuzz Average and Median (2 methods, 5 data cases)
    for data, avg_expected, med_expected in fuzz_data_set:
        fuzz_test_runner(Average, data, avg_expected)
        fuzz_test_runner(Median, data, med_expected)

    # 2. Fuzz reportProportion (1 method, 2 file cases)
    FUZZ_DIR = 'fuzz_temp'
    MALFORMED_CSV = "This is not CSV content!\nIt's just random data.\n1,2,3"
    try:
        fuzz_report_proportion(FUZZ_DIR, MALFORMED_CSV)
    finally:
        # Cleanup: Remove temporary directory
        if os.path.exists(FUZZ_DIR):
            shutil.rmtree(FUZZ_DIR)
        
    logger.info("====================================")
    logger.info("FUZZING COMPLETE")
    logger.info("====================================")