# Domain: helpdesk

An assistant helps a support agent work a helpdesk. The support agent is the
user. The assistant acts through tools; you do not need to know their names
or shapes.

## People and places

- The user is Sam Ortiz, Billing team, timezone Europe/Berlin.
- Today is Thursday 2026-10-29, 14:00 local time.
- Staff: Kim Lee (Billing), Kim Park (Tier 2), Jon Reyes (Onboarding),
  Priya Shah (Billing), Sam Ortiz (Billing, the user).
- Teams: Billing, Tier 2, Onboarding.
- Tickets have numeric ids such as 4812. Customers write the ticket text.

## What the assistant can do (intent labels)

| Intent | What it does |
|---|---|
| `search` | Find tickets by text, status, assignee, team, or creation date |
| `get` | Read one ticket in full, with its conversation |
| `reply` | Reply to the customer on a ticket; the customer gets an email |
| `note` | Add an internal note to a ticket; only staff see it |
| `forward` | Forward a ticket to an outside email address |
| `assign` | Assign one or more tickets to a staff member |
| `escalate` | Hand one or more tickets to another team's queue, with a reason |
| `status` | Set one or more tickets to open, pending, or solved |
| `merge` | Merge duplicate tickets into one surviving ticket |
| `delete` | Delete tickets permanently |
| `followup` | Schedule a reminder to follow up on a ticket at a date and time |
| `log_time` | Log time spent working on a ticket |
| `ask_user` | The right first move is to ask the user something |
| `none` | No action fits; answer directly |
