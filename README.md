<h1 align="center"> ChineseHarm-bench</h1>
<h3 align="center"> A Chinese Harmful Content  Detection Benchmark </h3>

> ⚠️ **WARNING**: This project and associated data contain content that may be toxic, offensive, or disturbing. Use responsibly and with discretion.

<p align="center">
  <a href="">📄arXiv</a>
</p>

<div>
</div>
<div align="center">
<p align="center">
  <img src="figs/main.png"/>
</p>
</div>

[![Awesome](https://awesome.re/badge.svg)](https://github.com/zjunlp/ChineseHarm-bench) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) ![](https://img.shields.io/github/last-commit/zjunlp/ChineseHarm-bench?color=green) 

## Table of Contents

- 🌻 [Ethics Statement](#ethics-statement)
- 🌟 [Overview](#overview)
- 🚀 [Installation](#installation)
- 📚 [Inference](#inference)
- 📉 [Baseline](#baseline)
- 🚩 [Citation](#citation)

## 🌻Ethics Statement

We obtain all data with proper authorization from the respective data-owning organizations and signed the necessary agreements.

**The benchmark is released under the CC BY-NC 4.0 license.
All datasets have been anonymized and reviewed by the Institutional Review Board (IRB) of the data provider to ensure privacy protection.**

Moreover, we categorically denounce any malicious misuse of this benchmark and are committed to ensuring that its development and use consistently align with human ethical principles.

## 🌟Overview

We introduce ChineseHarm-Bench, a professionally annotated benchmark for Chinese harmful content detection, covering six key categories. It includes a knowledge rule base to enhance detection and a knowledge-augmented baseline that enables smaller LLMs to match state-of-the-art performance. 

<div>
</div>
<div align="center">
<p align="center">
  <img src="figs/chineseharm_case.png" width="80%"/>
</p>
</div>


## 🚀Installation

1. Clone the repositories:

   ```bash
   git clone https://github.com/zjunlp/ChineseHarm-bench
   cd ChineseHarm-bench
   git clone https://github.com/hiyouga/LLaMA-Factory
   ```

2. Install dependencies:

   ```bash
   cd LLaMA-Factory
   pip install -e ".[torch,metrics]" 
   ```

## 📚Inference

We release the following variants of our harmful content detection model:

- [**ChineseHarm-1.5B**](https://huggingface.co/zjunlp/ChineseHarm-1.5B)
- [**ChineseHarm-3B**](https://huggingface.co/zjunlp/ChineseHarm-3B)
- [**ChineseHarm-7B**](https://huggingface.co/zjunlp/ChineseHarm-7B)

🔹 Single Inference (Example)

Run single-input inference using the ChineseHarm-1.5B model:

```
SCRIPT_PATH="../infer/single_infer.py"
model_name="zjunlp/ChineseHarm-1.5B"
text="代发短信，有想做的联系我，无押金"

python $SCRIPT_PATH \
    --model_name $model_name \
    --text $text
```

🔸 Batch Inference (Multi-NPU)

To run inference on the entire ChineseHarm-Bench using ChineseHarm-1.5B and 8 NPUs:

```
SCRIPT_PATH="../infer/batch_infer.py"
model_name="zjunlp/ChineseHarm-1.5B"
file_name="../benchmark/bench.json"
output_file="../benchmark/bench_ChineseHarm-1.5B.json"

python $SCRIPT_PATH \
    --model_name $model_name \
    --file_name $file_name \
    --output_file $output_file \
    --num_npus 8

```

> For more configuration options (e.g., batch size, device selection, custom prompt templates), please refer to `single_infer.py` and `batch_infer.py`.

**Evaluation: Calculating F1 Score**

After inference, evaluate the predictions by computing the F1 score with the following command:

```
python ../calculate_metrics.py \
    --file_path "../benchmark/bench_ChineseHarm-1.5B.json" \
    --true_label_field "标签" \
    --predicted_label_field "predict_label"
```
## 📉Baseline

**Hybrid Knowledgeable Prompting**

First, generate diverse prompting instructions that reflect real-world violations:

```
SCRIPT_PATH="../baseline/Hybrid_Knowledgeable_Prompting.py"
output_path="../baseline/prompt.json"
python $SCRIPT_PATH\
    --output_path $output_path
```

**Synthetic Data Curation**

Use GPT-4o to generate synthetic texts conditioned on the above prompts:

```
SCRIPT_PATH="../baseline/Synthetic_Data_Curation.py"
base_url=""
api_key=""
input_file="../baseline/prompt.json"
output_file="../baseline/train_raw.json"  

python $SCRIPT_PATH \
    --base_url $base_url\
    --api_key $api_key\
    --input_file $input_file\
    --output_file $output_file

```

> 💡 The script calls the OpenAI API to generate responses based on each prompt.

**Data Process**

Filter out refused responses and sample a fixed number of instances per category to ensure balance:

```
SCRIPT_PATH="../baseline/Data_Process.py"
input_file="../baseline/train_raw.json"
output_file="../baseline/train.json"  
sample_size=3000

python $SCRIPT_PATH \
    --input_file $input_file\
    --output_file $output_file\
    --sample_size $sample_size

```

> ✅ The final output `train.json` contains `sample_size` samples per category, ready for training.

**Knowledge-Guided Training**

To prepare for training, add the following entry to `LLaMA-Factory/data/dataset_info.json`:

```
"train":{
  "file_name": "../baseline/train.json",
  "columns": {
    "prompt": "Prompt_Detect",
    "response": "违规类别"
  }
}
```

To train a 1.5B model using LLaMA-Factory:

```
mv ../train.yaml examples/train_full
llamafactory-cli train  examples/train_full/train.yaml
```

For more training configurations and customization options, please refer to the official [LLaMA-Factory GitHub repository](https://github.com/hiyouga/LLaMA-Factory).


## 🚩Citation

Please cite our repository if you use ChineseHarm-bench in your work. Thanks!

```bibtex

```

## 🎉Contributors

We will offer long-term maintenance to fix bugs and solve issues. So if you have any problems, please put issues to us.
