from app.services.rag_pipeline import generate_answer

result = generate_answer("What are some of the company benefits?", top_k=5)

print("\nQUESTION:")
print(result["query"])

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")
for src in result["sources"]:
    print(src)