# Architecture Diagram Generator

**Version:** 1.0.0 | **Status:** Supported | **License:** Apache-2.0

---

## Overview

The **Architecture Diagram Generator** skill transforms natural language system descriptions into polished, presentation-ready architecture diagrams suitable for solution design documents, PRDs, technical presentations, blogs, and executive reviews.

This skill excels at visualizing:
- Platform and system architecture
- Microservices ecosystems
- Agentic AI system topologies
- Data flow and integration patterns
- Business capability layers
- Cloud and infrastructure designs

**Key Focus:** Clarity, correctness, professional presentation, and visual hierarchy over excessive detail.

---

## When to Use

Invoke this skill when you need to:

- **Document System Architecture** — Create visual representations for architecture decision records (ADRs), tech design documents, or solution briefs
- **Communicate with Stakeholders** — Generate diagrams for executive presentations, board reviews, or business partner alignment
- **Design New Systems** — Validate architecture concepts with visual layout during the design phase
- **API & Integration Documentation** — Illustrate how systems connect and communicate
- **Technical Blogs & Publications** — Create professional infographics for technical content
- **Enterprise Architecture Governance** — Support architectural review and compliance documentation
- **Sales & Marketing Collateral** — Build system topology diagrams for customer-facing materials

**When NOT to use:**
- For detailed sequence or timing diagrams (use interaction-focused tools instead)
- For data model ERD diagrams (use database-specific tools)
- For UML class diagrams (use UML tools for code-level design)

---

## Input Specification

### Required

A **system description** containing:
- **Purpose/mission** of the platform
- **Primary actors** and users
- **Major business capabilities** (what the system does)
- **Key components** (services, databases, integrations)
- **Technology stack** (if known)
- **Data flow** and workflow (core business process)
- **Infrastructure** and deployment model
- **Security & governance** considerations (if applicable)

### Optional but Recommended

- **Agentic AI components** (if system includes autonomous agents, LLMs, or MCP integrations)
- **Integration points** with external systems
- **User workflows** or business process steps
- **Deployment topology** (on-premise, cloud, hybrid)

### Format

Any of:
- Freeform prose description
- Bullet-point list of capabilities
- Existing architecture documentation (refined & visualized)
- BRD or PRD excerpt (design context)

---

## Output Specification

### Deliverable

A **single, polished architecture infographic** published as an interactive Artifact (SVG/HTML or image).

### Characteristics

- **Dimensions:** Landscape (16:9 aspect ratio), high resolution
- **Style:** Modern enterprise architecture aesthetic
- **Background:** White or subtle gradient
- **Color Palette:** Professional, brand-neutral (5–7 coordinated colors)
- **Components:** Rounded cards with icons, names, and 1–3 concise responsibilities
- **Typography:** Clear hierarchy, readable at presentation scale
- **Layout:** Layered architecture with logical grouping, minimal arrow crossing

### Standard Layers (Omit if Empty)

1. **Users & Channels** — End users, clients, external actors
2. **Experience / APIs** — Web, mobile, public APIs, gateways
3. **AI Agents & Intelligence** — Agentic systems, LLM orchestration, tools
4. **Business Services / Microservices** — Core domain logic, business rules
5. **Integration & Messaging** — Event buses, queues, API integrations
6. **Data & Storage** — Databases, caches, data lakes, search
7. **Infrastructure & Platform** — Kubernetes, cloud services, networking
8. **Security, Governance & Observability** — Auth, compliance, monitoring, logging

### Special Sections

- **Business Workflow Strip** (optional): Lifecycle or process flow at the bottom (e.g., Campaign → Discovery → Content → Launch → Analytics)
- **Agentic AI Layer** (if applicable): Clearly separated AI agents, LLM gateways, tools, MCP, RAG, memory, human approval, guardrails

---

## How It Works

### Step 1: Analyze the System Description

Parse the provided description to extract:
- System purpose and mission
- Actor personas and user types
- Major business capabilities
- Technological components and integrations
- Data flows and workflow patterns

### Step 2: Organize into Architecture Layers

Map components into the standard 8-layer model:
- Group related capabilities
- Separate business logic from infrastructure
- Place external systems outside platform boundaries
- Identify AI/agent-specific components (if present)

### Step 3: Design the Visual Layout

Decide:
- Which layers are needed (omit empty ones)
- Component grouping and visual nesting
- Color coding (layer-based or capability-based)
- Icon selections (meaningful, consistent style)
- Flow arrows (data, requests, integrations)

### Step 4: Generate the Infographic

Create a polished, presentation-ready diagram using SVG, Canvas, or inline HTML/CSS that:
- Follows enterprise architecture visual conventions
- Maintains professional typography and spacing
- Supports light and dark theme rendering
- Renders cleanly at multiple scales (presentations, printed documents, web)

### Step 5: Quality Assurance

Verify:
- ✓ Architecture is logically organized and correct
- ✓ Components are properly grouped and labeled
- ✓ Reading flow is intuitive (top-to-bottom, left-to-right)
- ✓ Text is readable at presentation scale
- ✓ Colors are consistent and accessible
- ✓ Alignment is clean, no visual clutter
- ✓ Diagram is immediately suitable for executive presentations

---

## Architecture Rules & Principles

### Design Principles

1. **Infer Reasonable Architecture** — When details are ambiguous, apply standard patterns (layered, microservices, event-driven, etc.)
2. **Group Related Capabilities** — Organize by domain, function, or responsibility
3. **Separate Business Logic from Infrastructure** — Platform services above, infrastructure below
4. **Boundary Clarity** — External systems are visually outside the platform boundary
5. **Data Flow Intentionality** — Show data flow only where it's meaningful or surprising
6. **Balance & Clarity** — Prioritize balanced layout over comprehensive coverage
7. **Layered Architecture** — Prefer horizontal layers over random box scattering
8. **No Invented Technologies** — Only use components and integrations explicitly mentioned or clearly implied

### AI Systems Specifics

For agentic AI systems, **clearly separate:**
- AI Agents (autonomous decision-making components)
- LLM / Model Gateway (model orchestration)
- Tools (callable capabilities exposed to agents)
- MCP (Model Context Protocol connections)
- RAG (retrieval-augmented generation pipeline)
- Memory (vector stores, conversation stores, knowledge bases)
- Human Approval (human-in-the-loop gates)
- Guardrails (safety, compliance, output filtering)

**Never confuse AI agents with normal microservices.**

---

## Visual Standards

### Color Palette

Use a professional, accessible palette:
- **Neutral Base:** Off-white, light gray
- **Primary Accent:** Blue or corporate brand color
- **Secondary:** Complementary color (green, orange, purple)
- **Infrastructure:** Gray-blue (neutral infrastructure feel)
- **AI/Intelligence:** Purple or gold (intelligence/uniqueness)
- **Data:** Amber or teal (data flows)
- **Security:** Red or burgundy (governance/compliance)

### Typography

- **Title:** Large, bold, dark color (white text on dark banner optional)
- **Component Names:** Medium weight, high contrast
- **Responsibilities:** Small, secondary color, max 3 lines
- **Labels & Legends:** Consistent sans-serif, readable at 10pt print size

### Icons

- Use consistent icon sets (Material Design, Feather, Font Awesome style)
- Each component should have one meaningful icon
- Icons support text, never replace it

### Spacing & Layout

- Consistent padding within and around component cards
- Minimum 2–3 line heights between layers
- Clear visual separation between platform and external systems
- Minimal arrow crossing (reroute flows to avoid visual clutter)

---

## Examples

### Example 1: SaaS Marketing Platform

A system with users, APIs, microservices, data pipeline, and workflow:

```
[Clients]
    ↓
[Web App] [Mobile App] [Public APIs]
    ↓
[Campaign Service] [Content Service] [Analytics Engine]
    ↓
[Message Queue] [Integration Layer]
    ↓
[PostgreSQL] [Redis] [Data Lake] [External Platforms (Slack, Zapier, etc.)]
    ↓
[Kubernetes] [CDN] [Cloud Storage]
    ↓
[Monitoring] [Logging] [Auth]

Workflow Strip: Campaign → Discovery → Content → Review → Approval → Launch → Analytics → Monetization
```

### Example 2: Agentic AI Research Assistant

```
[Users] [Web Interface] [Slack Bot]
    ↓
[API Gateway]
    ↓
[Research Agent] ← [LLM Gateway (Claude)]
    ├── [Search Tool]
    ├── [RAG Pipeline] → [Vector Store]
    ├── [Summarization Tool]
    └── [Human Approval Gate]
    ↓
[PostgreSQL] [Redis] [Document Store]
    ↓
[Cloud Infrastructure] [Security & Compliance]
```

---

## Installation

### Using the Catalog Installer

```bash
# Install arch-diagram-generator to all runtimes
./install.sh --skill arch-diagram-generator

# Install to Claude Code only
./install.sh --skill arch-diagram-generator --target claude

# Force reinstall with file copy
./install.sh --skill arch-diagram-generator --force --mode copy
```

### Manual Installation

Copy the skill directory to your runtime:

**Claude Code:**
```bash
cp -r skills/arch-diagram-generator ~/.claude/skills/
```

**Google Antigravity:**
```bash
cp -r skills/arch-diagram-generator ~/.antigravity/skills/
# or
cp -r skills/arch-diagram-generator .agents/skills/
```

**OpenAI Codex:**
```bash
cp -r skills/arch-diagram-generator ~/.codex/skills/
```

---

## Skill Invocation

### Claude Code

```bash
/arch-diagram-generator
```

Or type naturally: *"Generate an architecture diagram for our microservices platform"* and invoke via the skill picker.

### Standalone / Python CLI

```bash
python3 -m skills.arch_diagram_generator.SKILL.md "Your system description here"
```

---

## Quality Assurance Checklist

Before delivering a diagram, verify:

- [ ] Architecture is logically organized (correct layer hierarchy)
- [ ] Components are correctly grouped by domain/function
- [ ] Reading flow is obvious (top-to-bottom, natural progression)
- [ ] Text is readable (font sizes, contrast, no overlap)
- [ ] Colors are consistent and meaningful
- [ ] Alignment is clean (grid-aligned, no visual clutter)
- [ ] Icons are consistent and meaningful
- [ ] External systems are clearly marked
- [ ] Data flows are shown only where meaningful
- [ ] AI components are clearly distinguished (if present)
- [ ] Workflow strip is present and correct (if applicable)
- [ ] Diagram is presentation-ready (no rough edges, finalized styling)

---

## Integration with Pipeline

**Upstream Dependencies:**
- Typically used **after** [`architecture-decisions`](../architecture-decisions/README.md) and [`detailed-design`](../detailed-design/README.md) phases to visualize decisions
- Can also be **standalone** for quick architecture documentation

**Downstream Usage:**
- Feeds into [`prd`](../prd/README.md) (architecture diagram as appendix)
- Suitable for solution design documents, technical specifications, and presentations

---

## Context & Token Efficiency

- **Input Analysis:** Compact, single-pass parsing of system description
- **Visual Generation:** Efficient SVG/HTML rendering (no complex animations or interactions)
- **Output Size:** Optimized for web rendering (typically 50–200 KB for a complete diagram)
- **Reusability:** Diagram can be exported as PNG, PDF, or embedded in multiple documents

**Typical Execution:** ~30–60 seconds, token cost varies with system complexity (400–1,500 tokens)

---

## Troubleshooting

### Diagram Looks Cluttered

- Reduce components shown per layer (move details to appendix)
- Increase layer spacing
- Simplify or consolidate responsibilities per component
- Consider splitting into multiple focused diagrams

### Hard to Read Text

- Increase font sizes
- Reduce component count or card sizes
- Use shorter, more concise labels
- Ensure sufficient contrast between text and background

### Missing or Wrong Components

- Re-run with a more detailed system description
- Provide explicit list of key components
- Clarify the role of ambiguous systems

### Architecture Seems Wrong

- Verify the description against actual system design
- Ask the skill to explain its grouping decisions
- Provide corrections as follow-up refinements

---

## License

Apache-2.0 © [Srikanth Kakumanu](https://github.com/srikanthkakumanu)

---

## See Also

- [Architecture Decisions Skill](../architecture-decisions/README.md) — Decide architecture style and patterns
- [Detailed Design Skill](../detailed-design/README.md) — Define design patterns and data models
- [Tech Stack Skill](../tech-stack/README.md) — Select specific technologies per component
- [Agent Skills Catalog](../../README.md) — Complete skill listing and installation guide
