ID:: 2605.02888v1
Type:: arXiv
Title:: SpecKV: Adaptive Speculative Decoding with Compression-Aware Gamma Selection
Authors:: Shikhar Shukla
Year:: 2026
URL:: https://arxiv.org/abs/2605.02888v1
Source:: arXiv:machine learning predict selec
Saved:: 2026-05-06
---

Speculative decoding accelerates large language model (LLM) inference by using a small draft model to propose candidate tokens that a larger target model verifies. A critical hyperparameter in this process is the speculation length~$γ$, which determines how many tokens the draft model proposes per step. Nearly all existing systems use a fixed~$γ$ (typically~4), yet empirical evidence suggests that the optimal value varies across task types and, crucially, depends on the compression level applied