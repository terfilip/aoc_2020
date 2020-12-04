import re
from typing import List, Dict


flds = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
optional_flds = {'cid'}
required_flds = flds - optional_flds
hcl_rgx = re.compile('#[a-f0-9]{6}')


def parse_passport(ln):
    items = ln.rstrip().split(' ')

    pp = {}

    for item in items:
        try:
            k, v = item.split(':')
        except ValueError:
            print('invalid format')
            print(item)
            print(f"##{ln}##")
            print(f"##{items}##")
            raise
        pp[k] = v

    return pp

def passport_is_valid(passport):
    return required_flds.issubset(set(passport.keys()))

def num_in_range(l, u):
    return lambda x: l <= int(x) <= u

def val_hgt(x):
    units = x[-2:]
    value = x[:-2]

    if units == 'cm':
        return num_in_range(150, 193)(value)
    elif units == 'in':
        return num_in_range(59, 76)(value)
    else:
        print(f'invalid units: {units}')
        return False
    

field_validators = dict(
    byr=num_in_range(1920, 2002),
    iyr=num_in_range(2010, 2020),
    eyr=num_in_range(2020, 2030),
    hgt=val_hgt,
    hcl= lambda x: hcl_rgx.fullmatch(x),
    ecl= lambda x: x in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
    pid= lambda x: len(x) == 9 and x.isdigit()
)

def validate_passport_fields(passport):
    try:
        return all((valfn(passport[k]) for k, valfn in field_validators.items()))
    except KeyError:
        print('Should only be called on passports with the required fields')
        raise


passports: List[Dict[str,str]] = []

with open('4.txt', 'r') as f:
    chunk = ''

    while line := f.readline():
        
        if line == '\n':
            passports.append(parse_passport(chunk))
            chunk = ''
        else:
            chunk += line.replace('\n', ' ')


    passports.append(parse_passport(chunk))

kind_of_valid_passports = [p for p in passports if passport_is_valid(p)]
print('P1: ', len(kind_of_valid_passports))

actually_valid_passports = [p for p in kind_of_valid_passports if validate_passport_fields(p)]
print('P2: ', len(actually_valid_passports))



