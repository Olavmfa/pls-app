from flask import Flask
from typing import Union
import datetime
import pandas as pd
import json

app = Flask(__name__)

#Test driven:

## Should validate a pnum based on rules for a pnum
## Should not accept a number with other characters than integers
## Should return male if pnum is male, female if female, no gender (invalid pnum) if invalid pnum
## Should return correct age based on pnum rule, and no age if invalid pnum
## Assert response is in correct format (JSON)

def _check_pnum_validity(pnum: str) -> Union[bool, str]:
    """_summary_

    Args:
        pnum (str): pnum recieved from request in string format

    Returns:
        bool: True if valid pnum, False otherwise
    """
    # Create error message explaining how to properly enter a personal number.
    #error_message = "\nA valid personal number contains 11 digits.\nThe first six digits represent the date of birth (ddmmyy).\nThe following three numbers are individual, where the final of the three represent whether the person is male (odd number) or female (even numer).\n The final two digits are control digits."
    error_message = ""
    # Check if pnum is all digits
    pnum = pnum.strip()
    if not pnum.isdigit():
        error_message = "The input personal number contains invalid characters." + error_message
        return False, error_message
    # Check if pnum is of len 11
    if len(pnum) != 11:
        error_message = "The input personal numbers must contain 11 digits." + error_message
        return False, error_message
    # Check if date of birth is plausible
    dd = int(pnum[0])*10 + int(pnum[1])
    mm = int(pnum[2])*10 + int(pnum[3])
    yy = int(pnum[4])*10 + int(pnum[5])
    try:
        datetime.datetime(year=yy,month=mm,day=dd)
    except ValueError:
        error_message = "The input personal numbers contains an invalid date of birth." + error_message
        return False, error_message
    # The pnum passed all tests, and is valid
    return True, ""

def _get_gender(pnum:str) -> str:
    """_summary_

    Args:
        pnum (str): pnum recieved from request in string format. Assumes pnum is valid.

    Returns:
        str: "male" or "female"
    """
    gender = int(pnum[8])
    return "female" if gender%2 == 0 else "male"

def _get_age(pnum:str) -> str:
    """_summary_

    Args:
        pnum (str): pnum recieved from request in string format. Assumes pnum is valid.

    Returns:
        str: age in years, as string.
    """
    # Today's date
    today = datetime.datetime.today()
    # Date of birth as datetime
    dd = int(pnum[0])*10 + int(pnum[1])
    mm = int(pnum[2])*10 + int(pnum[3])
    yy = int(pnum[4])*10 + int(pnum[5])
    # Assuming everyone is born after 1900
    if yy <= int(str(today.year)[2:4]):
        yy += 2000
    else:
        yy += 1900
    date_of_birth = datetime.datetime(year=yy,month=mm,day=dd)
    # Difference in years, +- 1 concerning the days and months
    age_in_years = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    age_in_years = str(age_in_years)
    return age_in_years

def _read_dataset():
    if app.testing == True:
        path='mock_pnr.txt'
    else:
        path='pnr.txt'
    with open(path, 'r') as f:
        lines = f.readlines()
    return lines

def _check_if_pnum_in_dataset(pnum:str) -> bool:
    """_summary_

    Args:
        pnum (str): pnum recieved from request in string format. Assumes pnum is valid.

    Returns:
        bool: True if pnum in dataset, False otherwise
    """
    # Access dataset
    dataset = _read_dataset()
    # Iterate over rows in the dataset
    for row in dataset[1:]:
        row = row.strip()
        # Return True if we find a match
        if row == pnum:
            return True
    # No match found
    return False

def _get_valid_pnums_per_gender_and_age() -> pd.DataFrame:
    """
    Method for subtracting and sorting information concerning personal numbers from the dataset.
    
    Returns:
        pd.DataFrame: Sorted amount of personal numbers by gender and age
    """
    # Access dataset
    dataset = _read_dataset()
    # Iterate over the rows in the data set
    df_rows = []
    for row in dataset[1:]:
        row = row.strip()
        # Skip row if invalid pnum
        isvalid, msg = _check_pnum_validity(row)
        if isvalid:
            # add row to df with gender and age
            age = int(_get_age(row))
            gender = _get_gender(row)
            df_rows.append([row, age, gender])
    # Create df to label and order the data
    df = pd.DataFrame(df_rows, columns=["pnum", "age", "gender"])
    # Create age categories (age groups)
    bins= [-1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200]
    labels = ["0 - 9 years", "10 - 19 years", "20 - 29 years", "30 - 39 years", "40 - 49 years", "50 - 59 years", "60 - 69 years", "70 - 79 years", "80 - 89 years", "99 - 99 years", "Above 100 years"]
    df['age group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    # Count rows of equal gender and age group
    df_series = df.groupby(['age group', 'gender']).size()
    df_series = df_series[df_series != 0]
    df_series = df_series.astype(str)
    return df_series

def _count_pnums() -> Union[str, str, str, str, str]:
    """
    Method for counting number of personal numbers in the dataset, as well as number of men and women

    Returns:
        Union[str, str, str]: number of pnums, valid pnums, invalid pnums, men and women
    """
    dataset = _read_dataset()
    men = 0
    women = 0
    pnums = 0
    invalid_pnums = 0
    valid_pnums = 0
    for row in dataset[1:]:
        row = row.strip()
        isvalid, msg = _check_pnum_validity(row)
        if isvalid:
            gender = _get_gender(row)
            if gender == "male":
                men += 1
            else:
                women += 1
            valid_pnums += 1
        else:
            invalid_pnums += 1
    pnums = valid_pnums + invalid_pnums
    return str(pnums), str(valid_pnums), str(invalid_pnums), str(men), str(women)


@app.get("/pnums/listall")
def list_pnums():
    pnums, valid_pnums, invalid_pnums, men, women = _count_pnums()
    response = {
        "total pnums": pnums,
        "valid pnums": valid_pnums,
        "invalid pnums": invalid_pnums,
        "male" : men,
        "female": women
        }
    response = json.dumps(response)
    return response

@app.get("/pnums/listbygroups")
def get_list_of_pnums_by_gender_and_age():
    pnum_df = _get_valid_pnums_per_gender_and_age()
    response = pnum_df.to_json()
    return response
    
@app.get("/pnums/age/<pnum>")
def get_age(pnum: str = ""):
    isvalid, error_msg = _check_pnum_validity(pnum)
    if not isvalid:
        # Finn ut hvordan man raiser error.
        return json.dumps({"Error message": error_msg}), 400
    age = _get_age(pnum)
    response = {
        "pnum": pnum.strip(),
        "age": age
        }
    response = json.dumps(response)
    return response

@app.get("/pnums/gender/<pnum>")
def get_gender(pnum: str = ""):
    isvalid, error_msg = _check_pnum_validity(pnum)
    if not isvalid:
        return json.dumps({"Error message": error_msg}), 400
    gender = _get_gender(pnum)
    response = {
        "pnum": pnum.strip(),
        "gender": gender
        }
    response = json.dumps(response)
    return response

@app.get("/pnums/isvalid/<pnum>")
def get_validity(pnum: str = ""):
    isvalid, error_msg = _check_pnum_validity(pnum)
    response = {
        "pnum": pnum.strip(),
        "is valid pnum": "yes" if isvalid else "no",
        }
    if not isvalid:
        response["reason"] = error_msg
    response = json.dumps(response)
    return response

@app.get("/pnums/isregistered/<pnum>")
def get_register_status(pnum: str = ""):
    isvalid, error_msg = _check_pnum_validity(pnum)
    isregistered = _check_if_pnum_in_dataset(pnum)
    response = {
        "pnum": pnum.strip(),
        "is in dataset": "yes" if isregistered else "no",
        "is valid pnum": "yes" if isvalid else "no"
    }
    response = json.dumps(response)
    return response