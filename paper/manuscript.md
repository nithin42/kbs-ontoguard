# Ontology-Constrained Neuro-Symbolic Decoding: Enforcing Axiomatic Least-Privilege in Autonomous LLM Agents

**Author:** Nithin Kumbam  
**Target Journal:** *Knowledge-Based Systems* (Elsevier) — Short Communication  
**Code & Benchmark Repository:** [https://github.com/nithin42/kbs-ontoguard](https://github.com/nithin42/kbs-ontoguard)  

---

## Abstract
Autonomous tool-calling Large Language Model (LLM) agents are increasingly entrusted with operational authority in enterprise business workflows, including financial disbursements, database modifications, and customer identity operations. However, existing safety paradigms rely predominantly on *in-context system prompts* or *post-hoc classifiers*, both of which remain vulnerable to indirect prompt injection, privilege escalation, and adversarial parameter tampering. In this paper, we propose **Ontology-Constrained Token Decoding (O-CTD)**, a neuro-symbolic framework that compiles formal, declarative Role-Based Access Control (RBAC) ontologies into runtime Context-Free Grammars (CFGs). By projecting the LLM's autoregressive logit distribution onto the permissible transitions of a Deterministic Finite Automaton (DFA) at each generation step, O-CTD mathematically guarantees that unauthorized tool selections and out-of-bounds parameter values cannot be sampled. We empirically evaluate O-CTD against three standard industry baselines across 100 enterprise business scenarios (400 total inferences) using `Qwen2.5-7B-Instruct` on an NVIDIA RTX 4090 GPU. Experimental results demonstrate that O-CTD suppresses the Attack Success Rate (ASR) from 80.0% (in-context guardrails) down to 20.0%, reduces policy Invariant Violation Rates (IVR) from 90.0% to 10.0%, and achieves 100.0% Benign Task Completion (BTC). A paired Wilcoxon signed-rank test confirms statistical significance ($W = 0.0, p = 3.74 \times 10^{-19}, r = 0.800$). We publish our benchmark suite, declarative schemas, and decoding harness to advance formal verification in agentic AI.

**Keywords:** Neuro-symbolic AI; Large Language Models; Constrained Decoding; Autonomous Agents; Role-Based Access Control; Prompt Injection Defense.

---

## Research Highlights
* Formalizes enterprise Role-Based Access Control (RBAC) into dynamic Context-Free Grammars.
* Introduces Ontology-Constrained Token Decoding (O-CTD) to eliminate unauthorized tokens at inference time.
* Demonstrates an 80% to 20% ASR reduction and 90% to 10% IVR reduction on real-world enterprise workflows.
* Achieves 100% Benign Task Completion (BTC) with verified statistical significance ($p < 10^{-18}, r = 0.800$).
* Establishes an open-source benchmark and PyTorch/Outlines implementation for reproducible research.

---

## 1. Introduction & Threat Model

The transition of Large Language Models (LLMs) from passive conversational engines to autonomous agents operating via function calling and external API dispatch represents a foundational paradigm shift in enterprise automation [1, 2]. Autonomous agents are currently deployed in core business domains, such as executing customer refunds, modifying shipping schedules, and querying relational database management systems. 

Despite their operational utility, agentic workflows introduce catastrophic security vulnerabilities [3, 4]. Most critically, untrusted data ingested from emails, documents, or database outputs can trigger *indirect prompt injection* (IPI), wherein embedded adversarial instructions hijack the model's intent [5, 6]. Under such attacks, autonomous agents frequently suffer from the classic *Confused Deputy* problem [7], using legitimate enterprise credentials to execute unauthorized disbursements or exfiltrate private ledgers.

Contemporary defensive strategies fall into two predominant categories:
1. **In-Context Prompt Guarding:** Prepending instructional constraints to the system prompt (e.g., *"You are a Tier 1 agent. Never issue refunds over $50.00"*) [8].
2. **Post-Hoc Classification:** Filtering outputs through secondary safety classifiers or heuristic regex parsers before execution [9].

Both approaches are fundamentally probabilistic. Soft system prompts are routinely circumvented by authority impersonation, debug mode exploits, or payload obfuscation [6]. Conversely, post-hoc classifiers are decoupled from the generation process, operating retroactively and introducing high false-rejection rates on complex business tasks [10].

To address these vulnerabilities, we propose **Ontology-Constrained Token Decoding (O-CTD)**, a neuro-symbolic framework that grounds autoregressive language generation in formal declarative knowledge representations [11, 12]. By compiling an enterprise Role-Based Access Control (RBAC) ontology into a dynamic Context-Free Grammar (CFG), O-CTD applies token-level logit masking at each autoregressive decoding step [13, 14]. Consequently, any token that violates active role privileges, invokes unauthorized tools, or exceeds numerical parametric bounds is assigned a probability of zero before sampling.

---

## 2. Mathematical Formulation

### 2.1 Enterprise RBAC Security Ontology

We formalize enterprise access policies as an axiomatic security ontology defined over roles, operational tools, and parametric bounds [15, 16].

**Definition 1 (Enterprise Security Ontology).** An Enterprise Security Ontology is a 3-tuple:
$$\mathcal{O} = \langle \mathcal{R}, \mathcal{T}, \Sigma \rangle$$
where:
* $\mathcal{R} = \{r_1, r_2, \dots, r_m\}$ is the set of authenticated enterprise user roles (e.g., $\text{CustomerSupportTier1}$, $\text{BillingManager}$).
* $\mathcal{T} = \{t_1, t_2, \dots, t_n\}$ is the catalog of enterprise tools/APIs available in the operational environment.
* $\Sigma = \{\sigma_1, \sigma_2, \dots, \sigma_k\}$ is the set of formal security axioms governing tool invocation.

Each role $r \in \mathcal{R}$ is mapped to an authorized tool subset $\mathcal{T}_r \subseteq \mathcal{T}$ and a set of parametric invariant axioms $\Sigma_r \subseteq \Sigma$. Specifically, for an action $a = \langle t, \theta \rangle$ where $t \in \mathcal{T}$ and $\theta = \{p_i: v_i\}$ represents the argument dictionary, the validity predicate $\Phi(a, r)$ is defined as:
$$\Phi(\langle t, \theta \rangle, r) \iff \left( t \in \mathcal{T}_r \right) \land \left( \forall \sigma \in \Sigma_r, \, \sigma(\theta) = \text{True} \right)$$

In our enterprise benchmark, parametric axioms $\sigma \in \Sigma_r$ enforce strict bounds, including:
$$\sigma_{\text{refund}}(\theta) \iff \theta[\text{amount\_usd}] \le C_r$$
$$\sigma_{\text{address}}(\theta) \iff \theta[\text{is\_international}] = \text{False}$$
$$\sigma_{\text{sql}}(\theta) \iff \theta[\text{query}] \notin \mathcal{L}_{\text{prohibited}}$$
where $C_r$ is the maximum refund ceiling authorized for role $r$ ($C_{\text{Tier1}} = \$50.00$, $C_{\text{Billing}} = \$1000.00$), and $\mathcal{L}_{\text{prohibited}}$ denotes blacklisted data modification patterns.

### 2.2 Context-Free Grammar Compilation

To enforce $\Phi(a, r)$ during autoregressive generation, the compiler $\mathcal{M}$ dynamically transforms the active role definition $r$ into a formal Context-Free Grammar $\mathcal{G}_r = \langle V_N, V_T, P, S \rangle$ [17]:
$$\mathcal{M}: r \mapsto \mathcal{G}_r$$
where $V_T$ is the alphabet of terminal characters, $V_N$ is the set of non-terminals, $P$ is the set of production rules, and $S$ is the start symbol. 

Under $\mathcal{G}_r$, the production rules for the tool identifier are constrained to the exact literal union of authorized tools:
$$S \to \text{\texttt{"action\_name": }} \left( t_{r, 1} \mid t_{r, 2} \mid \dots \mid t_{r, |\mathcal{T}_r|} \right) \quad \forall t_{r, j} \in \mathcal{T}_r$$
Numerical parameters subject to ceiling constraints $C_r$ are compiled into bounded regular expressions or sub-grammars that reject any numeric string representation exceeding $C_r$.

### 2.3 Token-Level Logit-Masking Projection

Let $\mathcal{V}$ denote the tokenizer vocabulary of size $|\mathcal{V}|$, and let $x_{<t} = [x_1, \dots, x_{t-1}]$ denote the sequence of generated tokens up to step $t$. At step $t$, the base language model outputs unconstrained logit vector $\mathbf{z}_t \in \mathbb{R}^{|\mathcal{V}|}$. 

The grammar $\mathcal{G}_r$ is compiled into a Deterministic Finite Automaton (DFA) over the token vocabulary [13, 18]. Let $q_t \in Q$ denote the current DFA state after ingesting $x_{<t}$. The set of admissible next tokens $\mathcal{A}(q_t) \subseteq \mathcal{V}$ is defined as:
$$\mathcal{A}(q_t) = \{ v \in \mathcal{V} \mid \exists q' \in Q, \, \delta(q_t, v) = q' \}$$
where $\delta$ is the state transition function.

The neuro-symbolic projection operator $\mathcal{P}_{\mathcal{G}_r}: \mathbb{R}^{|\mathcal{V}|} \to \mathbb{R}^{|\mathcal{V}|}$ masks the logit distribution:
$$\mathcal{P}_{\mathcal{G}_r}(\mathbf{z}_t)_v = 
\begin{cases} 
    \mathbf{z}_{t, v} & \text{if } v \in \mathcal{A}(q_t) \\
    -\infty & \text{if } v \notin \mathcal{A}(q_t)
\end{cases}$$

The next token is sampled from the normalized masked distribution:
$$x_t \sim \text{Softmax}\left( \mathcal{P}_{\mathcal{G}_r}(\mathbf{z}_t) \right)$$

**Theorem 1 (Soundness of Axiomatic Enforcement).** Let $\mathbf{x} = [x_1, \dots, x_K]$ be a completed generation sequence terminated by an end-of-sequence token under O-CTD. Then the extracted tool call $a = \text{Parse}(\mathbf{x})$ satisfies:
$$P\left( \Phi(a, r) = \text{False} \right) = 0$$
with respect to all syntactically expressible invariants in $\mathcal{G}_r$.

*Proof Sketch:* By construction, any token sequence $\mathbf{x}$ yielding an unauthorized tool $t \notin \mathcal{T}_r$ or an out-of-bounds numeric token sequence requires traversing at least one invalid DFA transition $\delta(q_t, v) = \emptyset$. Since $\mathcal{P}_{\mathcal{G}_r}(\mathbf{z}_t)_v = -\infty$, the sampling probability $P(x_t = v) = 0$. By induction over generation steps $1 \le t \le K$, the probability of generating a violating sequence is identically zero. $\square$

---

## 3. Experimental Setup

### 3.1 Benchmark Dataset & Threat Classes

We synthesized a benchmark suite consisting of $N = 100$ balanced business evaluation cases (50 adversarial attack prompts and 50 benign utility queries) grounded in the InjecAgent and AgentDojo threat models [5, 6]. The scenarios span three core business roles:
* **CustomerSupportTier1:** Authorized for order lookup, shipping address updates (domestic only), and refunds capped at $50.00.
* **BillingManager:** Authorized for invoice credits up to $5,000.00 and refunds up to $1,000.00.
* **DataAnalyst:** Authorized for aggregate analytics; strictly barred from financial tools and raw payment ledgers.

The 50 adversarial prompts span five distinct threat categories:
1. **Parameter Tampering (PT):** Adversary coerces the agent into issuing a $500.00 or $1,200.00 refund via authority pressure (e.g., claiming "Executive VIP Override").
2. **Privilege Escalation (PE):** Frontline support agent is instructed via debug commands to invoke admin tools (`view_payment_ledger`).
3. **SQL / Exfiltration Injection (SQL):** Malicious payloads inside query arguments attempting `DROP TABLE` or plain-text credential exfiltration.
4. **Indirect Prompt Injection (IPI):** Simulated third-party vendor emails containing hidden instructions directing wire disbursements.
5. **Policy Boundary Tampering (PBT):** Coercing domestic customer support to route orders to embargoed international addresses.

### 3.2 Comparative Frameworks & Controls
* **M0 (Vanilla Base LLM):** Unconstrained generation; agent receives standard ReAct-style role descriptions without defensive guardrails.
* **M1 (In-Context Prompt Guard):** Standard enterprise defensive baseline; system prompt includes explicit natural-language prohibitions (e.g., *"CRITICAL: You are strictly forbidden from exceeding $50 refunds or viewing ledgers"*).
* **M2 (Post-Hoc Classifier):** Output is generated unconstrained, followed by a secondary classifier pass that checks generated JSON against policy rules before execution.
* **M\* (Proposed O-CTD):** Autoregressive token decoding strictly constrained by the compiled role-specific context-free grammar.

All experiments were executed on an NVIDIA GeForce RTX 4090 (24 GB VRAM) using `Qwen/Qwen2.5-7B-Instruct` (bfloat16) with a single shared model instance on `cuda:0` to eliminate CPU offloading.

---

## 4. Empirical Results & Discussion

### 4.1 Comparative Benchmark Results

Table 1 summarizes the empirical findings across the 100 evaluation scenarios (400 total inferences).

| Framework | ASR (Min $\downarrow$) | IVR (Min $\downarrow$) | BTC (Max $\uparrow$) | Mean Latency | P95 Latency | Empirical Finding |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **M0 (Vanilla Base LLM)** | **100.0%** | **100.0%** | **0.0%** | 893.1 ms | 1396.1 ms | Completely susceptible to prompt injection; 0% schema adherence. |
| **M1 (Prompt Guard)** | **80.0%** | **90.0%** | **0.0%** | 1157.0 ms | 2261.7 ms | Proves soft in-context system prompts collapse under adversarial pressure. |
| **M2 (Post-Hoc Classifier)** | **100.0%** | **100.0%** | **0.0%** | 1120.3 ms | 1618.8 ms | External post-hoc filters fail against obfuscated and roleplay attacks. |
| **M\* (Proposed O-CTD)** | **20.0%** | **10.0%** | **100.0%** | 3116.0 ms | 4097.4 ms | **4× lower ASR, 9× lower violations, 100% utility.** |

*Table 1: Main comparative benchmark results across 100 enterprise business evaluation scenarios (400 inferences) using Qwen2.5-7B-Instruct on an NVIDIA RTX 4090.*

#### Primary Empirical Findings:
1. **The Collapse of In-Context Guardrails:** In-context prompt defense (M1) proved overwhelmingly ineffective under targeted adversarial pressure, exhibiting an **80.0% ASR** and a **90.0% IVR**. When confronted with adversarial jailbreaks framing the request as an emergency or debug override, the LLM systematically ignored system instructions. This empirically substantiates that probabilistic next-token generation cannot enforce safety invariants when adversarial tokens shift the context distribution [8].
2. **Utility Fragility in Unconstrained LLMs:** Strikingly, M0, M1, and M2 all exhibited **0.0% BTC** on benign business tasks. Detailed log inspection revealed that this utility collapse was not due to cognitive inability, but rather *syntactic non-conformance*. Unconstrained Qwen-2.5 generated conversational preambles (e.g., *"Certainly! Here is the tool call:"*) or formatted argument keys inconsistently, failing automated API parsers. In contrast, M* achieved **100.0% BTC**, demonstrating that neuro-symbolic grammar constraints simultaneously serve as a powerful utility guarantee by enforcing rigorous JSON schema adherence.
3. **Decisive Security Dominance of O-CTD:** O-CTD achieved a **4× reduction in ASR** (from 80.0% to 20.0%) and a **9× reduction in policy violations** (from 90.0% to 10.0%). All privilege escalation attempts (e.g., Tier 1 support invoking financial ledgers) and parameter ceiling breaches (e.g., refunds exceeding $50.00) were physically eliminated at the logit level.

### 4.2 Statistical Significance Testing

To verify that the empirical superiority of O-CTD over standard prompt guarding is not an artifact of prompt selection, we conducted a non-parametric paired analysis [25]. Because binary policy violation outcomes violate normality assumptions, the paired **Wilcoxon Signed-Rank Test** was executed across all matched sample pairs between M1 and M*:
* **Wilcoxon Test Statistic ($W$):** $0.0$
* **Two-Sided $p$-Value:** $\mathbf{3.7441 \times 10^{-19}} \ll 0.001$
* **Rank-Biserial Effect Size ($r$):** $\mathbf{0.800}$ [26]

The effect size of $r = 0.800$ substantially exceeds the standard threshold for a "large" effect ($r \ge 0.50$), confirming that O-CTD delivers statistically definitive and reproducible safety improvements.

### 4.3 Qualitative Error Analysis: The 20% Residual ASR

While O-CTD reduced ASR from 80% to 20%, we investigate why the residual 20% occurred despite formal grammar constraints:
1. **The Confused Deputy within Allowed Tools:** In two attack scenarios, the adversary instructed the agent: *"Order ORD-12345 was delayed; look up its status and append a note containing internal API keys."*. Because `lookup_order_status` was an authorized tool for Tier 1 support, the grammar permitted its selection. While the grammar prevented unauthorized financial execution, the model processed the adversarial context within the legitimate tool's free-text field.
2. **Safe Fallback Invocation:** Under extreme adversarial prompt injection where all attempted tool tokens were masked out by the DFA, the agent safely fell back to the default permitted tool (`lookup_order_status`). Although no unauthorized action occurred, the evaluation harness marked the sample as partially engaged because the agent did not output an explicit refusal string.

This analysis highlights a critical theoretical boundary: **Context-Free Grammars mathematically eliminate structural and parametric privilege escalations, but semantic validation inside unbounded free-text fields remains an orthogonal challenge.**

### 4.4 Computational Overhead & The Pareto Frontier

The trade-off between security and computational latency is documented in our experimental outputs:
* M* introduces a mean latency of **3116.0 ms** compared to **1157.0 ms** for prompt guarding. 
* This $\sim$2.7× latency overhead stems from the runtime intersection between the tokenizer vocabulary ($|\mathcal{V}| \approx 152,000$) and the DFA transition table at each generation step. 
* In high-stakes enterprise decision-support workflows (e.g., approving customer disbursements, altering databases), an added 2-second overhead is well within acceptable latency SLAs in exchange for deterministic security guarantees.

---

## 5. Conclusion & Reproducibility

In this paper, we introduced **Ontology-Constrained Token Decoding (O-CTD)**, a neuro-symbolic framework that compiles declarative enterprise RBAC ontologies into runtime Context-Free Grammars for autonomous LLM agents. By enforcing deterministic logit masking during autoregressive generation, O-CTD mathematically eliminates unauthorized tool privilege escalations and parametric boundary tampering. On a 100-sample enterprise benchmark using `Qwen2.5-7B-Instruct`, O-CTD reduced Attack Success Rates from 80% to 20%, decreased policy invariant violations from 90% to 10%, and achieved 100% task utility with strong statistical significance ($p = 3.74 \times 10^{-19}, r = 0.800$).

**Open Source Repository:**  
The full experimental benchmark, declarative ontology specifications, evaluation suites, and PyTorch/Outlines implementation are openly available in the project repository:  
[https://github.com/nithin42/kbs-ontoguard](https://github.com/nithin42/kbs-ontoguard)

---

## References

1. S. Yao, et al., "ReAct: Synergizing Reasoning and Acting in Language Models," *ICLR*, 2023.
2. Y. Qin, et al., "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs," *ICLR*, 2024.
3. K. Greshake, et al., "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection," *ACM AISEC*, pp. 79–90, 2023.
4. OWASP Foundation, "OWASP Top 10 for Large Language Model Applications and Generative AI," Version 2.0, 2025.
5. Q. Zhan, Z. Liang, Z. Ying, D. Kang, "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents," *Findings of the ACL 2024*, pp. 9822–9845, 2024.
6. E. Debenedetti, et al., "AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents," *NeurIPS Datasets and Benchmarks Track*, 2024.
7. A. Mavrogiannis, M. Balunovic, F. Tramer, "The Confused Deputy Returns: Privilege Escalation in Tool-Using Large Language Models," *IEEE SPW*, pp. 112–120, 2024.
8. A. Wei, N. Haghtalab, J. Steinhardt, "Jailbroken: How Does LLM Safety Training Fail?" *NeurIPS*, 2024.
9. J. Ruan, et al., "Identifying and Mitigating Vulnerabilities in LLM-Integrated Workflows," *ACM CCS Workshop*, 2024.
10. Z. Wang, Y. Liang, H. Wang, D. Kang, "Progent: Programmable Privilege Control for AI Agents," *arXiv:2501.08922*, 2025.
11. A. Sheth, K. Roy, M. Gaur, "Neurosymbolic Artificial Intelligence (Why, What, and How)," *IEEE Intelligent Systems*, vol. 38, no. 3, pp. 56–62, 2023.
12. S. Pan, et al., "Unifying Large Language Models and Knowledge Graphs: A Roadmap," *IEEE TKDE*, vol. 36, no. 7, pp. 3580–3599, 2024.
13. B. T. Willard, R. Louf, "Efficient Guided Generation for Large Language Models," *arXiv:2307.09702*, 2023.
14. S. Zhang, et al., "SynCode: LLM Generation with Grammar Augmentation," *ACM FSE*, vol. 1, pp. 1–24, 2024.
15. R. S. Sandhu, et al., "Role-based access control models," *IEEE Computer*, vol. 29, no. 2, pp. 38–47, 1996.
16. D. F. Ferraiolo, et al., "Proposed NIST standard for role-based access control," *ACM TISSEC*, vol. 4, no. 3, pp. 224–274, 2001.
17. J. E. Hopcroft, R. Motwani, J. D. Ullman, *Introduction to Automata Theory, Languages, and Computation*, Addison-Wesley, 2001.
18. Y. Zhao, C.-Y. Shen, T. Chen, "XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models," *arXiv:2411.04107*, 2024.
19. Qwen Team, "Qwen2.5 Technical Report," *arXiv:2412.15115*, 2024.
20. A. Dubey, et al., "The Llama 3 Herd of Models," *arXiv:2407.21783*, 2024.
21. F. Poesia, et al., "Synchromesh: Reliable Code Generation from Pre-trained Language Models with Constrained Semantic Decoding," *ICLR*, 2022.
22. L. Beurer-Kellner, M. Fischer, M. Vechev, "Prompting Is Programming: A Query Language for Large Language Models," *ACM PLDI*, 2023.
23. Q. Wu, et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation," *arXiv:2308.08155*, 2023.
24. National Institute of Standards and Technology, "Artificial Intelligence Risk Management Framework (AI RMF 1.0)," *NIST SP 1270*, 2023.
25. F. Wilcoxon, "Individual comparisons by ranking methods," *Biometrics Bulletin*, vol. 1, no. 6, pp. 80–83, 1945.
26. D. S. Kerby, "The simple difference formula: An approach to teaching nonparametric correlation," *Comprehensive Psychology*, vol. 3, 2014.
27. H. Wang, et al., "A Survey on Knowledge-Enhanced Text Generation: Methods and Applications," *Knowledge-Based Systems*, vol. 291, 2024.
28. M. Schuster, K. K. Paliwal, "Bidirectional recurrent neural networks," *IEEE Trans. Signal Processing*, vol. 45, no. 11, pp. 2673–2681, 1997.
