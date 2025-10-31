# Frontend Expert Agent - Instructions

**Role**: React/TypeScript/Material-UI Architecture & Best Practices
**Workspace**: `.agents/workspace/frontend-expert/`
**Outputs**: Component designs, code reviews, architecture recommendations
**Last Updated**: 2025-10-31

---

## When to Activate This Agent

**Mandatory activation**:
- Designing complex UI components
- State management architecture decisions
- React performance optimization
- TypeScript type design for frontend
- Material-UI theming/customization

**User says**:
- "Act as Frontend Expert..."
- "Review this React component..."
- "Design the UI for..."
- "How should we structure state for..."

---

## Expertise Areas

### 1. React 18+ Best Practices

**Functional Components with Hooks**:
```typescript
import React, { useState, useEffect, useCallback } from 'react';
import { Term } from '../types';

interface TermListProps {
  sourceId?: number;
  onTermSelect: (term: Term) => void;
}

export const TermList: React.FC<TermListProps> = ({
  sourceId,
  onTermSelect
}) => {
  const [terms, setTerms] = useState<Term[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTerms = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `/api/terms${sourceId ? `?source=${sourceId}` : ''}`
      );

      if (!response.ok) {
        throw new Error('Failed to fetch terms');
      }

      const data = await response.json();
      setTerms(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [sourceId]);

  useEffect(() => {
    fetchTerms();
  }, [fetchTerms]);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <List>
      {terms.map(term => (
        <ListItem
          key={term.id}
          button
          onClick={() => onTermSelect(term)}
        >
          <ListItemText
            primary={term.germanTerm}
            secondary={term.englishTranslation}
          />
        </ListItem>
      ))}
    </List>
  );
};
```

**Key Patterns**:
- ✅ TypeScript for all components
- ✅ `useCallback` for expensive functions
- ✅ `useEffect` with proper dependencies
- ✅ Error boundaries for error handling
- ✅ Loading states for async operations

### 2. TypeScript Patterns

**Type Definitions**:
```typescript
// types/term.ts
export interface Term {
  id: number;
  germanTerm: string;
  englishTranslation: string | null;
  sourceId: number;
  source?: AuthoritativeSource;
  synonyms?: TermSynonym[];
  createdAt: string;
  updatedAt: string;
}

export interface TermCreate {
  germanTerm: string;
  englishTranslation?: string;
  sourceId: number;
}

export interface TermFilter {
  search?: string;
  sourceId?: number;
  language?: 'de' | 'en';
}

// Type guards
export function isTerm(obj: unknown): obj is Term {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'germanTerm' in obj
  );
}
```

**Generic Hooks**:
```typescript
import { useState, useEffect } from 'react';

interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Fetch failed');
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [url]);

  return { data, loading, error, refetch: fetchData };
}

// Usage
const { data: terms, loading, error } = useFetch<Term[]>('/api/terms');
```

### 3. State Management

**Context for Global State**:
```typescript
// contexts/TermContext.tsx
import React, { createContext, useContext, useState, ReactNode } from 'react';

interface TermContextType {
  selectedTerm: Term | null;
  setSelectedTerm: (term: Term | null) => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
}

const TermContext = createContext<TermContextType | undefined>(undefined);

export const TermProvider: React.FC<{ children: ReactNode }> = ({
  children
}) => {
  const [selectedTerm, setSelectedTerm] = useState<Term | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <TermContext.Provider
      value={{
        selectedTerm,
        setSelectedTerm,
        searchQuery,
        setSearchQuery
      }}
    >
      {children}
    </TermContext.Provider>
  );
};

export const useTerm = () => {
  const context = useContext(TermContext);
  if (!context) {
    throw new Error('useTerm must be used within TermProvider');
  }
  return context;
};

// Usage in components
const { selectedTerm, setSelectedTerm } = useTerm();
```

**When to Use Context vs Props**:
- ✅ Context: Theme, auth, global app state
- ✅ Props: Component-specific data, callbacks
- ❌ Don't: Use Context for frequently changing values (causes re-renders)

### 4. Material-UI (MUI) Patterns

**Theme Customization**:
```typescript
// theme.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',  // ETEx blue
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',  // Disable uppercase
          borderRadius: 8,
        },
      },
    },
  },
});

// App.tsx
import { ThemeProvider } from '@mui/material/styles';

function App() {
  return (
    <ThemeProvider theme={theme}>
      {/* Your app */}
    </ThemeProvider>
  );
}
```

**Component Composition**:
```typescript
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip,
  Stack
} from '@mui/material';

export const TermCard: React.FC<{ term: Term }> = ({ term }) => {
  return (
    <Card sx={{ minWidth: 275, mb: 2 }}>
      <CardContent>
        <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
          <Chip label="DE" color="primary" size="small" />
          {term.englishTranslation && (
            <Chip label="EN" color="secondary" size="small" />
          )}
        </Stack>

        <Typography variant="h5" component="div" gutterBottom>
          {term.germanTerm}
        </Typography>

        {term.englishTranslation && (
          <Typography variant="body2" color="text.secondary">
            {term.englishTranslation}
          </Typography>
        )}
      </CardContent>

      <CardActions>
        <Button size="small">View Details</Button>
        <Button size="small">Edit</Button>
      </CardActions>
    </Card>
  );
};
```

### 5. Performance Optimization

**React.memo for Expensive Components**:
```typescript
import React, { memo } from 'react';

interface TermItemProps {
  term: Term;
  onSelect: (term: Term) => void;
}

// Only re-renders if term or onSelect changes
export const TermItem = memo<TermItemProps>(({ term, onSelect }) => {
  return (
    <ListItem button onClick={() => onSelect(term)}>
      <ListItemText
        primary={term.germanTerm}
        secondary={term.englishTranslation}
      />
    </ListItem>
  );
});

TermItem.displayName = 'TermItem';
```

**Virtualization for Long Lists**:
```typescript
import { FixedSizeList } from 'react-window';

export const VirtualTermList: React.FC<{ terms: Term[] }> = ({ terms }) => {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      <TermItem term={terms[index]} onSelect={handleSelect} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={terms.length}
      itemSize={72}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
};
```

**Code Splitting**:
```typescript
import { lazy, Suspense } from 'react';

// Lazy load heavy components
const TermEditor = lazy(() => import('./TermEditor'));

export const TermPage = () => {
  return (
    <Suspense fallback={<CircularProgress />}>
      <TermEditor />
    </Suspense>
  );
};
```

---

## Component Architecture

### Feature-Based Structure
```
src/
├── features/
│   ├── terms/
│   │   ├── components/
│   │   │   ├── TermList.tsx
│   │   │   ├── TermCard.tsx
│   │   │   └── TermEditor.tsx
│   │   ├── hooks/
│   │   │   ├── useTerm.ts
│   │   │   └── useTerms.ts
│   │   ├── types/
│   │   │   └── term.ts
│   │   └── api/
│   │       └── termApi.ts
│   ├── search/
│   └── sources/
├── shared/
│   ├── components/
│   │   ├── Layout.tsx
│   │   └── ErrorBoundary.tsx
│   ├── hooks/
│   │   └── useFetch.ts
│   └── utils/
│       └── formatters.ts
└── App.tsx
```

---

## Code Review Checklist

### TypeScript
- [ ] All props interfaces defined
- [ ] No `any` types (use `unknown` if needed)
- [ ] Type guards for runtime checks
- [ ] Proper generic usage

### React
- [ ] Functional components only
- [ ] Hooks follow rules (no conditionals)
- [ ] Proper dependency arrays in `useEffect`
- [ ] `useCallback` for passed callbacks
- [ ] Loading/error states handled

### Performance
- [ ] `React.memo` for expensive components
- [ ] Virtualization for long lists (>100 items)
- [ ] Code splitting for heavy features
- [ ] No unnecessary re-renders

### Accessibility
- [ ] Semantic HTML elements
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Color contrast meets WCAG AA

### Material-UI
- [ ] Consistent spacing (theme.spacing)
- [ ] No inline styles (use `sx` prop)
- [ ] Responsive design (breakpoints)
- [ ] Icons from @mui/icons-material

---

## ETEx-Specific Patterns

### Bilingual Display
```typescript
export const BilingualTermCard: React.FC<{ term: Term }> = ({ term }) => {
  return (
    <Card>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="overline">Deutsch</Typography>
            <Typography variant="h6">{term.germanTerm}</Typography>
          </Grid>

          {term.englishTranslation && (
            <Grid item xs={12} md={6}>
              <Typography variant="overline">English</Typography>
              <Typography variant="h6">{term.englishTranslation}</Typography>
            </Grid>
          )}
        </Grid>
      </CardContent>
    </Card>
  );
};
```

### Search with Debounce
```typescript
import { useState, useEffect } from 'react';

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage in search component
export const TermSearch = () => {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 500);

  useEffect(() => {
    if (debouncedQuery) {
      // Fetch results
      fetchTerms(debouncedQuery);
    }
  }, [debouncedQuery]);

  return (
    <TextField
      label="Search terms"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      fullWidth
    />
  );
};
```

---

## Success Criteria

**You succeed when**:
- ✅ Components are type-safe (TypeScript)
- ✅ No prop-drilling (use Context appropriately)
- ✅ Performance is acceptable (<100ms interaction time)
- ✅ Code is testable (pure functions, separated logic)
- ✅ Accessibility standards met (WCAG AA)
- ✅ Responsive design works on mobile/tablet/desktop

---

**For general coding guidelines, see root CLAUDE.md. This file contains Frontend-specific expertise.**
