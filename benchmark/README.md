
## Benchmark

This folder contains the ChineseHarm-Bench.

* `bench.json`: the full benchmark, combining all categories, with 1,000 examples per category.
* The other files (e.g., `低俗色情.json`, `欺诈.json`) are category-specific subsets.

Each file is a list of examples with:

* `"文本"`: the input Chinese text
* `"标签"`: the ground-truth label
