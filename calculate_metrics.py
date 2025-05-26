import json
import argparse
from collections import defaultdict

def parse_arguments():
    parser = argparse.ArgumentParser(description="Calculate precision, recall, and F1 score for classification tasks")
    parser.add_argument('--file_path', type=str, required=True, help="Path to the JSON file")
    parser.add_argument('--true_label_field', type=str, required=True, help="Field name for the true labels")
    parser.add_argument('--predicted_label_field', type=str, required=True, help="Field name for the predicted labels")
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()
    file_path = args.file_path
    true_label_field = args.true_label_field
    predicted_label_field = args.predicted_label_field

    # Collect all true labels and predicted labels
    true_labels = []
    predicted_labels = []

    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Initialize statistics dictionary
    label_stats = defaultdict(lambda: {'TP': 0, 'FP': 0, 'FN': 0})

    for item in data:
        true_label = item[true_label_field]  # Get the true label using the dynamic field name
        predicted_label = item.get(predicted_label_field, '').strip()  # Get the predicted label using the dynamic field name

        if predicted_label == true_label:
            label_stats[true_label]['TP'] += 1
        else:
            label_stats[predicted_label]['FP'] += 1
            label_stats[true_label]['FN'] += 1
        true_labels.append(true_label)
        predicted_labels.append(predicted_label)


    # Define label order for output
    label_order = ["博彩", "低俗色情", "谩骂引战", "欺诈", "黑产广告", "不违规"]

    # Calculate precision, recall, and F1 score for each label
    for label in label_order:
        stats = label_stats[label]
        TP = stats['TP']
        FP = stats['FP']
        FN = stats['FN']
        
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"Label: {label}")
        print(f"Precision: {precision:.2f} Recall: {recall:.2f} F1 Score: {f1_score:.2f}")

    # Calculate average F1 score across all labels
    num_labels = len(label_order)
    total_f1_score = 0

    for label in label_order:
        stats = label_stats[label]
        TP = stats['TP']
        FP = stats['FP']
        FN = stats['FN']
        
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        total_f1_score += f1_score
        print(f"& {f1_score:.2f}", end=' ')

    average_f1_score = total_f1_score / num_labels
    print(f"& {average_f1_score:.2f}")

if __name__ == "__main__":
    main()

