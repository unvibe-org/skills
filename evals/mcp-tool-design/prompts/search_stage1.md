# Instructions for the consuming agent, search stage 1

You play an AI assistant inside a chat app whose host shows only tool names
and makes you load a tool with a search before you can call it. This is a
test of how a tool surface reads to an assistant, so act exactly as you would
in that app.

1. Read the input file you were given. It holds the host context, the
   connected tool names, and the cases. Every case is a separate
   conversation; forget the earlier cases when you read the next one.
2. For each case, decide the one search you would run first.
3. Write one JSON array to the output path you were given, one object per
   case, in case order:

```json
{"id": "B01", "query": "keywords, or null", "select": ["exact tool names"] }
```

Use either `query` or `select` (set the other to null). Use neither (both
null) only if your first move needs no tool.

Do not read any other file, do not use the web, do not use skills, and do
not call any of your own tools other than Read and Write. When the file is
written and parses as JSON, reply with only the word `done`.
