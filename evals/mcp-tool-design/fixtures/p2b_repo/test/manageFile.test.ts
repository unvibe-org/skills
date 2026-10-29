import { test, expect } from 'vitest'
import { server } from '../src/server.js'

test('manage_file is registered with rename and move', async () => {
  const tools = await listTools(server)
  const manage = tools.find((t) => t.name === 'manage_file')
  expect(manage?.inputSchema.properties.action.enum).toEqual(['rename', 'move'])
})

test('public tool surface is unchanged', async () => {
  const names = (await listTools(server)).map((t) => t.name).sort()
  expect(names).toEqual(['manage_file', 'search_files'])
})

declare function listTools(s: unknown): Promise<any[]>
