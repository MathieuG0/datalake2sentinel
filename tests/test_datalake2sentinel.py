import pytest
import json
from core import _build_logger
from Datalake2Sentinel import Datalake2Sentinel
from unittest import mock

logger = _build_logger()

ipv4 = "0.0.0.0"
ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
url = "https://www.google.com"
file = "dccffd34ed20d9b20480d99045606af1"
fqdn = "www.google.com"

bs_results = [
    {
        "bulk_search_hash": "0290b7530bdfeac34aa2fccc34d1ec0b",
        "advanced_query_hash": "2e310c7f15ce1887b024e275fc05b19a",
        "query_fields": [
            "atom_type",
            "atom_value",
            "tags",
            "threat_hashkey",
            "last_updated",
            "threat_types",
            "threat_scores",
            "subcategories",
        ],
        "for_stix_export": False,
        "task_uuid": "fbdd3bdf-532d-457c-a9e3-21768d59aefe",
        "results": [
            [
                "ip",
                "43.139.67.239",
                [
                    "c2",
                    "cobalt strike",
                    "cobaltstrike",
                    "cobaltstrike-2",
                    "cs-watermark-1234567890",
                    "peerpressure",
                    "port: 80",
                    "shenzhen tencent computer systems company limited",
                ],
                "7468ffb21b36a569b1dc74b1fc93fbb8",
                "2022-10-12T00:42:02Z",
                ["malware", "hack", "phishing"],
                [93, 1, 0],
                [
                    "OCD - Threat pattern:Command and Control [C2]",
                    "Tool:Cobalt Strike - S0154",
                ],
            ],
            [
                "ip",
                "37.187.180.39",
                ["bumblebee", "c2", "peerpressure", "port: 443"],
                "1ab0dd530060ff0934f29d8a8195cf47",
                "2022-10-12T00:42:02Z",
                ["malware"],
                [100],
                [
                    "Malware:Bumblebee - S1039",
                    "OCD - Threat pattern:Command and Control [C2]",
                ],
            ],
            [
                "ip",
                "154.22.168.135",
                ["c2", "cobaltstrike", "peerpressure", "port: 80"],
                "15ba40c947d0a322c14fa3d0e7c30eb3",
                "2022-10-12T00:42:02Z",
                ["malware"],
                [100],
                [
                    "OCD - Threat pattern:Command and Control [C2]",
                    "Tool:Cobalt Strike - S0154",
                ],
            ],
        ],
    }
]

datalake2Sentinel = Datalake2Sentinel(logger=logger)


def test_identify_indicator_type():
    assert datalake2Sentinel._identify_indicator_type(ipv4) == "ipv4-addr"
    assert datalake2Sentinel._identify_indicator_type(ipv6) == "ipv6-addr"
    assert datalake2Sentinel._identify_indicator_type(url) == "url"
    assert datalake2Sentinel._identify_indicator_type(file) == "file-hash"
    assert datalake2Sentinel._identify_indicator_type(fqdn) == "domain-name"
    assert datalake2Sentinel._identify_indicator_type(".") == None


def test_create_stix_pattern():
    assert (
        datalake2Sentinel._create_stix_pattern(ipv4) == "[ipv4-addr:value = '0.0.0.0']"
    )
    assert (
        datalake2Sentinel._create_stix_pattern(ipv6)
        == "[ipv6-addr:value = '2001:0db8:85a3:0000:0000:8a2e:0370:7334']"
    )
    assert (
        datalake2Sentinel._create_stix_pattern(url)
        == "[url:value = 'https://www.google.com']"
    )
    assert (
        datalake2Sentinel._create_stix_pattern(file)
        == "[file:hashes.MD5 = 'dccffd34ed20d9b20480d99045606af1']"
    )
    assert (
        datalake2Sentinel._create_stix_pattern(fqdn)
        == "[domain-name:value = 'www.google.com']"
    )
    assert datalake2Sentinel._create_stix_pattern(".") == "Unknown indicator type"


def test_create_stix_labels():
    tags = [
        "c2",
        "cobalt strike",
    ]
    threat_types = ["malware", "hack", "phishing"]
    threat_scores = [93, 1, 0]
    subcategories = [
        "OCD - Threat pattern:Command and Control [C2]",
        "Tool:Cobalt Strike - S0154",
    ]

    assert datalake2Sentinel._create_stix_labels(
        tags, threat_types, threat_scores, subcategories
    ) == [
        "c2",
        "cobalt strike",
        "OCD - Threat pattern:Command and Control [C2]",
        "Tool:Cobalt Strike - S0154",
        "dtl_score_93",
        "dtl_score_malware_93",
        "dtl_score_hack_1",
        "dtl_score_phishing_0",
    ]


def test_generateStixIndicators():
    stix_indicators = datalake2Sentinel._generateStixIndicators(bs_results)
    assert len(stix_indicators) == 3
