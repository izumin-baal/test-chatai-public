# -*- coding: utf-8 -*-
"""
toolsを定義するファイル
main.pyから呼び出される
tools = [{},{},{}]
"""

TOOLS = [
    {
        "type": "function",
        "name": "get_peeringdb_net_info",
        "description": "PeeringDBから情報を取得する関数。検索にはasnかnameの情報のどちらかが必要", # API Docs: https://www.peeringdb.com/apidocs/
        "parameters": {
            "type": "object",
            "properties": {
                "asn": {
                    "type": "integer",
                    "description": "BGPのAS番号",
                },
                "name": {
                    "type": "string",
                    "description": "ASの組織名 英語で記載してください",
                }
            }
        }
    },
    {
        "type": "function",
        "name": "show_route",
        "description": "BGPルータのルーティングテーブルを表示する関数。詳細な情報は表示しない。IPもしくはPrefix情報が必ず必要です。1つのPrefixを指定してください。IPアドレスやPrefixが判明しているときに使います。",
        "parameters": {
            "type": "object",
            "properties": {
                "prefix": {
                    "type": "string",
                    "description": "BGPのプレフィックスもしくはIPアドレス",
                }
            }
        },
        "required": ["prefix"],
    },
    {
        "type": "function",
        "name": "show_route_detail",
        "description": "BGPルータのルーティングテーブルを表示する関数。詳細な情報を表示する。IPもしくはPrefix情報が必ず必要です。1つのPrefixを指定してください。IPアドレスやPrefixが判明しているときに使います。",
        "parameters": {
            "type": "object",
            "properties": {
                "prefix": {
                    "type": "string",
                    "description": "BGPのプレフィックスもしくはIPアドレス",
                }
            }
        },
        "required": ["prefix"],
    },
    {
        "type": "function",
        "name": "show_route_as-regex",
        "description": "BGPルータのルーティングテーブルを表示する関数。AS番号の正規表現でフィルタリングする。ASN情報が必ず必要です。経路を知りたいときに使います。",
        "parameters": {
            "type": "object",
            "properties": {
                "asn_regex": {
                    "type": "string",
                    "description": "BGPのAS番号の正規表現 ex) .*65000",
                }
            }
        },
        "required": ["asn_regex"],
    }
]