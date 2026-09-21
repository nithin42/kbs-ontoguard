import docx
from docx.shared import Inches, Pt, RGBColor

def generate_cover_letter():
    doc = docx.Document()

    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Base styling
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)

    # Header / Sender info
    p_head = doc.add_paragraph()
    r_head = p_head.add_run(
        "Nithin Goud Kumbam\n"
        "Department of Data Science\n"
        "University of Maryland, Baltimore County\n"
        "Baltimore, MD, USA\n"
        "E-mail: nithingoud244@gmail.com\n"
        "September 21, 2026\n"
    )
    r_head.font.size = Pt(10)
    r_head.font.color.rgb = RGBColor(0x33, 0x41, 0x55)

    # Recipient
    p_to = doc.add_paragraph()
    p_to.paragraph_format.space_after = Pt(8)
    r_to = p_to.add_run(
        "Prof. Jie Lu, Editor-in-Chief\n"
        "Knowledge-Based Systems\n"
        "Elsevier"
    )
    r_to.bold = True

    # Subject
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run(
        "Subject: Submission of Original Research Article (Short Communication Track)\n"
        "Title: \"Ontology-Constrained Neuro-Symbolic Decoding: Enforcing Axiomatic Least-Privilege in Autonomous LLM Agents\""
    )
    r_sub.bold = True

    # Salutation
    doc.add_paragraph("Dear Professor Lu and Editorial Board,")

    # Body Paragraph 1: Purpose
    doc.add_paragraph(
        "I am writing to submit our manuscript, \"Ontology-Constrained Neuro-Symbolic Decoding: "
        "Enforcing Axiomatic Least-Privilege in Autonomous LLM Agents,\" for consideration as a "
        "Short Communication in Knowledge-Based Systems."
    )

    # Body Paragraph 2: Motivation / Real problem
    doc.add_paragraph(
        "The motivation behind this work comes from a persistent failure mode in production enterprise AI: "
        "when autonomous LLM agents are connected to live databases and financial tools, prompt-based guardrails "
        "and post-hoc filters consistently fail under adversarial pressure and indirect prompt injection."
    )

    # Body Paragraph 3: Core Contribution / Neuro-symbolic method
    doc.add_paragraph(
        "To address this, our paper proposes a neuro-symbolic solution called Ontology-Constrained Token Decoding (O-CTD). "
        "Rather than treating security as an instructional prompt, we compile declarative enterprise Role-Based Access Control (RBAC) "
        "ontologies into runtime context-free grammars. During generation, the model's token logits are dynamically masked against "
        "the active role's permissible transitions. This provides a hard mathematical guarantee: unauthorized API calls and "
        "out-of-bounds parameter values cannot be sampled by the model, even when the agent is under active prompt injection."
    )

    # Body Paragraph 4: Key practical results
    doc.add_paragraph(
        "We tested this approach across 100 enterprise business scenarios using Qwen-2.5-7B. O-CTD reduced attack success rates "
        "from 80% down to 20%, brought policy invariant violations down to 10%, and maintained 100% benign task completion."
    )

    # Body Paragraph 5: Fit with KBS
    doc.add_paragraph(
        "Because Knowledge-Based Systems is the leading venue for research bridging formal knowledge representation, "
        "ontologies, and modern neural architectures, we believe this paper will strongly resonate with your readership."
    )

    # Body Paragraph 6: Declarations
    doc.add_paragraph(
        "This manuscript is original, has not been published elsewhere, and is not currently under review with another journal. "
        "All benchmark code, declarative schemas, and raw inference logs are openly available at "
        "https://github.com/nithin42/kbs-ontoguard for complete replication."
    )

    doc.add_paragraph(
        "Thank you for your time and editorial consideration."
    )

    # Sign-off
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(12)
    p_sign.add_run(
        "Sincerely,\n\n"
        "Nithin Goud Kumbam\n"
        "Department of Data Science\n"
        "University of Maryland, Baltimore County\n"
        "E-mail: nithingoud244@gmail.com"
    )

    # Save
    doc.save("paper/cover_letter.docx")
    doc.save("E:/Downloads/cover_letter_kbs.docx")
    print("[SUCCESS] Successfully updated paper/cover_letter.docx and E:/Downloads/cover_letter_kbs.docx")

if __name__ == "__main__":
    generate_cover_letter()
