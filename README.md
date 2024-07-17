# VTG-LLM

# Construct Datasets for Finetuning
Please construct the datasets in the following format.
```json
{
        "id": "id of the data",
        "video": "dir to the data",
        "conversations": [
            {
                "from": "human",
                "value": "<image>\n Instruction"
            },
            {
                "from": "gpt",
                "value": "Output"
            },
            {
                "from": "human",
                "value": "<image>\n Instruction"
            },
            {
                "from": "gpt",
                "value": "Output"
            }
        ]
    },
```
