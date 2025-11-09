**ROLE**: You are a research methodologist and domain expert.

**TASK:** Analyze the following research article. Your objective is to deconstruct its components into a structured, factual summary. Do not provide opinions or a qualitative critique. Extract the information and format it precisely as specified below.

**INPUT:** [Paste the full text, or at minimum, the Abstract, Introduction, Methods, and Results sections of the paper here.]

**OUTPUT FORMAT** (Strict JSON):

**1. Full Citation (APA 7th)**

[AI extracts and formats the full citation]

**2. Core Research Question & Hypothesis(es)**

- **Primary Question:** [AI identifies the main "gap" or question the study addresses]
- **Hypotheses:** [AI lists the specific, testable predictions]

**3. Theoretical Framework**

[AI summarizes the theoretical antecedents and rationale. What theories or prior findings motivate the study?]

**4. Methodology & Design**

- **Research Design:** [e.g., Longitudinal cohort, cross-sectional, randomized controlled trial, qualitative interview]
- **Sample (N):** [e.g., N = 120 undergraduate students]
- **Population:** [Key demographics, recruitment method, limitations on generalizability]
- **Independent Variable(s) / Predictors:** [What was manipulated or measured as the "cause"?]
- **Dependent Variable(s) / Outcomes:** [What was measured as the "effect"?]
- **Key Covariates:** [What variables were controlled for in the analysis?]

**5. Empirical Findings**

[AI lists the primary statistical results *without* interpretation. e.g., "Variable X was a significant predictor of Variable Y ($\beta$ = .21, p < .05). The mediation model was (or was not) significant."]

**6. Authors' Stated Conclusions**

[AI summarizes the authors' *interpretation* of their findings and their stated contributions.]

**7. Authors' Stated Limitations**

[AI lists the limitations explicitly identified by the authors in the discussion section.]

**8. [MY ANALYSIS] Critical Appraisal & Integration**

- **Methodological Critique (Internal Validity):**
- **Generalizability Critique (External Validity):**
- **Construct Validity:** [Did they *really* measure what they claim to have measured?]
- **Key Contribution / Novelty:** [My assessment of its importance]
- **Connections:** [e.g., "Refutes [Seminal Paper A]", "Provides mechanism for [Review Paper B]", "Contradicts [Other Paper C]"]
- **Unanswered Questions:** [What this paper makes me think of next]

**9. Attributes and tags**

IMPORTANT: You MUST provide ALL of the following metadata fields. Do not omit any field.

- **`type:`**: The paper's ontology. This is your single most important filter.
    - `Empirical-Study`
    - `Meta-Analysis`
    - `Systematic-Review`
    - `Theory`
    - `Commentary`
    - `Book-Chapter`
- **`year:`**: For chronological filtering (e.g., finding all papers post-2020). REQUIRED.
- **`rating:`**: Your personal, subjective appraisal (1-5). Allows you to filter *for* high-quality or *against* low-quality studies. REQUIRED.
- **`journal:`**: The journal or conference. REQUIRED.
- **`authors:`**: List ALL authors as `[[FirstName LastName]]`. This will automatically create and link author-specific pages in Obsidian. REQUIRED - include every author from the paper.
- **`topic/`**: The primary subject matter. Provide 2-4 relevant topic tags. REQUIRED.
    - `#topic/emotion-regulation`
    - `#topic/affect-labeling`
    - `#topic/self-care`
- **`method/`**: The methodology employed. Provide all relevant methods. REQUIRED.
    - `#method/fMRI`
    - `#method/RCT` (Randomized Controlled Trial)
    - `#method/longitudinal`
    - `#method/self-report`
    - `#method/qualitative`
    - `#method/cross-sectional`
- **`theory/`**: The theoretical framework being used, tested, or proposed. REQUIRED.
    - `#theory/process-model-of-er`
    - `#theory/constructivism`
- **`population/`**: The sample studied. REQUIRED.
    - `#population/clinical`
    - `#population/undergraduate`
    - `#population/in-vivo`
- **`#seminal-work`**: Optional - only tag if this is one of the 5-10 foundational papers in the field.