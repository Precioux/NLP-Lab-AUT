import requests

data = {
    "conversation": {
        "intent": {
            "label": "convert_currency",
            "logit_score": "16.22031021118164",
            "softmax_score": "0.9965572357177734",
            "min_max_normalized_score": "1.0",
            "simple_normalized_score": "0.27542752027511597"
        },
        "top_intents": [
            {
                "label": "convert_currency",
                "logit_score": "16.22031021118164",
                "softmax_score": "0.9965572357177734",
                "min_max_normalized_score": "1.0",
                "simple_normalized_score": "0.27542752027511597"
            },
            {
                "label": "ask_currency",
                "logit_score": "10.523137092590332",
                "softmax_score": "0.0033438855316489935",
                "min_max_normalized_score": "0.5532662868499756",
                "simple_normalized_score": "0.1786871701478958"
            },
            {
                "label": "movie_score",
                "logit_score": "5.264869689941406",
                "softmax_score": "1.7402629964635707e-05",
                "min_max_normalized_score": "0.1409485638141632",
                "simple_normalized_score": "0.08939964324235916"
            },
            {
                "label": "investment_money",
                "logit_score": "4.554596900939941",
                "softmax_score": "8.553568477509543e-06",
                "min_max_normalized_score": "0.08525379002094269",
                "simple_normalized_score": "0.07733891904354095"
            },
            {
                "label": "translate_it",
                "logit_score": "4.050086975097656",
                "softmax_score": "5.16465661348775e-06",
                "min_max_normalized_score": "0.045693539083004",
                "simple_normalized_score": "0.06877213716506958"
            },
            {
                "label": "what_is_bot",
                "logit_score": "3.8756725788116455",
                "softmax_score": "4.338045528129442e-06",
                "min_max_normalized_score": "0.032017141580581665",
                "simple_normalized_score": "0.06581050902605057"
            },
            {
                "label": "word_meaning",
                "logit_score": "3.7970638275146484",
                "softmax_score": "4.010097200080054e-06",
                "min_max_normalized_score": "0.025853175669908524",
                "simple_normalized_score": "0.06447570025920868"
            },
            {
                "label": "calendar_convert",
                "logit_score": "3.630157232284546",
                "softmax_score": "3.393660563233425e-06",
                "min_max_normalized_score": "0.01276549231261015",
                "simple_normalized_score": "0.06164155527949333"
            },
            {
                "label": "get_food_energy",
                "logit_score": "3.5081427097320557",
                "softmax_score": "3.0038479508220917e-06",
                "min_max_normalized_score": "0.0031979396007955074",
                "simple_normalized_score": "0.059569697827100754"
            },
            {
                "label": "ask_time",
                "logit_score": "3.4673595428466797",
                "softmax_score": "2.8838067009928636e-06",
                "min_max_normalized_score": "0.0",
                "simple_normalized_score": "0.058877184987068176"
            }
        ],
        "slots": [
            {
                "start": 10,
                "end": 15,
                "text": "دینار",
                "label": "currency",
                "score": "1.0"
            },
            {
                "start": 25,
                "end": 29,
                "text": "دلار",
                "label": "dest_currency",
                "score": "1.0"
            }
        ]
    },
    "whatever": False
}


response = requests.post("http://localhost:8080/process_request", json=data)
print(response.json())