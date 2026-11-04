# Finance & FinOps

5 bots. Generated from the skills on disk by `tools/build_readmes.py`; do not edit by hand.

| Bot | What it owns | Guide |
|---|---|---|
| [`budget-variance-explainer`](budget-variance-explainer/) | Drafts the narrative behind a budget variance from the context the user supplies and the discussion in mail and meetings, never producing or changing… | [PDF](../../guides/budget-variance-explainer.pdf) |
| [`cloud-cost-digest`](cloud-cost-digest/) | Turns cloud billing exports and provider alert emails into a short digest of what moved, what is anomalous and what to ask an owner about. | [PDF](../../guides/cloud-cost-digest.pdf) |
| [`expense-reconciliation`](expense-reconciliation/) | Reconciles submitted expense claims against the receipts and statements sitting in the mailbox, lists what is missing or unmatched, and drafts the… | [PDF](../../guides/expense-reconciliation.pdf) |
| [`invoice-vendor-followup`](invoice-vendor-followup/) | Finds invoice and payment threads in the mailbox that have gone unanswered, ages them, and drafts the follow-up to each counterparty. | [PDF](../../guides/invoice-vendor-followup.pdf) |
| [`subscription-hunter`](subscription-hunter/) | Finds every recurring subscription, licence and service renewal hiding in the user's mailbox and files, and builds a dated renewal calendar with a… | [PDF](../../guides/subscription-hunter.pdf) |

## Installing this pack

Each bot is a separate archive. Download the ones you want from `dist/`, then in Cowork: **Customize** → **Skills** → the arrow next to **Add** → **Upload skill**. Cowork validates each file and writes it to your OneDrive.

The **Guide** column is a one-page PDF written for someone who has never used Cowork. Send it with the archive and they will not need to ask you anything.

This pack costs **5 of your 50 custom skills**. Scheduling is optional on every bot; each schedule you create costs one of your 25.
