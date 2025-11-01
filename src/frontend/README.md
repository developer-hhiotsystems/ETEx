# ETEx Frontend

React 18 + TypeScript + Vite + Material-UI (MUI) v5

## Development

```bash
cd src/frontend
npm install
npm run dev
```

Frontend dev server: http://localhost:5173

## Build

```bash
npm run build
```

Output: `dist/` directory

## Architecture

- **React 18**: Functional components with hooks
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server
- **Material-UI v5**: Component library
- **React Router v6**: Client-side routing
- **Axios**: HTTP client for API calls

## API Proxy

The Vite dev server proxies `/api/*` requests to the backend at `http://localhost:8000`.

Example:
```typescript
// Frontend makes request to /api/terms
// Vite proxies to http://localhost:8000/api/terms
const response = await axios.get('/api/terms');
```

## Project Structure

```
src/frontend/
├── public/           # Static assets
├── src/
│   ├── components/   # Reusable React components
│   ├── pages/        # Page components (routes)
│   ├── hooks/        # Custom React hooks
│   ├── utils/        # Utility functions
│   ├── types/        # TypeScript type definitions
│   ├── App.tsx       # Main app component
│   ├── main.tsx      # Entry point
│   └── index.css     # Global styles
├── index.html        # HTML template
├── vite.config.ts    # Vite configuration
└── tsconfig.json     # TypeScript configuration
```

## Code Style

- Use functional components only
- TypeScript for all files (.tsx/.ts)
- Material-UI components with `sx` prop for styling
- No inline styles
- Follow Frontend Expert agent guidelines (see `.agents/frontend-expert/CLAUDE.md`)
