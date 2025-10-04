from search import search_with_scores

q = "Tell me more about the gpt-5 thinking evaluation and performance results comparing to gpt-4"
results = search_with_scores(q, k=5)

print(f"hits={len(results)}")
for i, (doc, score) in enumerate(results, 1):
    print(f"\n#{i} score={score}")
    print(doc.page_content[:600].replace("\n", " "))
