# WRXS Style Guide

This document defines the design system, content patterns, and code conventions for the WRXS workout tracking application. All development should follow these guidelines to ensure consistency.

---

## Design System

### Typography

**Case conventions:**
- **Sentence case everywhere** - All headers, labels, buttons, and content use sentence case (only first word capitalized)
- Examples:
  - ✅ "Add workout"
  - ✅ "Workout plans"
  - ✅ "Personal trainer"
  - ❌ "Add Workout" (Title Case)
  - ❌ "WORKOUT PLANS" (All Caps)

**Font hierarchy:**
- Page titles: `<h1>` - Large, bold
- Section headers: `<h2>`, `<h3>` - Medium weight
- Body text: Default font, readable size
- Labels: Slightly smaller, medium weight

### Colors

**Primary palette:**
```css
--primary-blue: #007bff;
--primary-hover: #0056b3;
--danger-red: #dc3545;
--danger-hover: #c82333;
--success-green: #28a745;
--warning-yellow: #ffc107;
--text-primary: #333;
--text-secondary: #666;
--text-muted: #999;
--border-color: #ddd;
--background-light: #f8f9fa;
```

**Special gradients:**
- AI features: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Used for: Personal trainer cards, AI suggestions, AI-related CTAs

**Semantic usage:**
- Primary actions: Blue (#007bff)
- Destructive actions: Red (#dc3545)
- Success states: Green (#28a745)
- AI/intelligent features: Purple gradient
- Disabled states: Gray with reduced opacity

### Buttons

**Primary button:**
```css
background-color: #007bff;
color: white;
padding: 10px 20px;
border: none;
border-radius: 4px;
cursor: pointer;
font-size: 14px;
```

**Secondary button:**
```css
background-color: #6c757d;
color: white;
/* Same padding/border/cursor as primary */
```

**Danger button:**
```css
background-color: #dc3545;
color: white;
/* Same padding/border/cursor as primary */
```

**Button states:**
- Hover: Darken background by ~10%
- Disabled: `opacity: 0.6; cursor: not-allowed;`
- Loading: Show spinner, disable interaction

**Button sizing:**
- Default: `padding: 10px 20px; font-size: 14px;`
- Small: `padding: 8px 16px; font-size: 13px;`
- Large: `padding: 12px 24px; font-size: 16px;`

### Spacing

**Consistent spacing scale:**
```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-xxl: 48px;
```

**Application:**
- Card padding: 24px (--space-lg)
- Section margins: 32px (--space-xl)
- Form field spacing: 16px (--space-md)
- Inline elements: 8px (--space-sm)
- Tab padding: 10px 20px

### Cards

**Standard card:**
```css
background: white;
border-radius: 8px;
padding: 24px;
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
margin-bottom: 24px;
```

**Card with gradient (AI features):**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
border-radius: 8px;
padding: 24px;
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
```

### Forms

**Form groups:**
```css
margin-bottom: 16px;
```

**Labels:**
```css
display: block;
margin-bottom: 8px;
font-weight: 500;
color: #333;
```

**Inputs/Selects:**
```css
width: 100%;
padding: 10px;
border: 1px solid #ddd;
border-radius: 4px;
font-size: 14px;
```

**Input states:**
- Focus: `border-color: #007bff; outline: none;`
- Error: `border-color: #dc3545;`
- Disabled: `background-color: #f8f9fa; cursor: not-allowed;`

---

## Content Patterns

### Button Labels

**Rule: Use only the verb of the action**

Examples:
- ✅ "Add workout"
- ✅ "Save"
- ✅ "Edit"
- ✅ "Delete"
- ✅ "Cancel"
- ✅ "Generate program"
- ❌ "Click here to add a workout"
- ❌ "Save changes"
- ❌ "Delete this item"

**Context-specific verbs:**
- Creating: "Add [noun]", "Create [noun]"
- Editing: "Edit", "Update"
- Deleting: "Delete", "Remove"
- Saving: "Save"
- Canceling: "Cancel"
- Navigation: "View [noun]", "Go to [noun]"

### Headers

**Page headers (h1):**
- Application name: "WRXS"
- Page titles: "Dashboard", "Workouts", "Exercises", "Profile"

**Section headers (h2/h3):**
- "Account info"
- "Gyms and equipment"
- "Preferences"
- "Today's workout"
- "Recent workouts"
- "Active programs"

**Rule: Keep headers concise (1-3 words)**

### Empty States

**Pattern: Brief statement + helpful action**

Examples:
- "No workout logs yet." + [Add workout] button
- "No active programs." + [Generate program] button
- "No gym profiles created." + [Add equipment] button
- "No exercises logged today." + [Start workout] button

**Don't use:**
- Long explanatory text
- Overly friendly/casual tone ("Looks like you haven't...")
- Multiple CTAs in empty state

### Success/Error Messages

**Success messages:**
- "Workout logged successfully"
- "Profile updated"
- "Program generated"
- "Gym profile created"

**Error messages:**
- "Failed to save workout"
- "Email already registered"
- "Username already taken"
- "Could not load data"

**Pattern:**
- Brief, specific, actionable
- Use past tense for completed actions
- Use present tense for ongoing issues

### Placeholder Text

**Inputs:**
- Email: "you@example.com"
- Location: "e.g., Toronto, ON"
- Gym name: "e.g., My local gym"
- Weight: "70"
- Height: "175"

**Pattern: Use realistic examples, not instructions**
- ✅ "e.g., Toronto, ON"
- ❌ "Enter your location"

### Navigation Labels

**Main navigation:**
- Dashboard
- Workouts
- Exercises
- Profile

**Tab navigation:**
- Preferences
- Settings
- AI suggestions
- History
- Plans
- AI trainer

**Rule: Single word or simple noun phrase**

---

## UI Patterns

### Tab Navigation

**Structure:**
```jsx
<div className="tabs">
  <button
    className={activeTab === 'history' ? 'active' : ''}
    onClick={() => setActiveTab('history')}
  >
    History
  </button>
  <button
    className={activeTab === 'plans' ? 'active' : ''}
    onClick={() => setActiveTab('plans')}
  >
    Plans
  </button>
</div>
```

**Styling:**
```css
.tabs {
  display: flex;
  gap: 16px;
  border-bottom: 2px solid #ddd;
  margin-bottom: 24px;
}

.tabs button {
  background: none;
  border: none;
  padding: 12px 16px;
  cursor: pointer;
  color: #666;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
}

.tabs button.active {
  color: #007bff;
  border-bottom-color: #007bff;
  font-weight: 500;
}
```

### Inline Editing Pattern

**Structure:**
```jsx
{editing ? (
  <div>
    <input value={value} onChange={handleChange} />
    <button onClick={handleSave}>Save</button>
    <button onClick={handleCancel}>Cancel</button>
  </div>
) : (
  <div>
    <p>{value || 'Not set'}</p>
    <button onClick={() => setEditing(true)}>Edit</button>
  </div>
)}
```

**Usage:**
- Account settings (username, email, location)
- Profile preferences that need validation
- Any field that should show display vs edit mode

### Modal/Form Overlays

**When to use:**
- Creating new items (workout plans, gym profiles)
- Confirming destructive actions
- Multi-step forms

**When NOT to use:**
- Simple toggles or dropdowns
- Inline editing (use inline editing pattern)
- Navigation (use links)

**Structure:**
```jsx
{showModal && (
  <div className="modal-overlay">
    <div className="modal-content">
      <h3>Modal title</h3>
      {/* Form content */}
      <div className="modal-actions">
        <button onClick={handleSubmit}>Save</button>
        <button onClick={handleClose}>Cancel</button>
      </div>
    </div>
  </div>
)}
```

### Loading States

**Patterns:**
- Full page loading: Centered spinner
- Section loading: Spinner in card
- Button loading: "Loading..." text or inline spinner
- Lazy loading: "Load more" button

**Don't use:**
- Generic "Please wait..." messages
- Blocking spinners for fast operations (<200ms)

### Error States

**Display patterns:**
- Inline errors: Red text below input
- Form errors: Alert box above form
- Page errors: Card with error icon and message
- Toast notifications: Top-right corner, auto-dismiss

**Content pattern:**
```
[What happened] - [Why] - [What to do]
Example: "Failed to save workout - Network error - Please try again"
```

### Badges and Status Indicators

**Program status:**
- Active: Green badge
- Completed: Gray badge
- Archived: Light gray badge

**Difficulty levels:**
- Easy: Green
- Moderate: Yellow
- Hard: Orange
- Very Hard: Red

**Styling:**
```css
.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}
```

---

## Code Conventions

### React Components

**File naming:**
- PascalCase: `WorkoutLogs.js`, `PersonalTrainer.js`
- One component per file
- Match component name to filename

**Component structure:**
```jsx
import React, { useState, useEffect } from 'react';

function ComponentName({ prop1, prop2 }) {
  // State
  const [state, setState] = useState(initialValue);

  // Effects
  useEffect(() => {
    // Effect logic
  }, [dependencies]);

  // Handlers
  const handleAction = () => {
    // Handler logic
  };

  // Render helpers (if needed)
  const renderSection = () => {
    return <div>...</div>;
  };

  // Main render
  return (
    <div>
      {/* JSX */}
    </div>
  );
}

export default ComponentName;
```

**Props:**
- Destructure in function signature
- Use PropTypes or TypeScript for type safety (future enhancement)
- Pass only necessary props

**State management:**
- Use `useState` for component state
- Use `useEffect` for side effects
- Fetch data on mount, update on dependency changes
- Clear intervals/listeners on unmount

### API Patterns

**Fetch pattern:**
```javascript
const fetchData = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/endpoint', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      setData(data);
    } else {
      // Handle error
      console.error('Error:', response.statusText);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
```

**POST/PUT pattern:**
```javascript
const saveData = async (payload) => {
  try {
    const response = await fetch('http://localhost:8000/api/endpoint', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      const data = await response.json();
      // Update state, show success
    } else {
      // Handle error
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
```

**DELETE pattern:**
```javascript
const deleteItem = async (id) => {
  try {
    const response = await fetch(`http://localhost:8000/api/endpoint/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      // Refresh data
      fetchData();
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### Inline Styles

**When to use:**
- Dynamic styles based on state
- One-off styles specific to a component
- Gradient backgrounds (AI features)

**When NOT to use:**
- Reusable styles (use CSS classes)
- Complex responsive layouts
- Hover/focus states (use CSS)

**Pattern:**
```jsx
<div style={{
  backgroundColor: '#007bff',
  padding: '24px',
  borderRadius: '8px',
  marginBottom: '24px'
}}>
  Content
</div>
```

**Gradient pattern (AI features):**
```jsx
<div style={{
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  color: 'white',
  padding: '24px',
  borderRadius: '8px',
  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
}}>
  AI Content
</div>
```

### Backend Patterns

**Router structure:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/api/resource", tags=["resource"])

@router.get("/", response_model=List[schemas.Resource])
def get_resources(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """Docstring describing endpoint"""
    # Implementation
    pass
```

**Model pattern:**
```python
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class ModelName(Base):
    __tablename__ = "table_name"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Other columns

    # Relationships
    user = relationship("User", back_populates="related_field")
```

**Schema pattern:**
```python
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResourceBase(BaseModel):
    field1: str
    field2: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    field1: Optional[str] = None
    field2: Optional[str] = None

class Resource(ResourceBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

---

## Accessibility Guidelines

### Semantic HTML

- Use proper heading hierarchy (h1 → h2 → h3)
- Use `<button>` for actions, `<a>` for navigation
- Use `<label>` elements for all form inputs
- Use semantic elements: `<nav>`, `<main>`, `<section>`, `<article>`

### Keyboard Navigation

- All interactive elements must be keyboard accessible
- Visible focus states on all focusable elements
- Logical tab order
- Support Enter/Space for button activation

### Color Contrast

- Text on white: Minimum #666 for body text
- Buttons: Ensure text contrasts with background
- Links: Underline or sufficient color contrast
- Status indicators: Don't rely on color alone (use text/icons)

### Forms

- All inputs have associated labels
- Error messages are associated with inputs
- Required fields are indicated
- Validation happens on submit, not on blur

---

## File Organization

### Frontend Structure
```
/frontend
  /src
    /components
      Component.js (one component per file)
    App.js (main app and routing)
    index.js (entry point)
    index.css (global styles)
```

### Backend Structure
```
/backend
  /app
    /routers
      resource.py (API endpoints)
    /services
      service.py (business logic)
    models.py (database models)
    schemas.py (Pydantic schemas)
    auth.py (authentication logic)
    config.py (configuration)
    database.py (database setup)
    main.py (FastAPI app)
```

---

## Version Control

### Commit Messages

**Pattern:** `type: Brief description`

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `style:` Formatting changes
- `docs:` Documentation updates
- `test:` Adding tests

**Examples:**
- `feat: Add gym profile management`
- `fix: Correct workout log date display`
- `refactor: Reorganize Profile component tabs`
- `style: Update button padding consistency`

### Branch Naming

**Pattern:** `type/brief-description`

**Examples:**
- `feat/gym-profiles`
- `fix/login-error`
- `refactor/profile-tabs`

---

## Testing Patterns (Future)

### Frontend Tests
- Component rendering
- User interactions
- API integration
- Form validation

### Backend Tests
- Endpoint responses
- Authentication
- Database operations
- Data validation

---

## Performance Guidelines

### Frontend
- Lazy load routes (future enhancement)
- Debounce search inputs
- Optimize re-renders (use React.memo when needed)
- Fetch data only when needed

### Backend
- Use database indexes on foreign keys
- Limit query results (pagination)
- Cache expensive computations
- Optimize N+1 queries with joins

---

## Future Enhancements

- Add TypeScript for type safety
- Implement comprehensive testing
- Add animation library (Framer Motion)
- Implement proper toast notification system
- Add i18n for internationalization
- Implement proper error boundary components
- Add analytics tracking

---

**Last Updated:** December 2024
**Version:** 1.0
