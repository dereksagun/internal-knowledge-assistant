import asyncio
import json
from pathlib import Path
from src.core.container import get_deps
from src.services.agent_service import build_agent_service
from dotenv import load_dotenv
load_dotenv()
deps = get_deps()
handle_message = build_agent_service(deps)

def answer_with_citation(result):
    return bool(result["content"].strip()) and len(result["citations"]) > 0

def structured_answer_with_citation(result):
    structured = any(x in result["content"] for x in ["\n-", "\n1.", "\n•"])
    return structured and len(result["citations"]) > 0

def multi_doc_answer(result):
    sources = {c["source_path"] for c in result["citations"]}
    return len(sources) >= 2

def refute_with_citation(result):
    refute_terms = ["not", "does not", "is incorrect", "no,"]
    text = result["content"].lower()
    return any(t in text for t in refute_terms) and len(result["citations"]) > 0

def not_found(result):
    refusal_terms = [
        "couldn't find",
        "not found",
        "no information",
        "not available",
        "do not contain",
        "I don't"
    ]
    text = result["content"].lower()
    return any(t in text for t in refusal_terms) and len(result["citations"]) == 0


BEHAVIOR_CHECKS = {
    "answer_with_citation": answer_with_citation,
    "structured_answer_with_citation": structured_answer_with_citation,
    "multi_doc_answer": multi_doc_answer,
    "refute_with_citation": refute_with_citation,
    "not_found": not_found
}

# -------------------------
# Doc check
# -------------------------

def cites_expected_docs(result, expected_docs):
    # Checks if the citations are an exact match
    cited = {c["doc_title"] for c in result["citations"]}
    print(f"\nRETURNED:\n{cited}\n")
    print(f"\nEXPECTED:\n {expected_docs}\n")
    if(len(cited) != len(expected_docs)):
      return False
    return not any(doc not in cited for doc in expected_docs)



# -------------------------
# Eval runner
# -------------------------

async def run_eval():
    with open(Path.cwd() / "evals.json", "r") as file:
      tests = json.load(file)

    passed = 0
    failures = []

    for test in tests:
        print(f"\nQ{test['id']}: {test['question']}")
        result = await handle_message(test["question"])

        behavior = test["expected_behavior"]
        behavior_ok = BEHAVIOR_CHECKS[behavior](result)

        docs_ok = True
        if "expected_docs" in test:
            docs_ok = cites_expected_docs(result, test["expected_docs"])

        if behavior_ok and docs_ok:
            print("✅ PASS")
            passed += 1
        else:
            print("❌ FAIL")
            failures.append({
                "id": test["id"],
                "question": test["question"],
                "result": result,
                "expected_behavior": behavior,
                "expected_docs": test.get("expected_docs")
            })

    print("\n====================")
    print(f"Passed {passed}/{len(tests)} tests")
    print("====================")

    if failures:
        print("\nFailures:")
        for f in failures:
            print(f"- Q{f['id']}: {f['question']}")

if __name__ == "__main__":
    asyncio.run(run_eval())
'''9) Basic eval harness (small but powerful)

Feature
	•	A /evals JSON file with ~30 Q/A pairs + expected citations.
	•	Script that runs questions and scores:
	•	answer correctness (simple string/keyword match is fine),
	•	citation presence,
	•	“no hallucination” compliance.

Tests
	•	Run evals and print a tiny report: pass rate, failures, top missing docs.
  

  “We evaluate behavior deterministically by inspecting answer structure, 
  citation presence, and source attribution, rather than relying on LLM-based judges.”
  '''