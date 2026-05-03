import json
import csv
import os


def calculate_score(scores, response):
    """Calculate total score for a given response (A or B)"""
    return (
        scores["accuracy"][response]
        + scores["clarity"][response]
        + scores["completeness"][response]
    )


def load_dataset(file_path):
    """Load dataset with error handling"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        return None


def evaluate_dataset(data):
    """Evaluate dataset and compare predictions with human labels"""
    results = []
    correct_predictions = 0

    for item in data:
        try:
            score_a = calculate_score(item["scores"], "A")
            score_b = calculate_score(item["scores"], "B")

            predicted = "A" if score_a > score_b else "B"
            actual = item["best_response"]

            is_correct = predicted == actual
            if is_correct:
                correct_predictions += 1

            results.append({
                "question": item["question"],
                "score_a": score_a,
                "score_b": score_b,
                "predicted": predicted,
                "actual": actual,
                "correct": is_correct
            })

        except Exception as e:
            print(f"[WARNING] Skipping item due to error: {e}")

    accuracy = (correct_predictions / len(data)) * 100 if data else 0

    return results, accuracy


def save_txt(results, accuracy, output_file):
    """Save results in TXT format"""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for r in results:
                f.write(f"Question: {r['question']}\n")
                f.write(f"Score A: {r['score_a']} | Score B: {r['score_b']}\n")
                f.write(f"Predicted: {r['predicted']} | Actual: {r['actual']}\n")
                f.write(f"Correct: {r['correct']}\n")
                f.write("-" * 50 + "\n")

            f.write(f"\nOverall Accuracy: {accuracy:.2f}%\n")

    except Exception as e:
        print(f"[ERROR] Failed to save TXT: {e}")


def save_csv(results, output_file):
    """Save results in CSV format"""
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Question", "Score A", "Score B",
                "Predicted", "Actual", "Correct"
            ])

            for r in results:
                writer.writerow([
                    r["question"],
                    r["score_a"],
                    r["score_b"],
                    r["predicted"],
                    r["actual"],
                    r["correct"]
                ])

    except Exception as e:
        print(f"[ERROR] Failed to save CSV: {e}")


def ensure_output_dir(path):
    """Ensure output directory exists"""
    os.makedirs(path, exist_ok=True)


if __name__ == "__main__":
    dataset_path = "../data/dataset.json"
    output_dir = "../output"

    ensure_output_dir(output_dir)

    txt_output = os.path.join(output_dir, "results.txt")
    csv_output = os.path.join(output_dir, "results.csv")

    data = load_dataset(dataset_path)

    if data:
        results, accuracy = evaluate_dataset(data)

        save_txt(results, accuracy, txt_output)
        save_csv(results, csv_output)

        print("✅ Evaluation completed successfully")
        print(f"📊 Accuracy: {accuracy:.2f}%")
        print(f"📁 Results saved in: {output_dir}")
    else:
        print("❌ Evaluation failed")
