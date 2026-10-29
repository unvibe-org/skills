# Instructions for the consuming agent, search stage 2

You play an AI assistant inside a chat app with many connected tools. In
each case you have already run one search, and the tool definitions it
loaded are shown. This is a test of how a tool surface reads to an
assistant, so act exactly as you would in that app.

1. Read the input file you were given. Every case is a separate
   conversation; forget the earlier cases when you read the next one.
2. For each case, decide your single next move: one call to a loaded tool,
   or a message to the user with no tool call. If none of the loaded tools
   fits and you would search again, use `"search_again"` as the tool.
3. Write one JSON array to the output path you were given, one object per
   case, in case order:

```json
{"id": "B01", "tool": "exact tool name, \"search_again\", or null", "args": {"...": "..."}, "message": "text to the user, or null"}
```

When you call a tool, `args` holds exactly the arguments you would send.
When you do not call a tool, `tool` and `args` are null.

Do not read any other file, do not use the web, do not use skills, and do
not call any of your own tools other than Read and Write. When the file is
written and parses as JSON, reply with only the word `done`.
