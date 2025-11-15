# 🎨 Frontend Documentation

Complete guide to the React frontend architecture, components, and development patterns.

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Hooks & State Management](#hooks--state-management)
- [API Integration](#api-integration)
- [UI Components](#ui-components)
- [Styling System](#styling-system)
- [Development Patterns](#development-patterns)

## 🎯 Overview

The frontend is built with:
- **React 19** - Latest React with concurrent features
- **TypeScript** - Type safety and better DX
- **Vite** - Lightning-fast development and builds
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautiful, accessible component library

**Port:** 5000  
**Build Tool:** Vite  
**Package Manager:** npm

## 📁 Project Structure

```
src/
├── components/          # React components
│   ├── ui/             # shadcn/ui base components
│   │   ├── button.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   └── [30+ components]
│   ├── Sidebar.tsx     # Main navigation
│   ├── MainContent.tsx # Content area router
│   ├── LiveTranscription.tsx
│   ├── DatabaseStatus.tsx
│   ├── InterviewManager.tsx
│   └── [feature components]
├── hooks/              # Custom React hooks
│   ├── useSupabase.ts
│   ├── useMeetstreamSocket.ts
│   └── [other hooks]
├── lib/                # Utilities
│   ├── api.ts          # ⚠️ API client (CRITICAL)
│   ├── utils.ts        # Helper functions
│   └── constants.ts
├── styles/             # Global styles
├── App.tsx             # Root component
├── main.tsx            # Entry point
└── vite-env.d.ts       # Type definitions
```

## 🧩 Core Components

### App.tsx - Root Component

The main application container that sets up routing and layout.

```typescript
// src/App.tsx
function App() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const { isConnected } = useSupabaseConnection();

  return (
    <div className="flex h-screen">
      <Sidebar 
        activeSection={activeSection}
        onSectionChange={setActiveSection}
        isConnected={isConnected}
      />
      <MainContent 
        activeSection={activeSection}
        isConnected={isConnected}
      />
      <Toaster richColors />
    </div>
  );
}
```

**Key Features:**
- Section routing via state
- Database connection monitoring
- Toast notifications
- Full-height layout

### Sidebar.tsx - Navigation

Left sidebar for application navigation.

**Props:**
```typescript
interface SidebarProps {
  activeSection: string;
  onSectionChange: (section: string) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
  isConnected: boolean;
}
```

**Sections:**
- Dashboard
- Data Ingestion
- Data Playground
- Thought Nuggets
- Podcast Intelligence
- Meeting Agent
- Brain Discussion
- Repository
- Settings

### MainContent.tsx - Content Router

Routes to different feature components based on active section.

```typescript
function MainContent({ activeSection, isConnected }) {
  return (
    <main className="flex-1 overflow-auto">
      {activeSection === 'dashboard' && <Dashboard />}
      {activeSection === 'data-ingestion' && <DataIngestion />}
      {activeSection === 'thought-nuggets' && <LiveTranscription />}
      {/* ... other sections */}
    </main>
  );
}
```

### LiveTranscription.tsx - Audio Recording

Real-time audio transcription interface.

**Features:**
- Start/stop recording
- Real-time transcript display
- Speaker identification
- Export functionality
- WebSocket integration

**Key Code:**
```typescript
const startRecording = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const recorder = new MediaRecorder(stream);
  
  recorder.ondataavailable = async (event) => {
    const formData = new FormData();
    formData.append('audio', event.data);
    
    await fetch(`${API_BASE_URL}/audio-transcription/chunk`, {
      method: 'POST',
      body: formData
    });
  };
  
  recorder.start(1000); // Send chunks every second
};
```

### InterviewManager.tsx - Document Management

Manages interviews and research documents.

**Features:**
- Upload documents
- View document list
- Search documents
- Delete/archive documents

## 🎣 Hooks & State Management

### useMeetstreamSocket.ts - WebSocket Hook

**Critical Pattern:** Singleton socket connection.

```typescript
// Singleton instance (outside hook)
let socketInstance: Socket | null = null;
let activeBotsList: Record<string, BotCreatedEvent> = {};

export function useMeetstreamSocket() {
  const [activeBots, setActiveBots] = useState(activeBotsList);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Create socket only once
    if (!socketInstance) {
      socketInstance = io(SOCKET_URL, {
        transports: ['websocket', 'polling'],
        reconnection: true
      });

      socketInstance.on('connect', () => {
        console.log('Socket connected');
        setIsConnected(true);
      });

      socketInstance.on('bot_created', (bot) => {
        activeBotsList[bot.botId] = bot;
        setActiveBots({ ...activeBotsList });
      });
    }

    return () => {
      // Don't disconnect - shared instance!
    };
  }, []);

  const sendAgentMessage = useCallback((message: string) => {
    if (socketInstance) {
      socketInstance.emit('agent_message', { message });
    }
  }, []);

  return {
    socket: socketInstance,
    activeBots,
    isConnected,
    sendAgentMessage
  };
}
```

**Why Singleton?**
- Multiple components need the same socket
- Prevents duplicate connections
- Shared state across components
- Better resource management

### useSupabase.ts - Database Hook

Manages database connection status.

```typescript
export function useSupabaseConnection() {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        setIsConnected(data.database === 'connected');
      } catch (error) {
        setIsConnected(false);
      }
    };

    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  return { isConnected };
}
```

## 🔌 API Integration

### API Client Pattern (CRITICAL!)

**Location:** `/src/lib/api.ts`

**The Golden Rule:**
> ALL backend API calls MUST use `API_BASE_URL` from this file.

```typescript
// src/lib/api.ts
export const API_BASE_URL = 
  import.meta.env.VITE_API_URL || 'http://localhost:3001/api/v1';

// Helper for auth headers
const authHeaders = (headers = {}) => {
  const token = localStorage.getItem('auth_token');
  return token ? { ...headers, Authorization: `Bearer ${token}` } : headers;
};

// API modules
export const dataIngestionAPI = {
  uploadFile: async (file: File, options) => {
    const formData = new FormData();
    formData.append('file', file);
    if (options?.title) formData.append('title', options.title);

    const response = await fetch(`${API_BASE_URL}/data-ingestion/upload`, {
      method: 'POST',
      headers: authHeaders(),
      body: formData
    });
    return response.json();
  },

  getRecentUploads: async (limit = 10) => {
    const response = await fetch(
      `${API_BASE_URL}/data-ingestion/recent?limit=${limit}`,
      { headers: authHeaders() }
    );
    return response.json();
  }
};

export const meetstreamAPI = {
  createBot: async (data) => {
    const response = await fetch(`${API_BASE_URL}/meetstream/bot`, {
      method: 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(data)
    });
    return response.json();
  }
};

// ... more API modules
```

**Usage in Components:**

```typescript
import { API_BASE_URL, dataIngestionAPI } from '@/lib/api';

function UploadComponent() {
  const handleUpload = async (file: File) => {
    try {
      const result = await dataIngestionAPI.uploadFile(file, {
        title: 'My Document'
      });
      console.log('Uploaded:', result);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };
}
```

**Why This Pattern?**
- Works in desktop dev mode (different ports)
- Works in cloud deployment (same domain)
- Works in Electron app
- Single source of truth for API URL
- Easy to mock for testing

## 🎨 UI Components (shadcn/ui)

### Component Library

All UI components from shadcn/ui in `/src/components/ui/`:

**Form Components:**
- `button.tsx` - Buttons with variants
- `input.tsx` - Text inputs
- `textarea.tsx` - Multi-line text
- `select.tsx` - Dropdowns
- `checkbox.tsx` - Checkboxes
- `radio-group.tsx` - Radio buttons
- `switch.tsx` - Toggle switches

**Layout Components:**
- `card.tsx` - Card containers
- `dialog.tsx` - Modal dialogs
- `sheet.tsx` - Slide-out panels
- `tabs.tsx` - Tab navigation
- `accordion.tsx` - Collapsible sections

**Data Display:**
- `table.tsx` - Data tables
- `badge.tsx` - Status badges
- `avatar.tsx` - User avatars
- `progress.tsx` - Progress bars

**Feedback:**
- `alert-dialog.tsx` - Confirmation dialogs
- `toast.tsx` (via sonner) - Notifications
- `tooltip.tsx` - Hover tooltips

### Using Components

```typescript
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';

function MyComponent() {
  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Upload Document</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <Input placeholder="Document title" />
          <Button onClick={handleUpload}>Upload</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

## 🎨 Styling System

### Tailwind CSS

Utility-first CSS framework for rapid UI development.

**Configuration:** `tailwind.config.js`

**Common Patterns:**

```tsx
// Layout
<div className="flex flex-col h-screen">
  <header className="border-b">Header</header>
  <main className="flex-1 overflow-auto">Content</main>
</div>

// Responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map(item => <Card key={item.id} />)}
</div>

// Dark mode support
<div className="bg-white dark:bg-gray-900 text-black dark:text-white">
  Content
</div>

// Hover/Focus states
<button className="bg-blue-500 hover:bg-blue-600 focus:ring-2 focus:ring-blue-400">
  Click me
</button>
```

### CSS Variables

Custom colors and themes in `index.css`:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --secondary: 210 40% 96.1%;
  /* ... more variables */
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... dark mode overrides */
}
```

## 📝 Development Patterns

### Creating New Components

**1. Feature Component Template:**

```typescript
// src/components/MyFeature.tsx
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { API_BASE_URL } from '@/lib/api';

interface MyFeatureProps {
  userId: string;
  onComplete?: () => void;
}

export function MyFeature({ userId, onComplete }: MyFeatureProps) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, [userId]);

  const loadData = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/my-endpoint`);
      const result = await response.json();
      setData(result.data);
    } catch (error) {
      console.error('Failed to load:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async () => {
    // Handle action
    onComplete?.();
  };

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">My Feature</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="space-y-2">
          {data.map(item => (
            <div key={item.id}>{item.name}</div>
          ))}
        </div>
      )}
      <Button onClick={handleAction}>Action</Button>
    </div>
  );
}
```

### State Management Patterns

**Local State:**
```typescript
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);
```

**Derived State:**
```typescript
const filteredItems = items.filter(item => item.active);
const totalPrice = items.reduce((sum, item) => sum + item.price, 0);
```

**Async State:**
```typescript
const [data, setData] = useState([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);

useEffect(() => {
  setLoading(true);
  fetchData()
    .then(setData)
    .catch(err => setError(err.message))
    .finally(() => setLoading(false));
}, [dependency]);
```

### Performance Optimization

**Memoization:**
```typescript
import { useMemo, useCallback } from 'react';

// Expensive calculation
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

// Event handler
const handleClick = useCallback(() => {
  doSomething(value);
}, [value]);

// Component memoization
const MemoizedComponent = React.memo(MyComponent);
```

### Error Handling

```typescript
import { toast } from 'sonner';

try {
  const result = await apiCall();
  toast.success('Operation successful!');
} catch (error) {
  console.error('Operation failed:', error);
  toast.error('Operation failed. Please try again.');
}
```

## 🧪 Testing Components

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from './MyComponent';

test('renders component', () => {
  render(<MyComponent />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});

test('handles click', () => {
  const handleClick = jest.fn();
  render(<MyComponent onClick={handleClick} />);
  
  fireEvent.click(screen.getByRole('button'));
  expect(handleClick).toHaveBeenCalled();
});
```

## 🚀 Building for Production

```bash
# Build frontend
npm run build

# Output: dist/ directory with optimized files

# Preview build
npm run preview
```

**Build optimizations:**
- Code splitting
- Tree shaking
- Minification
- Asset optimization
- Source maps (in dev)

## 📚 Next Steps

- **[Backend Documentation](./05_BACKEND.md)** - Understanding the API
- **[Data Flow](./08_DATA_FLOW.md)** - How data moves through system
- **[API Reference](./06_API_REFERENCE.md)** - Complete API docs

---

**Key Takeaways:**
1. Always use `API_BASE_URL` for backend calls
2. Use singleton pattern for WebSocket connections
3. Follow shadcn/ui component patterns
4. Optimize with memo/callback when needed
5. Handle errors gracefully with toasts
