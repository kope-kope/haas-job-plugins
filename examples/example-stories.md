# Alex Chen — Interview Stories

## STORY 1: Tell Me About Yourself

"I'm a product manager who loves working closely with engineers. The very first product I managed was an API product for developers at banks to embed investment into the mobile app at ThreadPay. That experience made me empathize with software developers early on in my career, and I've found it easy working with them ever since.

I went on to co-found CoinFlow, a product that allowed developers to embed payments into their apps through APIs and SDKs. We onboarded over 100 developers and processed close to $500K in volume through our documentation and API contracts. That company was eventually acquired.

I'm currently in business school at Berkeley because a consistent piece of feedback I got from my previous roles was to become more business savvy. Now I feel like I have a good foundation in both the technical side and the business side to be a really effective product owner."

**Tags**: intro, technical credibility, career arc, startup founder

---

## STORY 2: How Do You Write Specs / Work With Engineers

**Situation**: At TradeFlow, the CTO had been building the product from day one. He had all the context, so specs could be lightweight.

**Task**: When we onboarded new engineers and wanted to build a whole new product — a B2B SaaS for investment pipeline management — we needed a completely different approach.

**Action**: I started by defining the customer goals: we want customers to be able to build an investor pipeline, start a fund, manage assets, create wallets. Then I broke each of those goals into user stories, sketched wireframes so the engineers could see what I was imagining and push back early, wrote everything into a doc, and then sat with the engineers to plan sprints so we could figure out together what to deliver first and what to sequence later.

**Result**: We shipped the B2B platform on time, and the process became the template for how we onboarded every new engineer after that.

**Key lesson**: "I don't throw specs over the wall. I sit with the engineers and we plan delivery together, because they always see constraints and dependencies I didn't think of. The spec is a starting point for a conversation, not a final order."

**Tags**: cross-functional, engineering collaboration, specs, process

---

## STORY 3: How Do You Prioritize What Gets Built?

**Situation**: At TradeFlow, our CEO identified that several startups on the platform were about to raise new rounds.

**Task**: If we could get them managing their stock options with us, we'd be positioned to capture the secondary transactions when those rounds closed. Even at 1% of those transactions, that was significant recurring revenue. It was a time-sensitive window.

**Action**: Because design leads engineering by a sprint in our process, I started working with design immediately. By the time the engineers were ready to pick it up, they'd already been part of the conversation through the design phase. We deprioritized what was originally planned, but it wasn't a shock to anyone — the team had visibility the whole way through.

**Result**: We shipped the stock options feature before the fundraising window closed and captured the secondary transactions.

**Key lesson**: "Prioritization isn't just a scoring exercise. It's about understanding the business case, making sure there's a real reason we're doing this now and not later, and then managing the transition so the team isn't caught off guard."

**Tags**: prioritization, business judgment, stakeholder management, time-sensitive

---

## STORY 4: Tell Me About a Time You Disagreed With an Engineer

**Situation**: At Nova (Horizon Ventures' digital jurisdiction product), we were building an MVP and needed to submit forms to a government agency to get the product live.

**Task**: The long-term plan was to integrate directly with the government's CRM. But for the MVP, that integration didn't exist yet. I proposed a scrappy workaround: take the user's data and write it onto a scanned copy of the government's paper form.

**Action**: The engineer pushed back — the form was a scanned image, not a fillable PDF. He was technically right: you can't write into a scanned image. But I realized I was framing the problem wrong. I didn't need to fill out the form. I needed to place text on top of an image at the right positions. That's not a form-filling problem, it's an image manipulation problem. So I built a scrappy proof of concept in Python — used a library to position data fields at specific coordinates on top of the scanned form image.

**Result**: The engineer took it and rebuilt it properly in TypeScript. We shipped the MVP and were able to process 200+ business registrations.

**Key lesson**: "Sometimes when an engineer says 'not possible,' what they mean is 'I can't see how this would work with the approach you're describing.' If I can reframe the problem and build a rough proof of concept, the conversation shifts from 'can we?' to 'how do we do this well?'"

**Tags**: disagreement, reframing, technical problem-solving, MVP, scrappy

---

## STORY 5: Tell Me About Yourself (Business-Side Version)

"I come from a family of entrepreneurs. But my generation is the first to combine that with a global education, so I've always had one foot in building things and one foot in understanding how global systems work.

I properly caught the bug in my second year of university. Brazil went through a macroeconomic shift — the real devalued, my dad's business crashed, and he couldn't access his pension. Overnight I became the breadwinner. I was lucky to be on multiple scholarships, so I had some capital, and I started a small e-commerce service. That was my first real business.

From there I moved into tech — I've spent my career as a product manager at startups, working with engineers to solve business problems. I co-founded a payments company that was acquired. But the experience that shaped me most was working with the Horizon Ventures team to set up Nova — a digital jurisdiction where tech companies expanding into Latin America could incorporate in a single registration point, instead of registering separately in multiple countries. We registered 200 businesses. That was when I understood the global economy for what it really is — infrastructure that either works for people or gets in their way.

I'm finishing my MBA at Berkeley in May."

**Tags**: intro, entrepreneurship, global perspective, business leadership, macro context

---

## THEME COVERAGE

| Theme | Covered By |
|-------|-----------|
| Tell me about yourself | Story 1 (technical), Story 5 (business) |
| Engineering collaboration | Story 2 |
| Prioritization | Story 3 |
| Disagreement / conflict | Story 4 |
| Failure / learning | (not yet covered — build this) |
| Data-driven decisions | Partially in Story 3 |
| Ambiguity | Story 4 |

**Gaps to fill**: Need a dedicated failure story and a stronger data-driven decision story. These are the two most common behavioral questions that aren't fully covered yet.

---

## WEAK SPOTS (be honest about these in prep)

- No dedicated failure story yet — interviewers almost always ask this
- "Tell me about yourself" runs long — practice the 90-second version
- Story 3 (prioritization) could use a clearer metric on the result
- Need a story about managing up / influencing a senior stakeholder
