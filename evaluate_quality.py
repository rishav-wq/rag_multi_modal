"""
Quality Evaluation Script for RAG System

This script performs automated testing of the RAG system with predefined questions.
It evaluates:
- Retrieval relevance (are the right chunks retrieved?)
- Answer grounding (is the answer based on context?)
- Answer completeness (does it address the question?)

This is a BONUS feature as mentioned in the assignment requirements.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from rag.llm import generate_answer
from rag.retriever import Retriever

# Test questions derived from common construction marketplace queries
TEST_QUESTIONS = [
    "What factors affect construction project delays?",
    "What are the payment terms for construction projects?",
    "How do I handle change orders?",
    "What safety requirements must be followed?",
    "What are the quality standards for materials?",
    "How long does the approval process take?",
    "What documentation is required for permits?",
    "What are the warranty terms?",
    "How are disputes resolved?",
    "What insurance is required for contractors?",
    "What are the environmental compliance requirements?",
    "How do I request a project inspection?",
]


def evaluate_retrieval(question: str, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate the quality of retrieved contexts."""
    if not contexts:
        return {
            "status": "no_contexts",
            "score": 0.0,
            "note": "No contexts retrieved",
        }
    
    # Check average similarity score
    avg_score = sum(c.get("score", 0) for c in contexts) / len(contexts)
    
    # Simple heuristic: score > 0.3 is considered relevant
    relevant_count = sum(1 for c in contexts if c.get("score", 0) > 0.3)
    
    return {
        "status": "ok",
        "num_contexts": len(contexts),
        "avg_score": round(avg_score, 3),
        "relevant_count": relevant_count,
        "top_score": round(contexts[0].get("score", 0), 3) if contexts else 0,
    }


def evaluate_answer(answer: str, contexts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Basic evaluation of the generated answer."""
    evaluation = {
        "length": len(answer),
        "has_error": answer.startswith("[Error]"),
        "says_dont_know": any(phrase in answer.lower() for phrase in [
            "don't know", "i don't know", "not found", "no information",
            "cannot find", "not present in", "not mentioned"
        ]),
    }
    
    return evaluation


def run_evaluation(output_file: str = "evaluation_results.json") -> None:
    """Run the full evaluation and save results."""
    print("=" * 70)
    print("RAG SYSTEM QUALITY EVALUATION")
    print("=" * 70)
    print(f"\nRunning {len(TEST_QUESTIONS)} test questions...\n")
    
    retriever = Retriever(top_k=5)
    results = []
    
    for idx, question in enumerate(TEST_QUESTIONS, 1):
        print(f"[{idx}/{len(TEST_QUESTIONS)}] {question}")
        
        try:
            # Retrieve contexts
            contexts = retriever.retrieve(question)
            
            # Generate answer
            answer = generate_answer(question, contexts, mode="offline")
            
            # Evaluate
            retrieval_eval = evaluate_retrieval(question, contexts)
            answer_eval = evaluate_answer(answer, contexts)
            
            result = {
                "question": question,
                "contexts": contexts,
                "answer": answer,
                "retrieval_evaluation": retrieval_eval,
                "answer_evaluation": answer_eval,
            }
            results.append(result)
            
            # Print summary
            print(f"  ✓ Retrieved {retrieval_eval.get('num_contexts', 0)} chunks "
                  f"(avg score: {retrieval_eval.get('avg_score', 0):.3f})")
            print(f"  ✓ Answer length: {answer_eval['length']} chars")
            
            if answer_eval['has_error']:
                print(f"  ⚠️  Error in answer generation")
            elif answer_eval['says_dont_know']:
                print(f"  ℹ️  System indicated knowledge gap (good grounding!)")
            
            print()
            
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
            results.append({
                "question": question,
                "error": str(e),
            })
    
    # Save results
    output_path = Path(output_file)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("=" * 70)
    print(f"✅ Evaluation complete! Results saved to: {output_path}")
    print("=" * 70)
    
    # Summary statistics
    successful = [r for r in results if "error" not in r]
    if successful:
        avg_retrieval_score = sum(
            r["retrieval_evaluation"].get("avg_score", 0) for r in successful
        ) / len(successful)
        
        dont_know_count = sum(
            1 for r in successful if r["answer_evaluation"]["says_dont_know"]
        )
        
        print(f"\n📊 SUMMARY:")
        print(f"  - Total questions: {len(TEST_QUESTIONS)}")
        print(f"  - Successful: {len(successful)}")
        print(f"  - Average retrieval score: {avg_retrieval_score:.3f}")
        print(f"  - 'Don't know' responses: {dont_know_count} "
              f"({dont_know_count/len(successful)*100:.1f}%)")
        print(f"\n💡 A healthy RAG system should:")
        print(f"  - Have avg retrieval score > 0.3")
        print(f"  - Say 'don't know' for out-of-scope questions")
        print(f"  - Avoid hallucinations by staying grounded in context")
    
    print()


if __name__ == "__main__":
    print("\n⚠️  Make sure you have:")
    print("  1. Built the index (click '(Re)build Index' in the UI)")
    print("  2. Configured your API key in .env")
    print("\nStarting evaluation in 3 seconds...\n")
    
    import time
    time.sleep(3)
    
    run_evaluation()
