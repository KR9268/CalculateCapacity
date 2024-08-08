import pandas as pd
import json

# 국가별 물량 입력을 위한 배열
countries = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "X"]

# A선사와 B선사 데이터 설정
aCompanyRates = { "A": 562, "B": 497, "C": 526, "D": 486, "E": 645, "F": 624, "G": 502, "H": 610, "I": 610, "J": 631, "K": 807, "L": 626, "N": 586, "M": 659, "O": 527, "P": 496, "R": 743, "S": 785, "T": 597, "U": 638, "V": 586, "W": 770, "X": 587 }
aCompanyCapacities = {
    1: { "countries": ["F"], "capacity": 3 },
    2: { "countries": ["E", "I", "O", "M", "L"], "capacity": 5 },
    3: { "countries": ["B", "P", "C", "D", "G"], "capacity": 8 },
    4: { "countries": ["H", "N", "R", "K", "S", "T", "U", "V"], "capacity": 5 },
    5: { "countries": ["A", "W", "X", "J"], "capacity": 4 }
}

bCompanyRates = { "A": 223, "B": 407, "C": 327, "D": 324, "E": 0, "F": 544, "G": 0, "H": 0, "I": 0, "J": 277, "K": 0, "L": 0, "N": 0, "M": 0, "O": 0, "P": 323, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0, "W": 508, "X": 234 }
bCompanyCapacities = {
    1: { "countries": ["X", "A", "W", "J"], "capacity": 9 },
    2: { "countries": ["B"], "capacity": 1 },
    3: { "countries": ["C"], "capacity": 4 },
    4: { "countries": ["P"], "capacity": 1 },
    5: { "countries": ["F"], "capacity": 15 },
    6: { "countries": ["D"], "capacity": 4 }
}

def get_form_data():
    # 사용자 입력을 위한 예시 데이터 (실제 사용 시 사용자 입력을 받아야 합니다)
    volume = {
        "A": 6, "B": 7, "C": 2, "D": 1, "E": 5, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0, "W": 0, "X": 0
    }
    return volume

def find_cheapest_company(ctr):
    return "b" if aCompanyRates[ctr] > bCompanyRates[ctr] else "a"

def calculate_shipping_volume(company, country, aCap, bCap, non_shippable_excess_volume):
    join_group = -1

    capacities = aCap if company == "a" else bCap

    for group in capacities:
        if country in capacities[group]["countries"]:
            join_group = group
            break

    if join_group == -1:
        return 0

    capacity = capacities[join_group]["capacity"]
    
    shipping_volume = min(non_shippable_excess_volume, capacity)
    
    capacities[join_group]["capacity"] -= shipping_volume
    
    return shipping_volume

def calculate_cheapest_shipping(volume:dict):
    #volume = get_form_data()

    aCap = json.loads(json.dumps(aCompanyCapacities))
    bCap = json.loads(json.dumps(bCompanyCapacities))

    result = {}

    for ctr in countries:
        result[ctr] = {
            "totalHopeShippingVolume": volume[ctr],
            "nonShippableExcessVolume": volume[ctr],
            "totalShippingVolume": 0,
            "totalCost": 0,
            "aCompanyShippingVolume": 0,
            "aCompanyShippingRate": aCompanyRates[ctr],
            "aCompanyTotalCost": 0,
            "bCompanyShippingVolume": 0,
            "bCompanyShippingRate": bCompanyRates[ctr],
            "bCompanyTotalCost": 0
        }

        cheapest_company = find_cheapest_company(ctr)
        not_cheapest_company = "b" if cheapest_company == "a" else "a"

        cheapest_shipping_volume = calculate_shipping_volume(cheapest_company, ctr, aCap, bCap, result[ctr]["nonShippableExcessVolume"])

        if cheapest_company == "a":
            result[ctr]["aCompanyShippingVolume"] = cheapest_shipping_volume
            result[ctr]["nonShippableExcessVolume"] -= cheapest_shipping_volume
            result[ctr]["totalShippingVolume"] += cheapest_shipping_volume
            result[ctr]["aCompanyTotalCost"] = aCompanyRates[ctr] * cheapest_shipping_volume
            result[ctr]["totalCost"] += result[ctr]["aCompanyTotalCost"]
        else:
            result[ctr]["bCompanyShippingVolume"] = cheapest_shipping_volume
            result[ctr]["nonShippableExcessVolume"] -= cheapest_shipping_volume
            result[ctr]["totalShippingVolume"] += cheapest_shipping_volume
            result[ctr]["bCompanyTotalCost"] = bCompanyRates[ctr] * cheapest_shipping_volume
            result[ctr]["totalCost"] += result[ctr]["bCompanyTotalCost"]

        not_cheapest_shipping_volume = calculate_shipping_volume(not_cheapest_company, ctr, aCap, bCap, result[ctr]["nonShippableExcessVolume"])

        if not_cheapest_company == "a":
            result[ctr]["aCompanyShippingVolume"] += not_cheapest_shipping_volume
            result[ctr]["nonShippableExcessVolume"] -= not_cheapest_shipping_volume
            result[ctr]["totalShippingVolume"] += not_cheapest_shipping_volume
            result[ctr]["aCompanyTotalCost"] += aCompanyRates[ctr] * not_cheapest_shipping_volume
            result[ctr]["totalCost"] += result[ctr]["aCompanyTotalCost"]
        else:
            result[ctr]["bCompanyShippingVolume"] += not_cheapest_shipping_volume
            result[ctr]["nonShippableExcessVolume"] -= not_cheapest_shipping_volume
            result[ctr]["totalShippingVolume"] += not_cheapest_shipping_volume
            result[ctr]["bCompanyTotalCost"] += bCompanyRates[ctr] * not_cheapest_shipping_volume
            result[ctr]["totalCost"] += result[ctr]["bCompanyTotalCost"]

    grand_total_cost = sum(r["totalCost"] for r in result.values())

    # Create a pandas DataFrame from the result dictionary
    df = pd.DataFrame(result).T  # Transpose to match the required format
    df.index.name = 'Country'

    # Print the grand total cost
    print(f"Grand Total Cost: {grand_total_cost:.2f}")

    # Print the DataFrame
    print(df.to_string(formatters={'totalCost': '{:.2f}'.format,
                                   'totalHopeShippingVolume': '{:.0f}'.format,
                                   'totalShippingVolume': '{:.0f}'.format,
                                   'nonShippableExcessVolume': '{:.0f}'.format,
                                   'aCompanyShippingVolume': '{:.0f}'.format,
                                   'aCompanyShippingRate': '{:.0f}'.format,
                                   'aCompanyTotalCost': '{:.2f}'.format,
                                   'bCompanyShippingVolume': '{:.0f}'.format,
                                   'bCompanyShippingRate': '{:.0f}'.format,
                                   'bCompanyTotalCost': '{:.2f}'.format
                                  }))
    
    return df

if __name__ == '__main__':
    # 호출 예제
    calculate_cheapest_shipping()

    import pandas as pd

    calculate_cheapest_shipping().to_csv('sample.csv')