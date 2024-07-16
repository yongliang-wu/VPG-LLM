# VTG-LLM

# Construct Datasets for Finetuning
```json
{
        "id": id of the video/image data,
        "video": dir to the video/image data,
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
