# TODO List

This document tracks planned features, improvements, and known issues for WRXS.

## 🎯 High Priority

### Core Features

- [ ] **Workout Plan Exercise Management**

  - [ ] Add exercises to workout plans (currently plans exist but can't add exercises)
  - [ ] Implement drag-and-drop reordering of exercises in plans
  - [ ] Add rest time configuration between exercises
  - [ ] Support for supersets and circuit training

- [ ] **Enhanced Progress Tracking**

  - [ ] Personal records (PRs) tracking and highlighting
  - [ ] Progress photos upload and timeline
  - [ ] Body measurements tracking (chest, waist, arms, etc.)
  - [ ] Weight progression graphs per exercise
  - [ ] Volume tracking (total weight lifted per session/week/month)

- [ ] **Mobile Responsiveness**
  - [ ] Optimize UI for mobile devices
  - [ ] Add touch-friendly controls
  - [ ] Implement mobile-first workout logging interface
  - [ ] Test and fix layout issues on various screen sizes

### Testing & Quality

- [ ] **Backend Tests**

  - [ ] Unit tests for all API endpoints
  - [ ] Integration tests for database operations
  - [ ] Test coverage for authentication flow
  - [ ] Test AI suggestion fallback logic

- [ ] **Frontend Tests**
  - [ ] Component tests for all major components
  - [ ] E2E tests for critical user flows
  - [ ] Test form validation
  - [ ] Test error handling and edge cases

## 🚀 Medium Priority

### User Experience

- [ ] **Dashboard Improvements**

  - [ ] Add workout streak tracking
  - [ ] Show upcoming scheduled workouts
  - [ ] Display recent activity feed
  - [ ] Add motivational quotes/tips
  - [ ] Quick action buttons for common tasks

- [ ] **Exercise Library Enhancements**

  - [ ] Add exercise demonstration videos/GIFs
  - [ ] Implement exercise variations and alternatives
  - [ ] Add user ratings and reviews for exercises
  - [ ] Exercise history (when last performed, best performance)
  - [ ] Favorite exercises feature

- [ ] **Workout Logging UX**
  - [ ] Quick log from previous workout (copy sets/reps)
  - [ ] Rest timer between sets
  - [ ] Plate calculator for barbell exercises
  - [ ] Voice input for logging (experimental)
  - [ ] Workout templates for quick logging

### Social Features

- [ ] **Community Features**

  - [ ] Share workout plans with other users
  - [ ] Public workout plan library
  - [ ] Follow other users
  - [ ] Activity feed from followed users
  - [ ] Comments and likes on shared content

- [ ] **Challenges & Gamification**
  - [ ] Create and join fitness challenges
  - [ ] Achievement badges system
  - [ ] Leaderboards (optional, privacy-respecting)
  - [ ] Streak tracking and rewards

### AI & Intelligence

- [ ] **Enhanced AI Features**
  - [ ] Improve AI workout suggestions with user history
  - [ ] Progressive overload recommendations
  - [ ] Deload week suggestions based on volume
  - [ ] Injury prevention alerts (overtraining detection)
  - [ ] Form tips and common mistakes for exercises
  - [ ] Nutrition suggestions integration (optional)

## 📊 Analytics & Reporting

- [ ] **Advanced Analytics**

  - [ ] Weekly/monthly workout summaries
  - [ ] Muscle group balance analysis
  - [ ] Training volume trends
  - [ ] Export data to CSV/PDF
  - [ ] Custom date range reports
  - [ ] Comparison with previous periods

- [ ] **Visualization Improvements**
  - [ ] Interactive charts with zoom/pan
  - [ ] Heatmap of training frequency
  - [ ] Body part training distribution pie charts
  - [ ] Strength progression curves
  - [ ] Volume load graphs

## 🔧 Technical Improvements

### Backend

- [ ] **Database Optimizations**

  - [ ] Add database indexes for frequently queried fields
  - [ ] Implement query pagination for all list endpoints
  - [ ] Add database connection pooling configuration
  - [ ] Set up database backup automation
  - [ ] Implement soft deletes for user data

- [ ] **API Improvements**

  - [ ] Add API rate limiting
  - [ ] Implement request caching for static data
  - [ ] Add API versioning (v1, v2)
  - [ ] Improve error messages and validation
  - [ ] Add request/response logging
  - [ ] OpenAPI schema validation

- [ ] **Security Enhancements**
  - [ ] Add refresh token mechanism
  - [ ] Implement password reset via email
  - [ ] Add two-factor authentication (2FA)
  - [ ] Rate limiting on authentication endpoints
  - [ ] Add CSRF protection
  - [ ] Security headers (HSTS, CSP, etc.)
  - [ ] Regular dependency updates and security audits

### Frontend

- [ ] **Performance Optimizations**

  - [ ] Implement React.lazy for code splitting
  - [ ] Add service worker for offline support
  - [ ] Optimize bundle size
  - [ ] Implement virtual scrolling for long lists
  - [ ] Add loading skeletons
  - [ ] Image lazy loading

- [ ] **State Management**

  - [ ] Consider React Query or SWR for data fetching
  - [ ] Implement optimistic updates
  - [ ] Add proper error boundaries
  - [ ] Centralize API calls in custom hooks

- [ ] **UI/UX Polish**
  - [ ] Add dark mode support
  - [ ] Implement keyboard shortcuts
  - [ ] Add animations and transitions
  - [ ] Improve accessibility (ARIA labels, keyboard navigation)
  - [ ] Add tooltips and help text
  - [ ] Implement undo/redo for certain actions

### DevOps & Infrastructure

- [ ] **CI/CD Pipeline**

  - [ ] Set up GitHub Actions for automated testing
  - [ ] Automated Docker image builds
  - [ ] Automated deployment to staging/production
  - [ ] Automated database migrations
  - [ ] Code quality checks (linting, formatting)

- [ ] **Monitoring & Logging**

  - [ ] Add application monitoring (e.g., Sentry)
  - [ ] Implement structured logging
  - [ ] Set up log aggregation
  - [ ] Add health check endpoints
  - [ ] Performance monitoring and alerting

- [ ] **Documentation**
  - [ ] Add API documentation examples
  - [ ] Create video tutorials
  - [ ] Add inline code documentation
  - [ ] Create deployment guide for various platforms
  - [ ] Add troubleshooting guide

## 🌟 Nice to Have

### Advanced Features

- [ ] **Workout Scheduling**

  - [ ] Calendar view for planned workouts
  - [ ] Recurring workout schedules
  - [ ] Email/push notifications for scheduled workouts
  - [ ] Integration with Google Calendar/Apple Calendar

- [ ] **Nutrition Tracking** (Optional Module)

  - [ ] Meal logging
  - [ ] Calorie and macro tracking
  - [ ] Nutrition goals based on fitness goals
  - [ ] Recipe database
  - [ ] Barcode scanner for food items

- [ ] **Wearable Integration**

  - [ ] Import data from fitness trackers
  - [ ] Heart rate monitoring during workouts
  - [ ] Sleep tracking correlation
  - [ ] Steps and activity tracking

- [ ] **Coach/Trainer Features**
  - [ ] Coach role with client management
  - [ ] Assign workouts to clients
  - [ ] View client progress
  - [ ] Messaging system
  - [ ] Payment integration for coaching services

### Mobile App

- [ ] **Native Mobile Apps**
  - [ ] React Native mobile app
  - [ ] Offline workout logging
  - [ ] Push notifications
  - [ ] Camera integration for progress photos
  - [ ] Apple Health / Google Fit integration

### Integrations

- [ ] **Third-Party Integrations**
  - [ ] Strava integration
  - [ ] MyFitnessPal integration
  - [ ] Fitbit/Apple Watch sync
  - [ ] Spotify workout playlists
  - [ ] YouTube exercise video embedding

## 🐛 Known Issues

- [ ] Fix: URL in README.md line 44 has incorrect format (extra parentheses)
- [ ] Improve: Error handling when OpenAI API is slow/unavailable
- [ ] Fix: Token expiration doesn't trigger automatic logout
- [ ] Improve: Loading states for all async operations
- [ ] Fix: Form validation messages sometimes don't clear

## 📝 Documentation Tasks

- [ ] Add screenshots to README
- [ ] Create user guide
- [ ] Add API usage examples
- [ ] Document environment variables
- [ ] Create contribution guidelines
- [ ] Add code of conduct
- [ ] Create issue templates
- [ ] Add pull request template

## 🔄 Refactoring & Technical Debt

- [ ] Refactor: Extract common API logic into reusable hooks
- [ ] Refactor: Separate concerns in large components
- [ ] Refactor: Create shared UI component library
- [ ] Refactor: Standardize error handling across backend
- [ ] Refactor: Move business logic out of route handlers
- [ ] Update: Upgrade dependencies to latest stable versions
- [ ] Improve: Add TypeScript to frontend (optional)
- [ ] Improve: Add type hints to all Python functions

---

## 📌 Notes

- Items are roughly ordered by priority within each section
- Check off items as they are completed: `- [x]`
- Add dates when items are completed
- Move completed items to a CHANGELOG.md file periodically
- Feel free to add new items as they come up

## 🤝 Contributing

If you'd like to work on any of these items, please:

1. Check if there's already an issue for it
2. Create an issue if one doesn't exist
3. Comment on the issue to claim it
4. Submit a PR when ready

Last updated: 2025-12-26
