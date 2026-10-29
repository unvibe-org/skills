# Instructions for the consuming agent

You play an AI assistant inside a chat app. You can act only through the
tools of one MCP server. This is a test of how a tool surface reads to an
assistant, so act exactly as you would in that app.

1. Read the fixture file you were given. It is the tool server as your host
   shows it: `tools` holds each tool's `name`, `description`,
   `input_schema`, and `annotations`. If `server_instructions` is not null,
   it holds the server's instructions, which your host showed you before the
   conversation began.
2. Read the case file you were given. It starts with the host context, then
   lists cases. Every case is a separate conversation; forget the earlier
   cases when you read the next one.
3. For each case, decide your single next move as the assistant: either one
   tool call, or a message to the user with no tool call. Do not simulate
   what would happen after it.
4. Write one JSON array to the output path you were given, one object per
   case, in case order:

```json
{"id": "A01", "tool": "tool_name or null", "args": {"...": "..."}, "message": "text to the user, or null"}
```

When you call a tool, `args` holds exactly the arguments you would send.
`message` holds any text you would show the user in the same turn, or null.
When you do not call a tool, `tool` and `args` are null.

Do not read any other file, do not use the web, and do not use skills. Do
not explain your choices in the file. When the file is written and parses as
JSON, reply with only the word `done`.
