# Local Development

Minimal steps to get the whole stack running.

---

## Prerequisites

- Node.js ⩾ 18 + `pnpm`
- Conda (e.g. [Miniconda](https://docs.conda.io/en/latest/miniconda.html))

---

## 🔀 Run the app (two-terminal workflow)

### 1️⃣  Terminal 1 – Frontend

```bash
cd frontend        # move to React client
yarn: pnpm i       # install deps
pnpm run dev       # Vite dev-server @ http://localhost:5173
```

### 2️⃣  Terminal 2 – Backend

```bash
cd be              # move to Express/FastAPI backend
pnpm i             # install Node deps
conda env create -f environment.yml  # create Python env (one-time)
conda activate agents                # activate it each session
pnpm run build      # compile & launch backend (update script if needed)
```

(Backend details live in [`be/README.md`](be/README.md).)

---

## Environment variables

Copy `example.env` → `.env` in the repo root and fill required keys (e.g. `FIRECRAWL_API_KEY`).

---

That's it 🎉 – open both URLs and start building! 