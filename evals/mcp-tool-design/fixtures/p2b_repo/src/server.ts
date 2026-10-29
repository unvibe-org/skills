import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { registerSearchFiles } from './tools/searchFiles.js'
import { registerManageFile } from './tools/manageFile.js'

export const server = new McpServer(
  { name: 'files-mcp', version: '1.4.0' },
  { instructions: 'Find files with search_files, then act on them with manage_file.' }
)
registerSearchFiles(server)
registerManageFile(server)
