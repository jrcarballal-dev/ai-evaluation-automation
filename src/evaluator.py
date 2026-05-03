import json

def calculate_score(scores, response):
    return sum([
        scores["accuracy"][response],
        scores["clarity"][response],
        scores["completeness"][response]
    ])

def evaluate_dataset(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    results = []

    for item in data:
        score_a = calculate_score(item["scores"], "A")
        score_b = calculate_score(item["scores"], "B")

        best = "A" if score_a > score_b else "B"

        results.append({
            "question": item["question"],
            "score_a": score_a,
            "score_b": score_b,
            "best": best
        })

    return results

def save_results(results, output_file):
    with open(output_file, "w") as f:
        for r in results:
            f.write(f"Question: {r['question']}\n")
            f.write(f"Score A: {r['score_a']} | Score B: {r['score_b']}\n")
            f.write(f"Best Response: {r['best']}\n")
            f.write("-" * 40 + "\n")

if __name__ == "__main__":
    dataset_path = "../data/dataset.json"
    output_path = "../output/results.txt"

    results = evaluate_dataset(dataset_path)
    save_results(results, output_path)

    print("Evaluation completed. Results saved.")
