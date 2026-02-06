# 📊 Quality Evaluation Results

## Test Setup
- **12 construction-related questions** from assignment documents
- **Evaluated:** Retrieval relevance, grounding, hallucination detection
- **Compared:** Online (Groq) vs Offline (phi3:mini) performance

---

## 🌐 Online Mode: Groq (llama-3.1-8b-instant)

| Metric | Result | Analysis |
|--------|--------|----------|
| **Questions Completed** | 6/12 | ⚠️ Hit rate limit at question 7 (6000 tokens/min) |
| **Avg Retrieval Score** | 0.352 | ✅ Above 0.3 threshold (good relevance) |
| **"Don't Know" Responses** | 2/6 (33%) | ✅ Conservative - admits knowledge gaps |
| **Hallucinations** | 0 | ✅ All answers grounded in context |
| **Latency** | ~1-2 sec/question | ⚡ Very fast |

**Strengths:**
- ✅ Ultra-fast response times
- ✅ High quality, concise answers
- ✅ Good grounding - says "don't know" when appropriate

**Limitations:**
- ⚠️ Free tier rate limits (6000 tokens/min)
- ⚠️ Requires internet connection
- ⚠️ API key needed

---

## 💻 Offline Mode: phi3:mini (3.8B params via Ollama)

| Metric | Result | Analysis |
|--------|--------|----------|
| **Questions Completed** | 12/12 | ✅ All completed successfully |
| **Avg Retrieval Score** | 0.311 | ✅ Above 0.3 threshold (good relevance) |
| **"Don't Know" Responses** | 1/12 (8.3%) | ℹ️ More confident, attempts more answers |
| **Hallucinations** | 0 | ✅ All answers grounded in context |
| **Latency** | ~10-30 sec/question | 🐢 Slower but acceptable |

**Strengths:**
- ✅ No rate limits - unlimited questions
- ✅ Works offline - no internet needed
- ✅ Free - no API costs
- ✅ Privacy - data stays local

**Limitations:**
- ⚠️ Slower response times (10-30x vs Groq)
- ⚠️ Requires 2.3GB disk space for model
- ⚠️ More verbose answers (not always concise)

---

## 🎯 Comparison Summary

| Aspect | Online (Groq) | Offline (phi3:mini) | Winner |
|--------|---------------|---------------------|--------|
| **Speed** | 1-2 sec | 10-30 sec | 🏆 Online |
| **Reliability** | Rate limited | Unlimited | 🏆 Offline |
| **Answer Quality** | Concise, focused | Detailed, verbose | 🏆 Online |
| **Grounding** | Conservative (33%) | Confident (8.3%) | 🏆 Online |
| **Privacy** | Cloud-based | Local | 🏆 Offline |
| **Cost** | Free tier limits | Completely free | 🏆 Offline |

**Recommendation:**
- **Production/Demo:** Use **Groq** for best user experience (speed + quality)
- **Development/Testing:** Use **phi3:mini** for unlimited testing
- **Privacy-critical:** Use **phi3:mini** to keep data local

## 🔍 Key Findings

1. ✅ **Both modes avoid hallucinations** - 100% grounded in context
2. ✅ **Retrieval quality consistent** - ~0.3 avg score in both modes
3. ⚡ **Groq 10-30x faster** - better for real-time chat
4. 🔒 **phi3:mini more reliable** - no rate limits or outages
5. 🎯 **Groq more cautious** - says "don't know" more often (better grounding)

## 🧪 Run Evaluation Yourself

```powershell
python evaluate_quality.py
```

To switch between modes, edit line 95 in `evaluate_quality.py`:
- `mode="online"` - Uses Groq (fast, rate limited)
- `mode="offline"` - Uses phi3:mini (slower, unlimited)
