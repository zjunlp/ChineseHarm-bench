<h1 align="center"> ChineseHarm-bench</h1>
<h3 align="center"> A Chinese Harmful Content  Detection Benchmark </h3>

> ⚠️ **WARNING**: This project and associated data contain content that may be toxic, offensive, or disturbing. Use responsibly and with discretion.

<p align="center">
  <a href="https://zjunlp.github.io/project/ChineseHarm-Bench/">Project</a> •
  <a href="https://arxiv.org/abs/2506.10960v1">Paper</a> •
  <a href="https://huggingface.co/collections/zjunlp/chineseharm-bench-683b452c5dcd1d6831c3316c">Hugging Face</a> 
</p>
  
<div>
</div>
<div align="center">
<p align="center">
  <img src="figs/chineseharm_case.png" width="80%"/></p>
</div>

[![Awesome](https://awesome.re/badge.svg)](https://github.com/zjunlp/ChineseHarm-bench) ![](https://img.shields.io/github/last-commit/zjunlp/ChineseHarm-bench?color=green) 

## Table of Contents

- 🌻 [Ethics Statement](#ethics-statement)
- 🧐 [Acknowledgement](#acknowledgement)
- 🌟 [Overview](#overview)
- 🚀 [Installation](#installation)
- 📚 [Inference](#inference)
- 📉 [Baseline](#baseline)
- 🔧 [Main Results](#main-results)
- 🚩 [Citation](#citation)

## 🌻Ethics Statement

We obtain all data with proper authorization from the respective data-owning organizations and signed the necessary agreements.

**The benchmark is released under the CC BY-NC 4.0 license.
All datasets have been anonymized and reviewed by the Institutional Review Board (IRB) of the data provider to ensure privacy protection.**

Moreover, we categorically denounce any malicious misuse of this benchmark and are committed to ensuring that its development and use consistently align with human ethical principles.

##  🧐Acknowledgement

We gratefully acknowledge Tencent for providing the dataset and LLaMA-Factory for the training codebase.


## 🌟Overview

We introduce ChineseHarm-Bench, a professionally annotated benchmark for Chinese harmful content detection, covering six key categories. It includes a knowledge rule base to enhance detection and a knowledge-augmented baseline that enables smaller LLMs to match state-of-the-art performance. 

The benchmark construction process is illustrated in the figure below. For more detailed procedures, please refer to our paper.

<div>
</div>
<div align="center">
<p align="center">
  <img src="figs/main.png"/>
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
Our inference scripts support both **Huawei Ascend NPUs and NVIDIA GPUs**, enabling flexible deployment across different hardware platforms.

We release the following variants of our harmful content detection model:

- [**ChineseGuard-1.5B**](https://huggingface.co/zjunlp/ChineseGuard-1.5B)
- [**ChineseGuard-3B**](https://huggingface.co/zjunlp/ChineseGuard-3B)
- [**ChineseGuard-7B**](https://huggingface.co/zjunlp/ChineseGuard-7B)

🔹 Single Inference (Example)

Run single-input inference using the ChineseGuard-1.5B model:

```
SCRIPT_PATH="../infer/single_infer.py"
model_name="zjunlp/ChineseHarm-1.5B"
text="代发短信，有想做的联系我，无押金"

python $SCRIPT_PATH \
    --model_name $model_name \
    --text $text
```

🔸 Batch Inference (Multi-NPU or Multi-GPU)

To run inference on the entire ChineseHarm-Bench using ChineseGuard-1.5B and 8 NPUs:

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
>
> **Note:** The inference scripts support both NPU and GPU devices.

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

## 🔧Main Results
> 🔴：Without Knowledge Augmentation 🟢：With Knowledge Augmentation 🟦：Our Strong Baseline

|            Model            |  Strategy  | Knowledge | Gambling | Pornography | Abuse | Fraud | Illicit Ads | Non-Violation | Macro-F1 |
| :-------------------------: | :--------: | :-------: | :------: | :---------: | :---: | :---: | :---------: | :-----------: | :------: |
|       **Deepseek-R1**       | Prompting  |     🔴     |   0.82   |    0.77     | 0.84  | 0.53  |    0.65     |     0.78      |   0.73   |
|                             | Prompting  |     🟢     |   0.89   |    0.83     | 0.87  | 0.65  |    0.77     |     0.80      |   0.80   |
|         **O3-mini**         | Prompting  |     🔴     |   0.56   |    0.55     | 0.74  | 0.57  |    0.22     |     0.45      |   0.51   |
|                             | Prompting  |     🟢     |   0.70   |    0.55     | 0.73  | 0.60  |    0.40     |     0.46      |   0.57   |
|         **GPT-4o**          | Prompting  |     🔴     |   0.78   |    0.75     | 0.83  | 0.59  |    0.53     |     0.79      |   0.71   |
|                             | Prompting  |     🟢     |   0.89   |    0.75     | 0.82  | 0.60  |    0.75     |     0.86      |   0.78   |
|       **GPT-4o-mini**       | Prompting  |     🔴     |   0.57   |    0.70     | 0.71  | 0.43  |    0.40     |     0.59      |   0.57   |
|                             | Prompting  |     🟢     |   0.82   |    0.76     | 0.74  | 0.51  |    0.62     |     0.72      |   0.69   |
|    **Gemini 2.0 Flash**     | Prompting  |     🔴     |   0.72   |    0.76     | 0.84  | 0.63  |    0.52     |     0.75      |   0.71   |
|                             | Prompting  |     🟢     |   0.91   |    0.77     | 0.82  | 0.51  |    0.69     |     0.75      |   0.74   |
|    **Claude 3.5 Sonnet**    | Prompting  |     🔴     |   0.76   |    0.76     | 0.79  | 0.11  |    0.57     |     0.80      |   0.63   |
|                             | Prompting  |     🟢     |   0.87   |    0.81     | 0.78  | 0.36  |    0.72     |     0.78      |   0.72   |
|    **BERT-Base-Chinese**    | Finetuning |     🔴     |   0.49   |    0.60     | 0.73  | 0.49  |    0.50     |     0.68      |   0.58   |
|              🟦              | Finetuning |     🟢     |   0.74   |    0.65     | 0.76  | 0.68  |    0.68     |     0.70      |   0.70   |
| **Qwen--2.5-0.5B-Instruct** | Prompting  |     🔴     |   0.00   |    0.21     | 0.00  | 0.00  |    0.00     |     0.30      |   0.09   |
|                             | Prompting  |     🟢     |   0.00   |    0.11     | 0.00  | 0.00  |    0.00     |     0.30      |   0.07   |
|                             | Finetuning |     🔴     |   0.35   |    0.59     | 0.72  | 0.39  |    0.44     |     0.74      |   0.54   |
|              🟦              | Finetuning |     🟢     |   0.75   |    0.64     | 0.75  | 0.62  |    0.70     |     0.74      |   0.70   |
| **Qwen--2.5-1.5B-Instruct** | Prompting  |     🔴     |   0.22   |    0.08     | 0.62  | 0.47  |    0.00     |     0.48      |   0.31   |
|                             | Prompting  |     🟢     |   0.55   |    0.13     | 0.53  | 0.52  |    0.00     |     0.45      |   0.36   |
|                             | Finetuning |     🔴     |   0.36   |    0.61     | 0.74  | 0.43  |    0.48     |     0.81      |   0.57   |
|              🟦              | Finetuning |     🟢     |   0.77   |    0.71     | 0.77  | 0.70  |    0.74     |     0.79      |   0.75   |
|  **Qwen-2.5-3B-Instruct**   | Prompting  |     🔴     |   0.38   |    0.53     | 0.58  | 0.38  |    0.36     |     0.50      |   0.46   |
|                             | Prompting  |     🟢     |   0.62   |    0.55     | 0.46  | 0.58  |    0.10     |     0.49      |   0.47   |
|                             | Finetuning |     🔴     |   0.47   |    0.63     | 0.77  | 0.37  |    0.49     |     0.82      |   0.59   |
|              🟦              | Finetuning |     🟢     |   0.81   |    0.72     | 0.79  | 0.72  |    0.74     |     0.85      |   0.77   |
|  **Qwen--2.5-7B-Instruct**  | Prompting  |     🔴     |   0.35   |    0.58     | 0.42  | 0.09  |    0.45     |     0.56      |   0.41   |
|                             | Prompting  |     🟢     |   0.51   |    0.63     | 0.48  | 0.37  |    0.32     |     0.42      |   0.46   |
|                             | Finetuning |     🔴     |   0.35   |    0.64     | 0.72  | 0.38  |    0.49     |     0.82      |   0.57   |
|              🟦              | Finetuning |     🟢     |   0.82   |    0.70     | 0.75  | 0.75  |    0.75     |     0.82      |   0.77   |

## 🚩Citation

Please cite our repository if you use ChineseHarm-bench in your work. Thanks!

```bibtex
@misc{liu2025chineseharmbenchchineseharmfulcontent,
      title={ChineseHarm-Bench: A Chinese Harmful Content Detection Benchmark}, 
      author={Kangwei Liu and Siyuan Cheng and Bozhong Tian and Xiaozhuan Liang and Yuyang Yin and Meng Han and Ningyu Zhang and Bryan Hooi and Xi Chen and Shumin Deng},
      year={2025},
      eprint={2506.10960},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2506.10960}, 
}
```

## 🎉Contributors

We will offer long-term maintenance to fix bugs and solve issues. So if you have any problems, please put issues to us.
