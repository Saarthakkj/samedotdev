- **Prerequisites**
  - Conda installed (https://docs.conda.io/en/latest/miniconda.html)
  - Node.js ⩾ 18 (comes with `npm`)

- **Setup**
  1. `cd be` – move to the backend folder.
  2. Create & activate the Python environment:
     ```bash
     conda env create -f environment.yml
     conda activate agents
     ```
  3. Install Node dependencies:
     ```bash
     pnpm i        # or pnpm install
     ```
  5. Start the development servers (Express 🡒 port 3000, FastAPI 🡒 port 8000):
     ```bash
     npm run dev
     ```

- **Environment variables**
  - Copy `example.env` → `.env` at the repo root and fill in any required keys (e.g. `FIRECRAWL_API_KEY`).

That's it 🎉 – your backend should now be running. 