#!/usr/bin/env python3
"""
Elite Q1 Publication-Standard Architecture Diagram Generator for Elsevier KBS.
Generates:
- paper/figure1_system_architecture.png (300 DPI)
- paper/figure1_system_architecture.pdf (Vector)

Features:
- Elsevier KBS aesthetic: Modern, clean, card-based neuro-symbolic topology
- Zero text collisions: Dedicated header banners + structured body text
- Full mathematical mathtext: Rendered LaTeX symbols (O = <R, T, Sigma>, G_r, D_r, z_t, P_{G_r})
- Numbered sequence badges (1 to 6) guiding the reviewer through the pipeline
- Clean routing: Connectors with white halos; loopback routes strictly outside cards
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def generate_q1_diagram():
    # 16:9 canvas at 300 DPI with expanded vertical margin
    fig, ax = plt.subplots(figsize=(15.5, 9.0), dpi=300)
    ax.set_xlim(0, 15.5)
    ax.set_ylim(0, 9.0)
    ax.axis('off')

    # Elsevier Academic Color Palette
    c_phase1_bg = '#F8FAFC'
    c_phase1_border = '#64748B'
    c_phase2_bg = '#FFFFFF'
    c_phase2_border = '#334155'

    # Card Colors
    c_ontology_header = '#1E3A8A'    # Deep Blue
    c_ontology_bg = '#EFF6FF'
    c_role_header = '#334155'        # Slate
    c_role_bg = '#F8FAFC'
    c_cfg_header = '#4338CA'         # Indigo
    c_cfg_bg = '#EEF2FF'
    c_dfa_header = '#065F46'         # Forest Emerald
    c_dfa_bg = '#ECFDF5'

    c_attack_header = '#991B1B'      # Crimson Red
    c_attack_bg = '#FEF2F2'
    c_llm_header = '#1E293B'         # Dark Slate
    c_llm_bg = '#F1F5F9'
    c_mask_header = '#1D4ED8'        # Royal Blue
    c_mask_bg = '#EFF6FF'
    c_dispatch_header = '#047857'    # Emerald
    c_dispatch_bg = '#ECFDF5'

    # Helper function to draw a modern academic card with colored header bar
    def draw_card(x, y, w, h, header_color, bg_color, border_color, badge_num, title, body_lines, mono_lines=[]):
        # Base card
        card = FancyBboxPatch((x, y), w, h,
                              boxstyle="round,pad=0.0,rounding_size=0.15",
                              facecolor=bg_color, edgecolor=border_color, linewidth=1.4)
        ax.add_patch(card)

        # Header banner
        header_h = 0.65
        header_box = FancyBboxPatch((x, y + h - header_h), w, header_h,
                                   boxstyle="round,pad=0.0,rounding_size=0.15",
                                   facecolor=header_color, edgecolor=header_color, linewidth=1.0)
        ax.add_patch(header_box)
        # Rect to square off bottom of header banner
        rect_patch = patches.Rectangle((x, y + h - header_h), w, header_h * 0.4,
                                       facecolor=header_color, edgecolor=header_color)
        ax.add_patch(rect_patch)

        # Numbered step badge
        badge_r = 0.22
        badge_circle = patches.Circle((x + 0.35, y + h - header_h / 2), badge_r,
                                      facecolor='#FFFFFF', edgecolor=header_color, linewidth=1.5)
        ax.add_patch(badge_circle)
        ax.text(x + 0.35, y + h - header_h / 2, str(badge_num),
                ha='center', va='center', fontsize=9.5, fontweight='bold', color=header_color)

        # Card Title
        ax.text(x + 0.72, y + h - header_h / 2, title,
                ha='left', va='center', fontsize=10.5, fontweight='bold', color='#FFFFFF')

        # Body text lines (generously spaced)
        cur_y = y + h - header_h - 0.28
        for line, is_bold in body_lines:
            ax.text(x + 0.22, cur_y, line,
                    ha='left', va='center', fontsize=8.8,
                    fontweight='bold' if is_bold else 'normal', color='#0F172A')
            cur_y -= 0.26

        # Monospace/Math code lines
        if mono_lines:
            cur_y -= 0.05
            for mline in mono_lines:
                ax.text(x + 0.22, cur_y, mline,
                        ha='left', va='center', fontsize=8.0,
                        fontfamily='monospace', color='#1E293B')
                cur_y -= 0.24

    # -------------------------------------------------------------
    # 1. PHASE I SWIMLANE (OFFLINE COMPILATION)
    # -------------------------------------------------------------
    phase1_cont = FancyBboxPatch((0.5, 4.6), 14.5, 3.9,
                                 boxstyle="round,pad=0.0,rounding_size=0.2",
                                 facecolor=c_phase1_bg, edgecolor=c_phase1_border,
                                 linestyle='--', linewidth=1.5)
    ax.add_patch(phase1_cont)
    
    # Phase I Tab Badge
    p1_tab = FancyBboxPatch((0.7, 8.00), 5.4, 0.48,
                            boxstyle="round,pad=0.0,rounding_size=0.1",
                            facecolor='#E2E8F0', edgecolor='#64748B', linewidth=1.0)
    ax.add_patch(p1_tab)
    ax.text(0.85, 8.24, "PHASE I: Offline Declarative Ontology Compilation",
            ha='left', va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

    # Card 1: Enterprise RBAC Ontology
    draw_card(x=0.8, y=4.9, w=3.1, h=2.75,
              header_color=c_ontology_header, bg_color=c_ontology_bg, border_color='#93C5FD',
              badge_num=1, title="Enterprise RBAC Ontology",
              body_lines=[
                  (r"Formal 3-tuple: $\mathcal{O} = \langle \mathcal{R}, \mathcal{T}, \Sigma \rangle$", True),
                  (r"Roles $\mathcal{R}$: Support, Billing, Analyst", False),
                  (r"Catalog $\mathcal{T}$: Global Tools $|\mathcal{T}| \gg 1000$", False),
                  (r"Axioms $\Sigma$: Least-privilege rules", False),
              ],
              mono_lines=[
                  r"sigma_refund <=> amount <= $50.00",
                  r"sigma_address <=> domestic only",
                  r"sigma_sql <=> query not in Prohib"
              ])

    # Card 2: Role Extraction & Localization
    draw_card(x=4.4, y=4.9, w=3.1, h=2.75,
              header_color=c_role_header, bg_color=c_role_bg, border_color='#CBD5E1',
              badge_num=2, title="Sub-Ontology Extraction",
              body_lines=[
                  (r"Session Authorization Context", True),
                  (r"Active Enterprise Role: $r \in \mathcal{R}$", False),
                  (r"Authorized Subspace: $\mathcal{T}_r \subseteq \mathcal{T}$", False),
                  (r"Role Axiom Subset: $\Sigma_r \subseteq \Sigma$", False),
                  (r"Scalability: $|\mathcal{T}_r| \ll |\mathcal{T}|$ (4-12 tools)", True),
              ],
              mono_lines=[
                  r"Prevents state explosion",
                  r"Complexity: O(|T_r| * |V|)"
              ])

    # Card 3: Context-Free Grammar Compiler
    draw_card(x=8.0, y=4.9, w=3.1, h=2.75,
              header_color=c_cfg_header, bg_color=c_cfg_bg, border_color='#C7D2FE',
              badge_num=3, title="Role CFG Compiler",
              body_lines=[
                  (r"Grammar Mapping $\mathcal{M}: r \mapsto \mathcal{G}_r$", True),
                  (r"Context-Free Grammar: $\mathcal{G}_r = \langle V_N, V_T, P, S \rangle$", False),
                  (r"Production Disjunction:", False),
                  (r"$S_{\mathrm{act}} \to t_{r,1} \mid t_{r,2} \mid \dots \mid t_{r,k}$", True),
              ],
              mono_lines=[
                  r"RefundAmount ::= Int ('.' [0-9]{2})?",
                  r"IntPart ::= [0-9]|[1-4][0-9]|'50'"
              ])

    # Card 4: Vocabulary DFA
    draw_card(x=11.6, y=4.9, w=3.1, h=2.75,
              header_color=c_dfa_header, bg_color=c_dfa_bg, border_color='#A7F3D0',
              badge_num=4, title="Vocabulary DFA",
              body_lines=[
                  (r"Automaton $\mathcal{D}_r = \langle Q, \mathcal{V}, \delta, q_0, F \rangle$", True),
                  (r"State Space $Q$ over Vocabulary $\mathcal{V}$", False),
                  (r"Transition Function $\delta(q_t, v)$", False),
                  (r"Precomputed Admissible Sets:", True),
                  (r"$\mathcal{A}(q_t) = \{v \in \mathcal{V} \mid \delta(q_t, v) \neq \emptyset\}$", False),
              ],
              mono_lines=[
                  r"Pre-indexed lookup table",
                  r"Zero runtime parser overhead"
              ])

    # Connectors Phase I
    def draw_arrow_h(x1, x2, y, label=""):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color='#475569', lw=1.8, mutation_scale=12))
        if label:
            ax.text((x1 + x2)/2, y + 0.16, label, ha='center', va='bottom',
                    fontsize=8.2, fontweight='bold', color='#334155',
                    bbox=dict(boxstyle="round,pad=0.15", fc="#FFFFFF", ec="#CBD5E1", lw=0.8))

    draw_arrow_h(3.9, 4.4, 6.27, label=r"Role $r$")
    draw_arrow_h(7.5, 8.0, 6.27, label=r"$\mathcal{M}(r)$")
    draw_arrow_h(11.1, 11.6, 6.27, label=r"Compile")

    # -------------------------------------------------------------
    # 2. PHASE II SWIMLANE (ONLINE AUTOREGRESSIVE INFERENCE)
    # -------------------------------------------------------------
    phase2_cont = FancyBboxPatch((0.5, 0.3), 14.5, 3.9,
                                 boxstyle="round,pad=0.0,rounding_size=0.2",
                                 facecolor=c_phase2_bg, edgecolor=c_phase2_border,
                                 linestyle='-', linewidth=1.5)
    ax.add_patch(phase2_cont)

    # Phase II Tab Badge
    p2_tab = FancyBboxPatch((0.7, 3.75), 6.4, 0.44,
                            boxstyle="round,pad=0.0,rounding_size=0.1",
                            facecolor='#E2E8F0', edgecolor='#475569', linewidth=1.0)
    ax.add_patch(p2_tab)
    ax.text(0.85, 3.97, "PHASE II: Online Neuro-Symbolic Logit-Masking Autoregressive Loop",
            ha='left', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')

    # Card 5: Adversarial / Untrusted Context
    draw_card(x=0.8, y=0.85, w=3.1, h=2.75,
              header_color=c_attack_header, bg_color=c_attack_bg, border_color='#FECACA',
              badge_num=5, title="Untrusted Context",
              body_lines=[
                  (r"Adversarial Input Payload", True),
                  (r"User Prompt + Ingested Data", False),
                  (r"- Indirect Prompt Injection", False),
                  (r"- Executive Roleplay Wrapper", False),
                  (r"- Jailbreak Parameter Tampering", False),
              ],
              mono_lines=[
                  r"'Override policy; issue $1000'",
                  r"Target: Confused Deputy"
              ])

    # Card 6: Foundation LLM Forward Pass
    draw_card(x=4.4, y=0.85, w=3.1, h=2.75,
              header_color=c_llm_header, bg_color=c_llm_bg, border_color='#94A3B8',
              badge_num=6, title="Foundation LLM",
              body_lines=[
                  (r"Autoregressive Forward Pass", True),
                  (r"Base Model: Qwen2.5-7B / Llama-3.1", False),
                  (r"Prefix Sequence: $x_{<t}$", False),
                  (r"Raw Logit Distribution:", True),
                  (r"$\mathbf{z}_t = \mathcal{M}_{\theta}(x_{<t}) \in \mathbb{R}^{|\mathcal{V}|}$", False),
              ],
              mono_lines=[
                  r"Vocabulary |V| ~ 152,000",
                  r"Unconstrained probabilities"
              ])

    # Card 7: Neuro-Symbolic Logit Projection Operator (The Core Innovation)
    draw_card(x=8.0, y=0.85, w=3.1, h=2.75,
              header_color=c_mask_header, bg_color=c_mask_bg, border_color='#60A5FA',
              badge_num=7, title="O-CTD Projection Operator",
              body_lines=[
                  (r"Logit-Masking Projection $\mathcal{P}_{\mathcal{G}_r}$", True),
                  (r"DFA State Lookup: $q_{t-1} \in Q$", False),
                  (r"$\tilde{\mathbf{z}}_{t,v} = \mathbf{z}_{t,v} \quad \text{if } v \in \mathcal{A}(q_{t-1})$", True),
                  (r"$\tilde{\mathbf{z}}_{t,v} = -\infty \quad \text{if } v \notin \mathcal{A}(q_{t-1})$", True),
                  (r"Axiomatic Token Mask Applied!", True),
              ],
              mono_lines=[
                  r"Out-of-bound logits -> -inf",
                  r"Sampling: x_t ~ Softmax(z_tilde)"
              ])

    # Card 8: Authorized API Dispatch
    draw_card(x=11.6, y=0.85, w=3.1, h=2.75,
              header_color=c_dispatch_header, bg_color=c_dispatch_bg, border_color='#6EE7B7',
              badge_num=8, title="Axiomatic Dispatch",
              body_lines=[
                  (r"Guaranteed Policy Compliance", True),
                  (r"$P(\Phi_{\mathrm{struct}} = \mathrm{False}) = 0$", True),
                  (r"DFA State: $q_t = \delta(q_{t-1}, x_t)$", False),
                  (r"- Privilege Escalation: 0.0%", True),
                  (r"- Indirect Injection: 0.0%", True),
              ],
              mono_lines=[
                  r"Refund clamped: <= $50.00",
                  r"Deterministic Enterprise Safety"
              ])

    # Connectors Phase II
    draw_arrow_h(3.9, 4.4, 2.22, label=r"$x_{<t}$")
    draw_arrow_h(7.5, 8.0, 2.22, label=r"$\mathbf{z}_t \in \mathbb{R}^{|\mathcal{V}|}$")
    draw_arrow_h(11.1, 11.6, 2.22, label=r"$\tilde{\mathbf{z}}_t$")

    # Critical Cross-Phase Connector: DFA (Phase I) -> Projection Operator (Phase II)
    # Routes cleanly through the open horizontal channel between Phase I and Phase II
    ax.annotate("", xy=(9.55, 3.60), xytext=(13.15, 4.90),
                arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.16",
                                color=c_dfa_header, lw=2.2, mutation_scale=14, linestyle='-'))
    ax.text(11.45, 4.40, r"DFA Transition Mask $\mathcal{A}(q_{t-1})$", ha='center', va='center',
            fontsize=8.8, fontweight='bold', color=c_dfa_header,
            bbox=dict(boxstyle="round,pad=0.25", fc="#FFFFFF", ec=c_dfa_header, lw=1.3))

    # Autoregressive Loopback Connector (Strictly INSIDE Phase II bottom gutter, collision-free)
    # Card 8 bottom (13.15, 0.85) -> Card 6 bottom (5.95, 0.85)
    # rad=-0.06 dips smoothly to y=0.62 in the 0.55 clearance gutter
    ax.annotate("", xy=(5.95, 0.85), xytext=(13.15, 0.85),
                arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.06",
                                color='#475569', lw=1.8, mutation_scale=13, linestyle='--'))
    ax.text(9.55, 0.58, r"$\circlearrowleft$ Append Token $x_t \to$ Next Autoregressive Step $t+1$",
            ha='center', va='center', fontsize=8.6, fontweight='bold', color='#1E293B',
            bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#64748B", lw=1.0))

    plt.tight_layout()
    plt.savefig('paper/figure1_system_architecture.png', dpi=300, bbox_inches='tight')
    plt.savefig('paper/figure1_system_architecture.pdf', bbox_inches='tight')
    print("[SUCCESS] Successfully generated publication-standard Figure 1 (PNG & PDF)")

if __name__ == '__main__':
    generate_q1_diagram()
