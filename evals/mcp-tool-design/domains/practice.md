# Domain: practice sessions

An assistant runs short practice sessions for a learner inside a chat. The
learner is the user. The assistant acts through tools; you do not need to
know their names or shapes.

## How a session works

- A run starts on a topic and gets an id such as `r_88`.
- A round has exactly three drills. The assistant fetches each drill, shows
  it, and submits the learner's answer. A submitted answer comes back marked
  correct or incorrect, with the expected answer.
- The assistant can fetch a hint for the current drill.
- At the end the assistant saves the run: the three results, the learner's
  own difficulty rating from 1 to 5, and how long the session took.
- A run can be resumed later, in a new conversation, by its id.
- Topics: `past tense`, `ordering food`, `numbers`, `directions`.

## What the assistant can do (intent labels)

| Intent | What it does |
|---|---|
| `start` | Start a practice run on a topic |
| `next_drill` | Fetch the next drill of the run |
| `submit` | Submit the learner's answer to the current drill |
| `hint` | Fetch a hint for the current drill |
| `finish` | Save the finished run |
| `resume` | Resume a run by id |
| `topics` | List the topics |
| `ask_user` | The right next move is to say something to the learner and wait |
