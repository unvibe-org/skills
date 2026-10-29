// Thin client for the Acme Drive REST API.
export const drive = {
  search: async (query: string) => api('GET', `/files?q=${encodeURIComponent(query)}`),
  rename: async (id: string, name: string) => api('PATCH', `/files/${id}`, { name }),
  move: async (id: string, folder: string) => api('POST', `/files/${id}/move`, { folder }),
  // Moves the file to Trash. Trash empties itself after 30 days.
  trash: async (id: string) => api('POST', `/files/${id}/trash`),
}

async function api(method: string, path: string, body?: unknown) {
  const res = await fetch(`https://api.acmedrive.example${path}`, { method, body: body ? JSON.stringify(body) : undefined })
  if (!res.ok) throw new Error(`${method} ${path}: ${res.status}`)
  return res.json()
}
