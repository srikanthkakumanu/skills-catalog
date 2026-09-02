---
name: arch-diagram-generator
description: Generate modern, professional, presentation-quality architecture diagrams from natural language system descriptions.
license: Apache-2.0
compatibility: Claude Code, OpenAI Codex, Google Antigravity 2
---
# Architecture Diagram Generator

## Objective

Transform any software or platform description into a beautiful, production-grade architecture infographic suitable for solution design documents, PRDs, presentations, blogs, and executive reviews.

Prioritize clarity, correctness, visual hierarchy, and professional presentation over excessive detail.

---

## Workflow

1. Analyze the system description.
2. Identify:
   - Purpose
   - Actors
   - Business capabilities
   - AI/Agent components (if applicable)
   - Application services
   - Data stores
   - Integrations
   - Infrastructure
   - Security & governance
   - End-to-end workflow
3. Organize components into logical architecture layers.
4. Generate a polished architecture infographic.

---

## Default Layer Order

1. Users & Channels
2. Experience / APIs
3. AI Agents & Intelligence
4. Business Services / Microservices
5. Integration & Messaging
6. Data & Storage
7. Infrastructure & Platform
8. Security, Governance & Observability

Omit empty layers when unnecessary.

---

## AI Systems

For Agentic AI systems clearly separate:

- AI Agents
- LLM / Model Gateway
- Tools
- MCP
- RAG
- Memory
- Human Approval
- Guardrails

Never confuse AI agents with normal microservices.

---

## Visual Style

Create a premium enterprise infographic.

Requirements:

- Landscape (16:9)
- High resolution
- Modern architecture style
- White or subtle gradient background
- Professional color palette
- Dark title banner
- Rounded component cards
- Consistent spacing
- Minimal crossing arrows
- Clear grouping
- Meaningful icons
- Readable typography

The diagram should resemble work produced by an experienced enterprise architect and infographic designer.

---

## Components

Each component should contain:

- Name
- Icon
- 1–3 concise responsibilities

Avoid paragraphs.

---

## Workflow Strip

For business platforms include a simple lifecycle along the bottom.

Example:

Campaign → Discovery → Content → Review → Approval → Launch → Analytics → Monetization

---

## Architecture Rules

- Infer reasonable architecture from the description.
- Group related capabilities together.
- Separate business logic from infrastructure.
- Place external systems outside the platform boundary.
- Show data flow only where meaningful.
- Keep diagrams balanced and uncluttered.
- Prefer layered architecture over random boxes.
- Do not invent unsupported technologies.

---

## Quality Checklist

Before finishing verify:

- Architecture is logically organized.
- Components are correctly grouped.
- Reading flow is obvious.
- Text is readable.
- Colors are consistent.
- Alignment is clean.
- Minimal visual clutter.
- Diagram is presentation-ready.

---

## Output

Generate a single polished architecture infographic that immediately communicates:

- What the system is
- Who uses it
- Major architectural layers
- AI capabilities (if any)
- Data flow
- Core business workflow

The result should look suitable for executive presentations and enterprise architecture documentation.
