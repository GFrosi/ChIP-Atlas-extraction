import json
import sys



def write_json(ca_json, output):
    """
    Write content to json path
    """

    list_dset = fix_sex(ca_json)

    with open(output, 'w') as f:
        json.dump({"datasets":list_dset}, f)



def fix_sex(ca_json):

    """
    Receives a json and returns 
    a stand sex field.
    """

    list_dset = []

    for dset in ca_json['datasets']:

        new_dset = dset.copy()

        if dset['sex'] == "F" or dset['sex'] == "Female":
            new_dset['sex'] = "female"

        if dset['sex'] == "M" or dset['sex'] == "Male":
            new_dset['sex'] = "male"


        list_dset.append(new_dset)

    return list_dset


def main():

    ca_json = json.load(open(sys.argv[1]))
    output = sys.argv[2]
    write_json(ca_json, output)


if __name__ == "__main__":


    main()