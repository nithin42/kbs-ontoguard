#!/usr/bin/env python3
"""
Generate Publication-Grade System Architecture Diagram for O-CTD.
Illustrates:
- Phase I: Offline Ontology-to-DFA Compilation Pipeline
- Phase II: Online Neuro-Symbolic Logit-Masking Autoregressive Loop
Outputs:
- paper/figure1_system_architecture.png (300 DPI)
- paper/figure1_system_architecture.pdf (Vector)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle

def create_architecture_diagram():
    fig = plt.figure(figsize=(12, 6.5), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Color Palette (Elsevier Academic Clean)
    c_blue_border = '#1E3A8A'
    c_blue_bg = '#EFF6FF'
    c_indigo_border = '#4338CA'
    c_indigo_bg = '#EEF2FF'
    c_green_border = '#065F46'
    c_green_bg = '#ECFDF5'
    c_red_border = '#991B1B'
    c_red_bg = '#FEF2F2'
    c_slate_border = '#334155'
    c_slate_bg = '#F8FAFC'
    c_text_dark = '#0F172A'

    # -------------------------------------------------------------
    # 1. PHASE I: OFFLINE COMPILATION CONTAINER
    # -------------------------------------------------------------
    phase1_box = FancyBboxPatch((0.4, 3.4), 11.2, 2.7,
                                boxstyle="round,pad=0.2,rounding_size=0.2",
                                facecolor='#F1F5F9', edgecolor='#94A3B8',
                                linestyle='--', linewidth=1.5)
    ax.add_patch(phase1_box)
    ax.text(0.6, 5.85, "PHASE I: Offline Declarative Ontology Compilation",
            fontsize=11, fontweight='bold', color=c_slate_border)

    # Box 1A: Enterprise RBAC Ontology O = <R, T, Sigma>
    box_1a = FancyBboxPatch((0.7, 3.8), 2.7, 1.7,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=c_blue_bg, edgecolor=c_blue_border, linewidth=1.5)
    ax.add_patch(box_1a)
    ax.text(2.05, 5.15, "Enterprise RBAC Ontology (O)", ha='center', fontsize=9.5, fontweight='bold', color=c_blue_border)
    ax.text(2.05, 4.75, "Roles: R = {r1, r2, ...}\nTools: T = {t1, t2, ...}\nAxioms: Sigma = {sigma1, ...}\nBounds: C_r <= $50.00",
            ha='center', fontsize=8, color=c_text_dark, family='sans-serif')

    # Arrow 1A -> 1B
    ax.annotate("", xy=(3.8, 4.65), xytext=(3.4, 4.65),
                arrowprops=dict(arrowstyle="->", color='#475569', lw=1.8))
    ax.text(3.6, 4.85, "Role r", ha='center', fontsize=8, fontstyle='italic', color='#475569')

    # Box 1B: Role Sub-Ontology Extraction
    box_1b = FancyBboxPatch((3.8, 3.8), 2.3, 1.7,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=c_slate_bg, edgecolor=c_slate_border, linewidth=1.5)
    ax.add_patch(box_1b)
    ax.text(4.95, 5.15, "Role Extraction", ha='center', fontsize=9.5, fontweight='bold', color=c_slate_border)
    ax.text(4.95, 4.7, "Active Role r in R\nT_r subseteq T\nSigma_r subseteq Sigma\n(Localization O(|T_r|))",
            ha='center', fontsize=8, color=c_text_dark)

    # Arrow 1B -> 1C
    ax.annotate("", xy=(6.5, 4.65), xytext=(6.1, 4.65),
                arrowprops=dict(arrowstyle="->", color='#475569', lw=1.8))
    ax.text(6.3, 4.85, "M(r)", ha='center', fontsize=8.5, fontweight='bold', color='#475569')

    # Box 1C: CFG Schema Compiler G_r
    box_1c = FancyBboxPatch((6.5, 3.8), 2.3, 1.7,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=c_indigo_bg, edgecolor=c_indigo_border, linewidth=1.5)
    ax.add_patch(box_1c)
    ax.text(7.65, 5.15, "CFG Compiler (G_r)", ha='center', fontsize=9.5, fontweight='bold', color=c_indigo_border)
    ax.text(7.65, 4.7, "Grammar Rules P\nAction disjunction:\nS -> t_{r,1} | ... | t_{r,k}\nNumeric BPE EBNF",
            ha='center', fontsize=8, color=c_text_dark)

    # Arrow 1C -> 1D
    ax.annotate("", xy=(9.2, 4.65), xytext=(8.8, 4.65),
                arrowprops=dict(arrowstyle="->", color='#475569', lw=1.8))
    ax.text(9.0, 4.85, "Build", ha='center', fontsize=8, fontstyle='italic', color='#475569')

    # Box 1D: Vocabulary DFA D_r
    box_1d = FancyBboxPatch((9.2, 3.8), 2.2, 1.7,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=c_green_bg, edgecolor=c_green_border, linewidth=1.5)
    ax.add_patch(box_1d)
    ax.text(10.3, 5.15, "Vocabulary DFA (D_r)", ha='center', fontsize=9.5, fontweight='bold', color=c_green_border)
    ax.text(10.3, 4.7, "States Q, Vocab V\nTransitions delta(q, v)\nPermissible Token Sets\nA(q_t) subseteq V",
            ha='center', fontsize=8, color=c_text_dark)

    # -------------------------------------------------------------
    # 2. PHASE II: ONLINE INFERENCE CONTAINER
    # -------------------------------------------------------------
    phase2_box = FancyBboxPatch((0.4, 0.3), 11.2, 2.8,
                                boxstyle="round,pad=0.2,rounding_size=0.2",
                                facecolor='#FAFAFA', edgecolor='#64748B',
                                linestyle='-', linewidth=1.5)
    ax.add_patch(phase2_box)
    ax.text(0.6, 2.85, "PHASE II: Online Neuro-Symbolic Logit-Masking Autoregressive Loop",
            fontsize=11, fontweight='bold', color=c_slate_border)

    # Prompt Input Box
    box_2a = FancyBboxPatch((0.7, 0.6), 2.0, 1.9,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=c_red_bg, edgecolor=c_red_border, linewidth=1.5)
    ax.add_patch(box_2a)
    ax.text(1.7, 2.15, "Untrusted Context", ha='center', fontsize=9.5, fontweight='bold', color=c_red_border)
    ax.text(1.7, 1.6, "User Query +\nVendor Email /\nIndirect Injection\n('Transfer $1000')",
            ha='center', fontsize=8, color=c_text_dark)

    # Arrow 2A -> 2B
    ax.annotate("", xy=(3.1, 1.55), xytext=(2.7, 1.55),
                arrowprops=dict(arrowstyle="->", color='#475569', lw=1.8))
    ax.text(2.9, 1.75, "x_{<t}", ha='center', fontsize=8.5, fontstyle='italic', color='#475569')

    # Box 2B: Foundation LLM Forward Pass
    box_2b = FancyBboxPatch((3.1, 0.6), 2.2, 1.9,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=c_slate_bg, edgecolor=c_slate_border, linewidth=1.5)
    ax.add_patch(box_2b)
    ax.text(4.2, 2.15, "Foundation LLM", ha='center', fontsize=9.5, fontweight='bold', color=c_slate_border)
    ax.text(4.2, 1.6, "Qwen2.5-7B-Instruct\nAutoregressive Pass\nUnconstrained Logits\nz_t in R^{|V|}",
            ha='center', fontsize=8, color=c_text_dark)

    # Arrow 2B -> 2C
    ax.annotate("", xy=(5.7, 1.55), xytext=(5.3, 1.55),
                arrowprops=dict(arrowstyle="->", color='#475569', lw=1.8))
    ax.text(5.5, 1.75, "z_t", ha='center', fontsize=9, fontweight='bold', color='#475569')

    # Box 2C: Logit-Masking Projection Operator
    box_2c = FancyBboxPatch((5.7, 0.6), 2.8, 1.9,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=c_blue_bg, edgecolor=c_blue_border, linewidth=2.0)
    ax.add_patch(box_2c)
    ax.text(7.1, 2.15, "O-CTD Projection Operator (P)", ha='center', fontsize=9.5, fontweight='bold', color=c_blue_border)
    ax.text(7.1, 1.55, "Evaluate: delta(q_{t-1}, v)\nz_tilde_{t,v} = z_{t,v} if v in A(q_{t-1})\nelse -infinity\nOut-of-bound logits masked!",
            ha='center', fontsize=8, color=c_text_dark)

    # Connecting Arrow from DFA (Phase I) to Projection Operator (Phase II)
    ax.annotate("", xy=(7.1, 2.5), xytext=(10.3, 3.8),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.25",
                                color=c_green_border, lw=2.0, linestyle='-'))
    ax.text(9.0, 3.0, "DFA State Mask A(q_{t-1})", ha='center', fontsize=8.5, fontweight='bold', color=c_green_border)

    # Arrow 2C -> 2D
    ax.annotate("", xy=(8.9, 1.55), xytext=(8.5, 1.55),
                arrowprops=dict(arrowstyle="->", color='#475569', lw=1.8))
    ax.text(8.7, 1.75, "z_tilde_t", ha='center', fontsize=8.5, fontweight='bold', color='#475569')

    # Box 2D: Authorized Execution Output
    box_2d = FancyBboxPatch((8.9, 0.6), 2.5, 1.9,
                            boxstyle="round,pad=0.1,rounding_size=0.15",
                            facecolor=c_green_bg, edgecolor=c_green_border, linewidth=1.5)
    ax.add_patch(box_2d)
    ax.text(10.15, 2.15, "Authorized Dispatch", ha='center', fontsize=9.5, fontweight='bold', color=c_green_border)
    ax.text(10.15, 1.55, "x_t ~ Softmax(z_tilde_t)\nState: q_t = delta(q_{t-1}, x_t)\nGuaranteed Phi_struct = True\nt in T_r and amount <= $50",
            ha='center', fontsize=8, color=c_text_dark)

    # Autoregressive loopback arrow from 2D back to 2B
    ax.annotate("", xy=(4.2, 0.6), xytext=(10.15, 0.6),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.35",
                                color='#475569', lw=1.5, linestyle=':'))
    ax.text(7.1, 0.15, "Append x_t -> Next Autoregressive Step t+1", ha='center', fontsize=8, fontstyle='italic', color='#475569')

    plt.tight_layout()
    plt.savefig('paper/figure1_system_architecture.png', dpi=300, bbox_inches='tight')
    plt.savefig('paper/figure1_system_architecture.pdf', bbox_inches='tight')
    print("[SUCCESS] Created paper/figure1_system_architecture.png and .pdf")

if __name__ == '__main__':
    create_architecture_diagram()
