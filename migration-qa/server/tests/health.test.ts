import { test } from "node:test";
import assert from "node:assert/strict";
import { createApiServer } from "../src/api/index.ts";

test("GET /health returns 200 with status ok", async () => {
  const server = createApiServer();
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const { port } = server.address() as { port: number };
  try {
    const res = await fetch(`http://localhost:${port}/health`);
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { status: "ok" });
  } finally {
    server.close();
  }
});

test("unknown route returns 404", async () => {
  const server = createApiServer();
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const { port } = server.address() as { port: number };
  try {
    const res = await fetch(`http://localhost:${port}/nope`);
    assert.equal(res.status, 404);
  } finally {
    server.close();
  }
});
