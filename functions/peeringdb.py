# -*- coding: utf-8 -*-
import requests

def get_peeringdb_net_info(asn=None, name=None):
    """
    PeeringDBから情報を取得する関数。検索にはasnかnameの情報のどちらかが必要
    """
    if not asn and not name:
        return "[Error] AS番号か組織名のいずれかを指定してください。"

    API_URL = "https://www.peeringdb.com/api/net"
    params = {}
    
    if asn:
        params["asn"] = asn
    if name:
        params["name__contains"] = name

    response = requests.get(API_URL, params=params)
    
    if response.status_code == 200:
        print("Function: get_peeringdb_net_info")
        print("Response:", response.json())
        return response.json()
    else:
        response.raise_for_status()

if __name__ == "__main__":
    # Example usage
    name = "Google"
    result = get_peeringdb_org_info(name=name)
    print(result)