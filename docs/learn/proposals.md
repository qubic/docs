# Proposals (Draft)

In the Qubic community, decisions aren't made by a single person or a centralized group of people. Instead, they are made by the community as a whole through a democratic and transparent process. A key aspect of this process is the proposal system.

## What are Proposals?

Proposals are suggestions for changes, improvements, or new features for the Qubic ecosystem. They can be put forward by any member of the Qubic community. Proposals cover a wide range of topics, from minor tweaks and bug fixes to major changes that could redefine how Qubic operates.

## How to Make a Proposal

Anyone in the Qubic community can make a proposal. Here's how:

1. **Identify an Issue or Opportunity:** You might have identified a problem that needs fixing, an opportunity for improvement, or a new feature that could benefit the entire community.
2. **Draft Your Proposal:** Write a detailed description of what you want to change. Be clear about the problem or opportunity, your proposed solution, and the benefits it would bring to Qubic.
3. **Submit Your Proposal:** Post your proposal on the designated platform where Qubic community members can review it. Be sure to check any formatting guidelines or submission rules.
4. **Community Review:** Community members can review, comment on, and ask questions about your proposal. Be open to feedback and ready to make revisions if necessary.

## How are Proposals Reviewed?

After a proposal is submitted, it is reviewed by the community. Review involves:

- Evaluating the problem or opportunity identified in the proposal.
- Assessing the feasibility of the proposed solution.
- Considering the potential benefits and drawbacks.
- Asking questions and seeking clarifications from the proposer.

Community members are encouraged to take an active role in the review process, as the decision will be made collectively.

## How are Decisions Made on Proposals?

Decisions on proposals are made democratically, through a voting process involving quorums. If a proposal gains support from the majority, it is accepted and moves onto the implementation phase.

Remember, the proposal process is a chance for you to help shape the future of Qubic. Your ideas and opinions matter, so don't hesitate to get involved!

## The voting Basics & Rules
- **A proposal consists** of a **URL** where the proposal is documented. This website should be something that **cannot be altered**. Explain what you propose and show which options the computors can choose from.
- A proposal can have up to **7 options** to vote for and **must be sorted without gaps, duplicates** make the proposal **invalid**.
- Proposals and ballots are **valid only per epoch** (lifetime)
- Per **epoch and computor** only **one** proposal is allowed per epoch
- A **computor that has proposed** anything is **not allowed to participate** in voting for this epoch. But the first option from the published proposal is taken as own computor's vote.
- Proposals and ballots are **published when** the **computor** is **tick leader** (in the worst case, you need to wait 676 ticks to see your votes counting)
- The **peer where the computor seed is running** must be in the **latest tick** to issue a vote
- A proposal with **less than 451** votes is **invalid**
- A **valid** vote is one that votes for **one of the given options** in the proposal
- The **result** of a proposal is the option which has got strictly more or equal than **50% (226 votes)** of Quorum (451)
- If **none** of the options has got the minimum votes (226), then **another proposal** should be published with the **two most popular** options only. In some cases if #1/#2 places are shared by several options more voting steps may be needed
