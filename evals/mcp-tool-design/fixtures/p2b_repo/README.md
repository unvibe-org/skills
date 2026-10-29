# files-mcp

MCP server for Acme Drive. Version 1.4.0.

## Public tool surface

The tool names below are a public contract. Customers' saved prompts and the
FlowLink integration call them by name (see `clients/flowlink-allowlist.json`).
Renaming or removing a tool breaks them.

| Tool | What it does |
|---|---|
| `search_files` | Find files by name or text |
| `manage_file` | Rename a file or move it to another folder |
