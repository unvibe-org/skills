import { z } from 'zod'
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { drive } from '../drive.js'

export function registerManageFile(server: McpServer) {
  server.registerTool(
    'manage_file',
    {
      description:
        'Rename a file or move it to another folder. Use it for "rename this" or "move it to Taxes". Returns the file\'s new name and folder. To find a file use search_files.',
      inputSchema: {
        action: z.enum(['rename', 'move']),
        fileId: z.string().describe('File id as returned by search_files.'),
        newName: z.string().optional().describe('rename: the new file name.'),
        folder: z.string().optional().describe('move: name of an existing folder.'),
      },
      annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    },
    async ({ action, fileId, newName, folder }) => {
      if (action === 'rename') return text(await drive.rename(fileId, newName!))
      return text(await drive.move(fileId, folder!))
    }
  )
}

const text = (v: unknown) => ({ content: [{ type: 'text' as const, text: JSON.stringify(v) }] })
